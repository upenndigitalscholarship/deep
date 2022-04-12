# These are the tables/models as they exist on the old site.
# 
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Auspice(models.Model):
    auspice_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    nid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auspice'


class AuspiceDeep(models.Model):
    auspice_deep_id = models.AutoField(primary_key=True)
    deep_id = models.PositiveIntegerField()
    auspice_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'auspice_deep'


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'author'


class AuthorAttribution(models.Model):
    author_attribution_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'author_attribution'


class AuthorAttributionDeep(models.Model):
    author_attribution_deep_id = models.AutoField(primary_key=True)
    author_attribution_id = models.IntegerField()
    deep_id = models.IntegerField()
    ordering = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'author_attribution_deep'


class AuthorDeep(models.Model):
    author_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    author_id = models.IntegerField()
    ordering = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'author_deep'


class Bookseller(models.Model):
    bookseller_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'bookseller'


class BooksellerDeep(models.Model):
    bookseller_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    bookseller_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bookseller_deep'


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'company'


class CompanyDeep(models.Model):
    company_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    company_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'company_deep'


class DcPdc(models.Model):
    dc_pdc_id = models.AutoField(primary_key=True)
    dc_deep_id = models.IntegerField()
    pdc_deep_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dc_pdc'


class Deep(models.Model):
    deep_id = models.AutoField(primary_key=True)
    nid = models.IntegerField(blank=True, null=True)
    deep_id_display_old = models.CharField(max_length=32, blank=True, null=True)
    deep_id_display = models.DecimalField(max_digits=7, decimal_places=3, blank=True, null=True)
    deep_id_revised = models.CharField(max_length=8, blank=True, null=True)
    deep_id_notused = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=225)
    year = models.PositiveIntegerField(blank=True, null=True)
    year_display = models.CharField(max_length=32)
    composition_date = models.PositiveIntegerField(blank=True, null=True)
    composition_date_display = models.CharField(max_length=255)
    first_publish_date = models.PositiveIntegerField(blank=True, null=True)
    first_publish_date_display = models.CharField(max_length=255)
    record_type_id = models.IntegerField()
    theater_type_id = models.IntegerField()
    greg_full = models.CharField(max_length=128)
    greg_brief = models.CharField(max_length=32)
    greg_middle = models.CharField(max_length=32)
    greg_word = models.CharField(max_length=150)
    not_in_greg = models.IntegerField()
    stc_or_wing = models.CharField(max_length=100)
    stc_or_wing2 = models.CharField(max_length=100, blank=True, null=True)
    collection_brief = models.CharField(max_length=32, blank=True, null=True)
    collection_middle = models.CharField(max_length=32, blank=True, null=True)
    collection_full = models.CharField(max_length=128, blank=True, null=True)
    collection_word = models.CharField(max_length=150, blank=True, null=True)
    play_edition_number = models.IntegerField()
    book_edition_number = models.IntegerField(blank=True, null=True)
    variant_description = models.TextField()
    edition = models.CharField(max_length=32)
    total_editions = models.TextField()
    sheets_delete = models.CharField(max_length=32)
    sheets = models.CharField(max_length=32)
    collation = models.CharField(max_length=100, blank=True, null=True)
    dedication_to = models.TextField()
    commendatory_verses_by = models.TextField()
    to_the_reader = models.CharField(max_length=255)
    argument = models.CharField(max_length=255)
    char_list = models.CharField(max_length=255)
    actor_list = models.CharField(max_length=255)
    illustrationontporfrontis = models.TextField()
    blackletter = models.CharField(max_length=255)
    latin = models.CharField(max_length=255)
    addition_and_correction_attributions = models.CharField(max_length=255)
    other_paratexts = models.TextField(blank=True, null=True)
    previous_sr_entry_date = models.TextField()
    additional_notes = models.TextField()
    transcript_title = models.TextField()
    transcript_author = models.TextField()
    transcript_performance = models.TextField()
    transcript_latin = models.TextField()
    transcript_imprint = models.TextField()
    transcript_explicit = models.TextField()
    transcript_colophon = models.TextField()
    transcript_dedication = models.TextField()
    transcript_commendatory_verses = models.TextField()
    transcript_to_the_reader = models.TextField()
    transcript_printed_license = models.TextField()
    transcript_general_title = models.TextField()
    transcript_woodcut = models.TextField()
    transcript_woodcut_frontispiece = models.TextField()
    transcript_engraved_title = models.TextField()
    transcript_engraved_portrait = models.TextField()
    transcript_engraved_frontispiece = models.TextField()
    biandic = models.IntegerField(db_column='BIandIC', blank=True, null=True)  # Field name made lowercase.
    transcript_character_list = models.TextField(blank=True, null=True)
    transcript_actor_list = models.TextField(blank=True, null=True)
    transcript_argument = models.TextField(blank=True, null=True)
    transcript_modern_spelling = models.TextField()
    transcript_old_spelling = models.TextField()
    display_play_type = models.CharField(max_length=200, blank=True, null=True)
    format = models.CharField(max_length=100, blank=True, null=True)
    display_authors = models.CharField(max_length=200, blank=True, null=True)
    display_genre = models.CharField(max_length=200, blank=True, null=True)
    display_booksellers = models.CharField(max_length=200, blank=True, null=True)
    display_printers = models.CharField(max_length=200, blank=True, null=True)
    display_publishers = models.CharField(max_length=200, blank=True, null=True)
    display_companies = models.CharField(max_length=200, blank=True, null=True)
    display_auspices = models.CharField(max_length=200, blank=True, null=True)
    title_alternative_keywords = models.TextField(blank=True, null=True)
    errata = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deep'


