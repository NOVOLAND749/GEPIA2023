from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backends.models import DataSet
from backends.serializers import DataSetSerializer
from django.http import Http404
from backends.database import DatabaseAPI
from rest_framework.decorators import api_view
from backends.plotting import GenePlot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from django.http import FileResponse

# Create your views here.
class TCGADataSetList(APIView):
    def get(self,request,format=None):
        datasets = DataSet.objects.filter(db_name='tcga')
        serializer = DataSetSerializer(datasets,many=True)
        return Response(serializer.data)

    # def post(self,request,format=None):
    #     serializer = DataSetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data,status=status.HTTP_201_CREATED)
    #
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TCGADataSetDetail(APIView):
    def get_object(self,collection_name):
        try:
            return DataSet.objects.get(db_name='tcga',collection_name=collection_name)
        except DataSet.DoesNotExist:
            raise Http404

    def get(self,request,collection_name,format=None):
        dataset = self.get_object(collection_name)
        serializer = DataSetSerializer(dataset)
        return Response(serializer.data)

class TCGADataSetRecord(APIView):
    def get_object(self,collection_name):
        try:
            return DataSet.objects.get(db_name='tcga',collection_name=collection_name)
        except DataSet.DoesNotExist:
            raise Http404


    def get(self,request,collection_name,pk,format=None):
        dataset = self.get_object(collection_name)
        api = DatabaseAPI(db_name='tcga',collection_name=dataset.collection_name)
        res = api.read_table_obs_by_var(int(pk))
        return Response({"obs_values":res})


@api_view(['GET'])
def disease_abbr_list(request,format = None):
    disease_abbr = {"Adrenocortical carcinoma": "ACC",
                    "Bladder Urothelial Carcinoma": "BLCA",
                    "Breast invasive carcinoma": "BRCA",
                    "Cervical squamous cell carcinoma and endocervical adenocarcinoma": "CESC",
                    "Cholangiocarcinoma": "CHOL",
                    "Colon adenocarcinoma": "COAD",
                    "Lymphoid Neoplasm Diffuse Large B-cell Lymphoma": "DLBC",
                    "Esophageal carcinoma": "ESCA",
                    "Glioblastoma multiforme": "GBM",
                    "Head and Neck squamous cell carcinoma": "HNSC",
                    "Kidney Chromophobe": "KICH",
                    "Kidney renal clear cell carcinoma": "KIRC",
                    "Kidney renal papillary cell carcinoma": "KIRP",
                    "Acute Myeloid Leukemia": "LAML",
                    "Brain Lower Grade Glioma": "LGG",
                    "Liver hepatocellular carcinoma": "LIHC",
                    "Lung adenocarcinoma": "LUAD",
                    "Lung squamous cell carcinoma": "LUSC",
                    "Mesothelioma": "MESO",
                    "Ovarian serous cystadenocarcinoma": "OV",
                    "Pancreatic adenocarcinoma": "PAAD",
                    "Pheochromocytoma and Paraganglioma": "PCPG",
                    "Prostate adenocarcinoma": "PRAD",
                    "Rectum adenocarcinoma": "READ",
                    "Sarcoma": "SARC",
                    "Skin Cutaneous Melanoma": "SKCM",
                    "Stomach adenocarcinoma": "STAD",
                    "Testicular Germ Cell Tumors": "TGCT",
                    "Thyroid carcinoma": "THCA",
                    "Thymoma": "THYM",
                    "Uterine Corpus Endometrial Carcinoma": "UCEC",
                    "Uterine Carcinosarcoma": "UCS",
                    "Uveal Melanoma": "UVM"
                    }
    if request.method == "GET":
        return Response(disease_abbr)

@api_view(['GET'])
def get_gene_info(request,gene_name,format = None):
    api = DatabaseAPI(db_name='tcga',collection_name='gene_info')
    keys = ['description', 'Synonyms', 'chromesome','ENSEMBL']
    res = api.query_metadata(keys,metadata_name='gene_info')
    if request.method == "GET":
        try:
            data = {key.capitalize(): res[key][gene_name] for key in keys}
        except KeyError:
            # Handle KeyError
            raise Http404
        return Response(data)

@api_view(['GET'])



@api_view(['GET'])
def general_plot_strip(request,gene_name,format = 'image/png'):
    pl = GenePlot(gene_name)
    fig = pl.stripplot()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return FileResponse(buf, content_type='image/png')







