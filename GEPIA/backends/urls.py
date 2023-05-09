from django.urls import re_path as url
from backends import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = format_suffix_patterns([
    url(r'^datasets/$',views.TCGADataSetList.as_view(),name='dataset-list'),
    url(r'^datasets/(?P<collection_name>[^/]+)/$',views.TCGADataSetDetail.as_view(),name='dataset-detail'),
    url(r'^datasets/(?P<collection_name>[^/]+)/(?P<pk>[0-9]+)/$',views.TCGADataSetRecord.as_view(),name='dataset-record'),
    url(r'^disease_abbr/$',views.disease_abbr_list,name='disease-abbr-list'),
    url(r'^gene_info/(?P<gene_name>[^/]+)/$',views.get_gene_info,name='gene-info'),
])
