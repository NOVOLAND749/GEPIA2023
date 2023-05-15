from rest_framework import serializers
from backends.models import DataSet,Gene

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('id','db_name','tumor_sample_number','normal_sample_number','has_normal','descriptions')


class GeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ('id','gene_name','ENSEMBL','description','Synonyms','chromosome','start','end')


