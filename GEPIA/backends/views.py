import gc

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backends.models import DataSet,Gene
from backends.serializers import DataSetSerializer,GeneSerializer
from django.http import Http404
from backends.database import DatabaseAPI
from rest_framework.decorators import api_view
from backends.plotting import GenePlot,boxplot,survive_curve,ElbowPlot,PCA2DPlot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from django.http import FileResponse,HttpResponse
# from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import MultipleObjectsReturned,ObjectDoesNotExist,ImproperlyConfigured
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Create your views here.
class TCGADataSetList(APIView):
    def get(self,request,format=None):
        datasets = DataSet.objects.all()
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
    def get_object(self,db_name):
        try:
            return DataSet.objects.get(db_name=db_name)
        except DataSet.DoesNotExist:
            raise Http404

    def get(self,request,db_name,format=None):
        dataset = self.get_object(db_name)
        serializer = DataSetSerializer(dataset)
        return Response(serializer.data)

class TCGADataSetRecord(APIView):
    def get_object(self,db_name):
        try:
            return DataSet.objects.get(db_name=db_name)
        except DataSet.DoesNotExist:
            raise Http404


    def get(self,request,db_name,pk,format=None):
        dataset = self.get_object(db_name)
        api = DatabaseAPI(db_name='tcga',collection_name=dataset.collection_name)
        res = api.read_table_obs_by_var(int(pk))
        return Response({"obs_values":res})


class GeneList(APIView):
    ## add ?page=1 to get the first page
    def get(self,request,format = None):
        gene_list = Gene.objects.all()
        # paginator = PageNumberPagination()
        # paginated_datasets = paginator.paginate_queryset(gene_list, request)
        serializer = GeneSerializer(gene_list, many=True)
        # filter_data = [{"gene_name":item['gene_name'],"ENSEMBL":item['ENSEMBL']} for item in serializer.data]
        filter_data = [item['gene_name'] for item in serializer.data]
        return Response(filter_data)
    #

class GeneDetail(APIView):
    def get_object(self,gene_name):
        status = 0
        try:
            return Gene.objects.get(gene_name=gene_name),status
        except Gene.DoesNotExist:
            raise Http404
        except MultipleObjectsReturned:
            status = 1
            print("Multiple objects returned for gene_name: %s" % gene_name)
            return Gene.objects.filter(gene_name=gene_name).first(),status


    def get(self,request,gene_name,format = None):
        gene,status = self.get_object(gene_name)
        # if status:
        #    serializer = GeneSerializer(gene,many=True)
        # else:
        serializer = GeneSerializer(gene)
        return Response(serializer.data)


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
    abbr_list = [{"full": key, "abbr": value} for key, value in disease_abbr.items()]
    if request.method == "GET":
        return Response(abbr_list)

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
def get_similar_gene_info(request,gene_name,format = None):
    api = DatabaseAPI(db_name='tcga',collection_name='gene_info')
    genes = api.read_metadata(gene_name,metadata_name="most 100 similar genes")
    values = api.read_metadata(gene_name,metadata_name="most 100 similar gene values")
    if request.method == "GET":
        my_list = [{"gene_name":gene,"value":value} for gene,value in zip(genes,values)]
        return Response(my_list)

@api_view(['GET'])
def diffrential_expression_by_ANOVA(request,dataset,Log2FC=1.0,p_adj=0.01):
    api = DatabaseAPI(db_name = "differential_genes",collection_name = "test")
    res = api.get_metadata(metadata_name=f'TCGA-{dataset}-differential-genes')
    if request.method == "GET":
        my_list = [{"gene_name":gene,**value}for gene,value in res.items() \
                   if np.abs(value['log2fc'])>=float(Log2FC) and value['p']<=float(p_adj)]
        return Response(my_list)

@api_view(['GET'])
def general_plot_strip(request,gene_name,format = 'image/png'):
    pl = GenePlot(gene_name)
    if request.method == "GET":
        fig = pl.stripplot()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close('all')
        buf.seek(0)
        gc.collect()
        return FileResponse(buf, content_type='image/png')
        # with io.BytesIO() as buf:
        #     fig.savefig(buf, format='png')
        #     plt.clf()  # clear the current figure...
        #     plt.close('all')
        #     buf.seek(0)
        #     gc.collect()
        #     response = HttpResponse(content=buf.getvalue(), content_type='image/png')
        #     return response

@api_view(['GET'])
def general_plot_bar(request,gene_name,format = 'image/png'):
    pl = GenePlot(gene_name)
    if request.method == "GET":
        fig = pl.bar_plot()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close('all')
        buf.seek(0)
        gc.collect()
        return FileResponse(buf, content_type='image/png')
        # with io.BytesIO() as buf:
        #     fig.savefig(buf, format='png')
        #     plt.clf()  # clear the current figure...
        #     plt.close('all')
        #     buf.seek(0)
        #     gc.collect()
        #     response = HttpResponse(content=buf.getvalue(), content_type='image/png')
        #     return response



