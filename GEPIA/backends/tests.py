import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GEPIA.settings")
django.setup()
from backends.models import Gene
from backends.serializers import GeneSerializer
import pandas as pd

file_path = "~/Downloads/GEPIA2023/counts"
gene_info = pd.read_csv(f"{file_path}/gene_info.csv")
data = [{col: row[col] for col in gene_info.columns} for _, row in gene_info.iterrows()]
serializer = GeneSerializer(data=data,many=True)
if serializer.is_valid():
    print("yes")
    serializer.save()