class Export(models.Model):
    token = models.CharField(primary_key=True, max_length=40)
    email = models.CharField(max_length=64)
    format = models.CharField(max_length=8, blank=True, null=True)
    tstamp = models.PositiveIntegerField()
    download_date = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'export'


class Genreharbage(models.Model):
    genreharbage_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'genreharbage'


class GenreharbageDeep(models.Model):
    genreharbage_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    genreharbage_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'genreharbage_deep'


class Genreplaybookattribution(models.Model):
    genreplaybookattribution_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'genreplaybookattribution'


class GenreplaybookattributionDeep(models.Model):
    genreplaybookattribution_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    genreplaybookattribution_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'genreplaybookattribution_deep'


class Imprintlocation(models.Model):
    imprintlocation_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)
    display_ordering = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imprintlocation'


class ImprintlocationDeep(models.Model):
    imprintlocation_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    imprintlocation_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'imprintlocation_deep'


class Playtype(models.Model):
    playtype_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'playtype'


class PlaytypeDeep(models.Model):
    playtype_deep_id = models.AutoField(primary_key=True)
    deep_id = models.IntegerField()
    playtype_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'playtype_deep'


class Printer(models.Model):
    printer_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'printer'


class PrinterDeep(models.Model):
    printer_deep_id = models.AutoField(primary_key=True)
    printer_id = models.IntegerField()
    deep_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'printer_deep'


class Pt(models.Model):
    deep_id = models.IntegerField(primary_key=True)
    playtype_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pt'


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'publisher'


class PublisherDeep(models.Model):
    publisher_deep_id = models.AutoField(primary_key=True)
    publisher_id = models.IntegerField()
    deep_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'publisher_deep'


class RecordType(models.Model):
    record_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    abbreviation = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'record_type'


class Srstationer(models.Model):
    srstationer_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'srstationer'


class SrstationerDeep(models.Model):
    srstationer_deep_id = models.AutoField(primary_key=True)
    srstationer_id = models.IntegerField()
    deep_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'srstationer_deep'


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'status'


class StatusDeep(models.Model):
    status_deep_id = models.AutoField(primary_key=True)
    status_id = models.IntegerField()
    deep_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'status_deep'


class Theater(models.Model):
    theater_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'theater'


class TheaterDeep(models.Model):
    theater_deep_id = models.AutoField(primary_key=True)
    theater_id = models.IntegerField()
    deep_id = models.IntegerField()
    ordering = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'theater_deep'


class TheaterType(models.Model):
    theater_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'theater_type'


class Variant(models.Model):
    variant_id = models.AutoField(primary_key=True)
    edition_id = models.IntegerField()
    deep_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'variant'


class VariantNewish(models.Model):
    variant_id = models.AutoField(primary_key=True)
    primary_deep_id = models.IntegerField()
    variant_deep_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'variant_newish'
