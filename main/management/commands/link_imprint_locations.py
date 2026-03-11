"""
Create StationerImprintLocation rows from distinct Item.stationer_imprint_location_display
values, link items to them, and auto-fill supra_category from name (city exact match or
letter-prefix rule). Run after migrations.
"""
from django.core.management.base import BaseCommand
from main.models import Item, StationerImprintLocation

# Cities: 1:1 match on name
CITY_SUPRAS = {
    'Cambridge', 'Dublin', 'Edinburgh', 'Hague', 'Kilkenny', 'Leiden',
    'Oxford', 'Rochester', 'Southwark',
}

# First character -> supra_category (for letter-prefix locations)
LETTER_TO_SUPRA = {
    'A': "A-B (Paul's Churchyard)",
    'B': "A-B (Paul's Churchyard)",
    'C': "C (Newgate Within)",
    'D': "D (Newgate Without)",
    'E': "E (Smithfield)",
    'F': "F (Aldersgate Without)",
    'G': "G (Aldersgate Within)",
    'H': "H (Cripplegate and Moorgate Within)",
    'I': "I (Cripplegate Without)",
    'N': "N (Cheapside)",
    'O': "O (Royal Exchange)",
    'P': "P (Leadenhall)",
    'Q': "Q (Ludgate)",
    'R': "R-T (Thames St)",
    'S': "R-T (Thames St)",
    'T': "R-T (Thames St)",
    'V': "V (Holborn)",
    'W': "W (Fleet St)",
    'X': "X (Westminster)",
}


def supra_category_for_name(name):
    """Return supra_category for a location name, or None if no rule matches."""
    if not name or not isinstance(name, str):
        return None
    s = name.strip()
    if not s:
        return None
    if s in CITY_SUPRAS:
        return s
    first = s[0].upper()
    return LETTER_TO_SUPRA.get(first)


class Command(BaseCommand):
    help = (
        'Create StationerImprintLocation from distinct stationer_imprint_location_display '
        'values, link items, and set supra_category from name (city or letter-prefix).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Only print what would be done, do not write to DB.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if dry_run:
            self.stdout.write('DRY RUN - no changes will be saved.')

        # 1. Collect distinct location names from display field
        names = set()
        for item in Item.objects.all():
            display = item.stationer_imprint_location_display or ''
            for part in display.split(';'):
                s = part.strip()
                if s:
                    names.add(s)

        self.stdout.write(f'Distinct location names: {len(names)}')

        # 2. Get or create StationerImprintLocation for each name; set supra_category
        name_to_sil = {}
        for name in sorted(names):
            if dry_run:
                supra = supra_category_for_name(name)
                self.stdout.write(f'  Would get_or_create: name={name!r}, supra_category={supra!r}')
                continue
            sil, created = StationerImprintLocation.objects.get_or_create(
                name=name,
                defaults={'supra_category': supra_category_for_name(name)},
            )
            if not created and not sil.supra_category:
                sil.supra_category = supra_category_for_name(name)
                sil.save()
            name_to_sil[name] = sil

        if dry_run:
            self.stdout.write('Would link items next (skipped in dry-run).')
            return

        # 3. Link each item to its StationerImprintLocation(s)
        linked = 0
        for item in Item.objects.all():
            display = item.stationer_imprint_location_display or ''
            if not display.strip():
                continue
            sil_list = []
            for part in display.split(';'):
                s = part.strip()
                if s and s in name_to_sil:
                    sil_list.append(name_to_sil[s])
            if sil_list:
                item.stationer_imprint_location.set(sil_list)
                linked += 1

        self.stdout.write(self.style.SUCCESS(f'Linked {linked} items to StationerImprintLocation.'))
