from django.db import models

# Create your models here.

class Title(models.Model):
    deep = models.IntegerField("DEEP #", primary_key=True)
    author = models.ManyToManyField('Person')
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    old_title = models.CharField(max_length=200)
    title_page = models.ForeignKey('TitlePage', on_delete=models.CASCADE)
    greg = models.CharField("Greg (Brief)(e.g., 197 for Hamlet)", max_length=200)
    sts = models.CharField("STC/Wing #", max_length=200)
    genre = models.CharField("Genre (Annals)", max_length=200)
    genre_wiggins = models.CharField("Genre (Wiggins)", max_length=200)
    date_first_publication = models.CharField("Date of First Publication", max_length=200)
    date_first_performance = models.CharField("Date of First Performance", max_length=200)
    date_first_performance_wiggins = models.CharField("Date of First Performance (Wiggins)", max_length=200)
    company_first_performance = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company_first_performance")
    company_first_performance_wiggins = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company_first_performance_wiggins")
    total_editions = models.IntegerField("Total Editions")
    british_drama = models.IntegerField("British Drama")
    stationers_register = models.ForeignKey('Stationer', on_delete=models.CASCADE, related_name="stationers_registers")
    format = models.CharField("Format", max_length=200)
    leaves = models.IntegerField("Leaves")
    record_type = models.CharField("Record Type", max_length=200)
    play_type = models.CharField("Play Type", max_length=200)

    def __str__(self):
        return self.title

class Edition(models.Model):
    edition = models.CharField(max_length=200)
    def __str__(self):
        return self.edition

class Issue(models.Model):
    issue = models.CharField(max_length=200)
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