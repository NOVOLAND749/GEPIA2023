import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GEPIA.settings")
django.setup()
from backends.models import DataSet
from backends.serializers import DataSetSerializer
import pandas as pd

file_path = "~/Downloads/GEPIA2023/counts"
dataset_info = pd.read_csv(f"{file_path}/datasets.csv",index_col=0)
data = [{col: row[col] for col in dataset_info.columns} for _, row in dataset_info.iterrows()]
serializer = DataSetSerializer(data=data,many=True)
if serializer.is_valid():
    print("yes")
    serializer.save()

