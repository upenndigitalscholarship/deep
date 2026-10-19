import re
from collections import defaultdict

from django.db import migrations


# Freeze the mapping here so future application changes cannot change a replay
# of this migration. Preserve populated categories and MoEML links as curated.
LETTER_CATEGORIES = {
    'A': "A-B (Paul's Churchyard)", 'B': "A-B (Paul's Churchyard)",
    'C': 'C (Newgate Within)', 'D': 'D (Newgate Without)', 'E': 'E (Smithfield)',
    'F': 'F (Aldersgate Without)', 'G': 'G (Aldersgate Within)',
    'H': 'H (Cripplegate and Moorgate Within)', 'I': 'I (Cripplegate Without)',
    'N': 'N (Cheapside)', 'O': 'O (Royal Exchange)', 'P': 'P (Leadenhall)',
    'Q': 'Q (Ludgate)', 'R': 'R-T (Thames St)', 'S': 'R-T (Thames St)',
    'T': 'R-T (Thames St)', 'V': 'V (Holborn)', 'W': 'W (Fleet St)',
    'X': 'X (Westminster)',
}
CITY_CATEGORIES = {
    city.casefold(): city for city in (
        'Cambridge', 'Dublin', 'Edinburgh', 'Hague', 'Kilkenny', 'Leiden',
        'Oxford', 'Rochester', 'Southwark',
    )
}
MISSING_VALUES = {'none', 'n/a', 'unknown', '[unknown]', '---', '-'}
CODED_LOCATION = re.compile(r'^([A-Z])(?:\.\d+[a-z]?)?\s*\(.+\)$', re.IGNORECASE)


def category_for_name(name):
    city = CITY_CATEGORIES.get(name.casefold())
    if city:
        return city
    match = CODED_LOCATION.fullmatch(name)
    return LETTER_CATEGORIES.get(match[1].upper()) if match else None


def backfill_imprint_locations(apps, schema_editor):
    Item = apps.get_model('main', 'Item')
    Location = apps.get_model('main', 'StationerImprintLocation')
    database = schema_editor.connection.alias
    valid_categories = {value for value, label in Location._meta.get_field('supra_category').choices}
    locations_by_name = defaultdict(list)
    for location in Location.objects.using(database).select_for_update().order_by('pk'):
        locations_by_name[location.name].append(location)

    # Validate every record before making any changes. Name is not unique, so
    # duplicate matches and conflicting contributor links need explicit review.
    plans = []
    issues = []
    items = Item.objects.using(database).select_for_update().order_by('pk').prefetch_related(
        'stationer_imprint_location_filter'
    )
    for item in items:
        names = list(dict.fromkeys(
            part.strip() for part in (item.stationer_imprint_location_display or '').split(';')
            if part.strip()
        ))
        if not names or all(name.casefold() in MISSING_VALUES for name in names):
            continue
        item_issues = []
        if any(name.casefold() in MISSING_VALUES for name in names):
            item_issues.append('missing-value marker mixed with location names')
        linked = list(item.stationer_imprint_location_filter.all())
        extra_links = [location.name for location in linked if location.name not in names]
        if extra_links:
            item_issues.append(f'existing links differ from display text: {extra_links!r}')
        resolved = []
        for name in names:
            matches = locations_by_name[name]
            if len(matches) > 1:
                item_issues.append(f'duplicate location name {name!r}, IDs {[loc.pk for loc in matches]}')
                continue
            location = matches[0] if matches else None
            category = location.supra_category if location else None
            if category and category not in valid_categories:
                item_issues.append(f'invalid category {category!r} for {name!r}')
                continue
            category = category or category_for_name(name)
            if not category:
                item_issues.append(f'unmapped location {name!r}')
                continue
            resolved.append((name, category))
        if item_issues:
            issues.append(f'DEEP {item.deep_id!r} (pk={item.pk}): ' + '; '.join(item_issues))
        plans.append((item, {location.name for location in linked}, resolved))
    if issues:
        raise RuntimeError(
            '0041 imprint-location backfill requires review; no backfill changes were made. '
            'Resolve these records and run migrate again:\n' + '\n'.join(issues)
        )

    for item, linked_names, resolved in plans:
        for name, category in resolved:
            matches = locations_by_name[name]
            if matches:
                location = matches[0]
                if not location.supra_category:
                    location.supra_category = category
                    location.save(using=database, update_fields=['supra_category'])
            else:
                location = Location.objects.using(database).create(name=name, supra_category=category)
                matches.append(location)
            if name not in linked_names:
                item.stationer_imprint_location_filter.add(location)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_stationer_imprint_location_filter'),
    ]

    operations = [
        # An additive backfill cannot safely distinguish its links from later
        # manual edits. Reversing 0041 therefore retains rows and relationships.
        migrations.RunPython(backfill_imprint_locations, migrations.RunPython.noop, atomic=True),
    ]
