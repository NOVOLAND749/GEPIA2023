from rest_framework import serializers
from backends.models import DataSet

class DataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('id','client_name','port','db_name','collection_name','descriptions')





