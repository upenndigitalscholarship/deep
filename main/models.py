from django.db import models

# Based on Farmer and Lesser, DEEP Fields (22 02 25).docx.
# The models create a hierarchy of Title, Edition and Issue
# Data at the edition or issue level can be updated without affecting the Title

class Title(models.Model):
    deep_id = models.IntegerField(primary_key=True)
    year = models.PositiveIntegerField("Year", blank=True, null=True)
    title = models.CharField("Title",max_length=200)
    greg = models.CharField("Greg (Brief)(e.g., 197 for Hamlet)", max_length=200)
    genre = models.CharField("Genre (Annals)", max_length=200)
    date_first_publication = models.CharField("Date of First Publication", max_length=200)
    date_first_performance = models.CharField("Date of First Performance", max_length=200)
    company_first_performance = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company_first_performance")
    total_editions = models.IntegerField("Total Editions", blank=True, null=True)
    british_drama = models.IntegerField("British Drama", blank=True, null=True)
    genre_wiggins = models.CharField("Genre (Wiggins)", max_length=200, blank=True, null=True)
    date_first_performance_wiggins = models.CharField("Date of First Performance (Wiggins)", max_length=200)
    company_first_performance_wiggins = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company_first_performance_wiggins")
    stationers_register = models.ForeignKey('Stationer', on_delete=models.CASCADE, related_name="stationers_registers")

    editions = models.ManyToManyField('Edition', blank=True, null=True)

    def __str__(self):
        return self.title


class Edition(models.Model):
    author = models.ManyToManyField('Person')
    greg = models.CharField("Greg (middle)(e.g., 197b for the second edition of Hamlet)", max_length=200)
    book_edition = models.CharField("Book Edition", max_length=200)
    play_edition = models.CharField("Play Edition", max_length=200)
    play_type = models.CharField("Play Type", max_length=200)
    blackletter = models.CharField(max_length=255)
    variants = models.ManyToManyField('Variant', blank=True, null=True)

    def __str__(self):
        return self.edition

class Variant(models.Model):
    year = models.PositiveIntegerField("Year (of publication)", blank=True, null=True)
    deep_id_display = models.DecimalField("DEEP #", max_digits=7, decimal_places=3, blank=True, null=True)
    greg = models.CharField("Greg #(i.e., Greg full, e.g., 197b(*) and 197b(†) for the two issues of the second edition of Hamlet)", max_length=200)
    stc = models.CharField("STC/Wing #", max_length=200)
    format = models.CharField("Format", max_length=200)
    leaves = models.IntegerField("Leaves")
    record_type = models.CharField("Record Type", max_length=200)
    company_attribution = models.CharField("Company Attribution", max_length=200)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company")
    
    old_title = models.CharField(max_length=200)
    title_page = models.ForeignKey('TitlePage', on_delete=models.CASCADE)
    date_first_publication = models.CharField("Date of First Publication", max_length=200)
    def __str__(self):
        return self.issue

class Person(models.Model):
    person = models.CharField(max_length=200)
    def __str__(self):
        return self.person

class Company(models.Model):
    company = models.CharField(max_length=200)
    def __str__(self):
        return self.company

class Theater(models.Model):
    theater = models.CharField(max_length=200)
    def __str__(self):
        return self.theater

# Entries in Stationers’ Registers
class Stationer(models.Model): 
    register = models.CharField(max_length=200)
    colophon = models.CharField(max_length=200)
    printer = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    bookseller = models.CharField(max_length=200)
    imprint_locaiton = models.CharField(max_length=200)

    def __str__(self):
        return self.register

class TitlePage(models.Model):
    title_page = models.CharField(max_length=200)
    def __str__(self):
        return self.title_page

class ParaText(models.Model):
    para_text = models.CharField(max_length=200)
    def __str__(self):
        return self.para_text