@api_view(['GET'])
def box_plot(request,gene_name,input_str,format = 'image/png'):
    if request.method == 'GET':
        datasets = input_str.split('&')
        if len(datasets) > 5:
            msg = "Too many datasets, please select less than 5 datasets"
            return Response(msg)
        else:
            api = DatabaseAPI(db_name='dataset',collection_name='test')
            count = []
            type = []
            disease = []
            box_pairs = []
            for dataset in datasets:
                t_val = api.read_metadata(key=gene_name,metadata_name=f'TCGA-{dataset}-tumor')
                n_val = api.read_metadata(key=gene_name,metadata_name=f'TCGA-{dataset}-normal')
                count += t_val
                count += n_val
                type += ['tumor']*len(t_val)
                type += ['normal']*len(n_val)
                disease += [dataset]*(len(t_val)+len(n_val))
                box_pairs.append(((dataset,'tumor'),(dataset,'normal')))
            df = pd.DataFrame({'count':count,'type':type,'disease':disease})
            fig = boxplot(df=df,x='disease',y='count',hue='type',box_pairs=box_pairs)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close('all')
            buf.seek(0)
            return FileResponse(buf, content_type='image/png')

@api_view(['GET'])
def survival_analysis(request,gene_name,input_str,High_cutoff = None,Low_cutoff = None,format = 'image/png'):
    if request.method == 'GET':
        datasets = input_str.split('&')
        if len(datasets) > 5:
            msg = "Too many datasets, please select less than 5 datasets"
            raise ImproperlyConfigured(msg)
        else:
            api = DatabaseAPI(db_name='tcga', collection_name='test')
            sample_info = pd.DataFrame(api.get_metadata(metadata_name='sample_info'))
            api2 = DatabaseAPI(db_name='survive_analysis',collection_name='test')
            if len(datasets) == 1:
                df = pd.DataFrame(api2.get_metadata(metadata_name=f'TCGA-{datasets[0]}-survival'))
            else:
                dfs = []
                for dataset in datasets:
                    dfs.append(pd.DataFrame(api2.get_metadata(metadata_name=f'TCGA-{dataset}-survival')))
                df = pd.concat(dfs)
            df = df[df.index.isin(sample_info.index)]
            obs_id = sample_info.loc[df.index,'obs_id']
            gene_exp = np.array(api.read_table_gene_by_var(gene_id='ERBB2'))[np.array(obs_id)]
            if High_cutoff is None:
                arr = gene_exp>np.median(gene_exp)
                df['factor'] = ['High' if a else 'Low' for a in arr]

            elif High_cutoff and Low_cutoff:
                df['gene_expression'] = gene_exp
                high = np.percentile(gene_exp,float(High_cutoff))
                low = np.percentile(gene_exp,float(Low_cutoff))
                def func(x):
                    if x > high:
                        return 'High'
                    elif x < low:
                        return 'Low'
                    else:
                        return 'Middle'
                df['factor'] = df['gene_expression'].apply(func)
                print(sum(df['factor'] == 'High'))
                df = df[(df['factor'] == 'High') | (df['factor'] == 'Low')]


            fig = survive_curve(df,gene_name=gene_name)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            plt.close('all')
            buf.seek(0)
            return FileResponse(buf, content_type='image/png')


def pca(input_str,gene_str=None):
    datasets = input_str.split('&')
    # if len(datasets) > 5:
    #     msg = "Too many datasets, please select less than 5 datasets"
    #     raise ImproperlyConfigured(msg)
    api = DatabaseAPI(db_name='tcga', collection_name='test')
    api2 = DatabaseAPI(db_name='dataset', collection_name='test')
    if gene_str is None:
        genes = pd.DataFrame(api.get_metadata(metadata_name='gene_info')).index
        genes = genes.sort_values()
        gene_list = genes[3:103].to_list()
    else:
        gene_list = gene_str.split('&')
        if len(gene_list) < 5:
            raise ImproperlyConfigured("Please Select Enough genes of interest")
    arrs = []
    Type = []
    for dataset in datasets:
        if f"TCGA-{dataset}" not in api2.db.list_collection_names():
            raise ObjectDoesNotExist
        else:
            arr = pd.DataFrame(api2.query_metadata(metadata_name=f'TCGA-{dataset}',keys = gene_list)).values
            arrs.append(arr)
            Type += [dataset] * arr.shape[0]
    arr = np.concatenate(arrs,axis=0)


    arr_scaled = StandardScaler().fit_transform(arr)
    n_component = min(50,len(gene_list))
    pca = PCA(n_components=n_component)
    pca_features = pca.fit_transform(arr_scaled)
    return pca_features,pca,Type

@api_view(['GET'])
def pca_elbow(request,input_str,gene_str=None,format = 'image/png'):
    if request.method == 'GET':
        _pca_features,pca_obj,_type = pca(input_str,gene_str)
        fig = ElbowPlot(pca_obj)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close('all')
        buf.seek(0)
        return FileResponse(buf, content_type='image/png')

@api_view(['GET'])
def pca_2d(request,input_str,gene_str=None,format = 'image/png'):
    if request.method == 'GET':
        pca_features,pca_obj,type = pca(input_str,gene_str)
        df = pd.DataFrame(pca_features[:,:2],columns=['PC1','PC2'])
        df['Group'] = type
        fig = PCA2DPlot(df)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close('all')
        buf.seek(0)
        return FileResponse(buf, content_type='image/png')











@api_view(['GET'])
def get_global_variable(request,variable, format = None):
    dict = {"PAGE_SIZE": 100}
    if request.method == "GET":
        try:
            return Response(dict[variable])
        except KeyError:
            raise Http404







