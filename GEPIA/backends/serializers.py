from rest_framework import serializers
from backends.models import DataSet,Gene

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('id','client_name','port','db_name','collection_name','descriptions')


class GeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ('id','gene_name','ENSEMBL','description','Synonyms','chromosome','start','end')


