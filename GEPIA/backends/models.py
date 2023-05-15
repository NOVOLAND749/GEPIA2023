from django.db import models
# from pymongo import MongoClient
# Create your models here.

class DataSet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    db_name = models.CharField(max_length=50,default='TCGA')
    tumor_sample_number = models.IntegerField(default=0)
    normal_sample_number = models.IntegerField(default=0)
    has_normal = models.BooleanField(default=True)
    descriptions = models.TextField(default='',blank=True)

    class Meta:
        ordering = ['created']



class Gene(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    gene_name = models.CharField(max_length=50,default='')
    ENSEMBL = models.CharField(max_length=50,default='')
    description = models.TextField(default='', blank=True)
    Synonyms = models.TextField(default='', blank=True)
    chromosome = models.CharField(max_length=10,default='')
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)

    class Meta:
        ordering = ['created']


