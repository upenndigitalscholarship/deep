from django.db import models

# Based on Farmer and Lesser, DEEP Fields (22 02 25).docx.
# The models create a hierarchy of Title, Edition and Issue
# Data at the edition or issue level can be updated without affecting the Title


class Title(models.Model):
    deep_id = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField("Title",max_length=200)
    greg = models.CharField("Greg (Brief)(e.g., 197 for Hamlet)", max_length=200)
    genre = models.CharField("Genre (Annals)", max_length=200, blank=True, null=True)
    date_first_publication = models.CharField("Date of First Publication", max_length=200)
    date_first_publication_display = models.CharField("Date of First Publication", max_length=200, blank=True, null=True)
    # TODO Where is this on the site? I don't see in DB
    date_first_performance = models.CharField("Date of First Performance", max_length=200, blank=True, null=True)
    
    company_first_performance = models.CharField("Company First Performance", max_length=200, blank=True, null=True)
    total_editions = models.CharField("Total Editions", blank=True, null=True, max_length=200)
    stationers_register = models.CharField("Stationers Register", max_length=200, blank=True, null=True)
    # TODO Need this data 
    british_drama = models.IntegerField("British Drama", blank=True, null=True)
    # TODO Is this data in DB?
    genre_wiggins = models.CharField("Genre (Wiggins)", max_length=200, blank=True, null=True)
    #date_first_performance_wiggins = models.CharField("Date of First Performance (Wiggins)", max_length=200)
    #company_first_performance_wiggins = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company_first_performance_wiggins")
    #stationer = models.CharField("Stationer", max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # remove if  not used
        super(Title, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} {self.date_first_publication} ({self.deep_id})"


class Edition(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    authors = models.ManyToManyField('Person')
    greg_middle = models.CharField("Greg (middle)(e.g., 197b for the second edition of Hamlet)", max_length=200)
    book_edition = models.CharField("Book Edition", max_length=200, blank=True, null=True)
    play_edition = models.CharField("Play Edition", max_length=200, blank=True, null=True)
    play_type = models.CharField("Play Type", max_length=200, blank=True, null=True)
    blackletter = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title.title} - {self.greg_middle} - {self.book_edition}"

class Item(models.Model): #Previously known as "DEEP"
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name="variant_edition")
    record_type = models.CharField("Record Type", max_length=200)
    collection = models.CharField("Collection", max_length=200, blank=True, null=True)
    year = models.CharField("Year (of publication)", blank=True, null=True, max_length=200)
    deep_id_display = models.CharField("DEEP #", max_length=200, blank=True, null=True)
    greg_full = models.CharField("Greg #(i.e., Greg full, e.g., 197b(*) and 197b(†) for the two issues of the second edition of Hamlet)", max_length=200)
    stc = models.CharField("STC/Wing #", max_length=200, blank=True, null=True)
    format = models.CharField("Format", max_length=200, blank=True, null=True)
    leaves = models.CharField("Leaves", max_length=200, blank=True, null=True)
    company_attribution = models.CharField("Company Attribution", max_length=200, blank=True, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="variant_company", blank=True, null=True)
    composition_date = models.CharField("Composition Date", max_length=200, blank=True, null=True)
    #old_title = models.CharField(max_length=200) What is this?
    #title_page = models.ForeignKey('TitlePage', on_delete=models.CASCADE)
    date_first_publication = models.CharField("Date of First Publication", max_length=200)

    def __str__(self):
        return f"{self.edition.title.title} - {self.edition.greg_middle}"


class Person(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "people"

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

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
