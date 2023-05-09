from django.db import models
# from pymongo import MongoClient
# Create your models here.

class DataSet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    client_name = models.CharField(max_length=50,default='localhost')
    port = models.IntegerField(default=27017)
    db_name = models.CharField(max_length=50,default='TCGA')
    collection_name = models.CharField(max_length=50,default='',blank=True)
    descriptions = models.TextField(default='',blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.collection_name


