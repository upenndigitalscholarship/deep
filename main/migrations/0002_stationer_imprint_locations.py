from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StationerImprintLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5000, verbose_name='Name')),
                ('supra_category', models.CharField(blank=True, choices=[("A-B (Paul's Churchyard)", "A-B (Paul's Churchyard)"), ('C (Newgate Within)', 'C (Newgate Within)'), ('D (Newgate Without)', 'D (Newgate Without)'), ('E (Smithfield)', 'E (Smithfield)'), ('F (Aldersgate Without)', 'F (Aldersgate Without)'), ('G (Aldersgate Within)', 'G (Aldersgate Within)'), ('H (Cripplegate and Moorgate Within)', 'H (Cripplegate and Moorgate Within)'), ('I (Cripplegate Without)', 'I (Cripplegate Without)'), ('N (Cheapside)', 'N (Cheapside)'), ('O (Royal Exchange)', 'O (Royal Exchange)'), ('P (Leadenhall)', 'P (Leadenhall)'), ('Q (Ludgate)', 'Q (Ludgate)'), ('R-T (Thames St)', 'R-T (Thames St)'), ('V (Holborn)', 'V (Holborn)'), ('W (Fleet St)', 'W (Fleet St)'), ('X (Westminster)', 'X (Westminster)'), ('Cambridge', 'Cambridge'), ('Dublin', 'Dublin'), ('Edinburgh', 'Edinburgh'), ('Hague', 'Hague'), ('Kilkenny', 'Kilkenny'), ('Leiden', 'Leiden'), ('Oxford', 'Oxford'), ('Rochester', 'Rochester'), ('Southwark', 'Southwark')], max_length=500, null=True, verbose_name='Supra-category')),
                ('moeml_link', models.CharField(blank=True, max_length=5000, null=True, verbose_name='MoEML link')),
            ],
            options={
                'verbose_name': 'Stationer: Imprint Location',
                'verbose_name_plural': 'Stationer: Imprint Locations',
            },
        ),
        migrations.RenameField(
            model_name='item',
            old_name='stationer_imprint_location',
            new_name='stationer_imprint_location_display',
        ),
        migrations.AlterField(
            model_name='item',
            name='stationer_imprint_location_display',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Stationer: Imprint Location Display'),
        ),
        migrations.AddField(
            model_name='item',
            name='stationer_imprint_location_filter',
            field=models.ManyToManyField(blank=True, related_name='items', to='main.stationerimprintlocation', verbose_name='Stationer: Imprint Location Filter'),
        ),
    ]
