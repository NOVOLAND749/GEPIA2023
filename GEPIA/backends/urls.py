from django.urls import re_path as url
from backends import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = format_suffix_patterns([
    url(r'^datasets/$',views.TCGADataSetList.as_view(),name='dataset-list'),
    url(r'^datasets/(?P<collection_name>[^/]+)/$',views.TCGADataSetDetail.as_view(),name='dataset-detail'),
    url(r'^datasets/(?P<collection_name>[^/]+)/(?P<pk>[0-9]+)/$',views.TCGADataSetRecord.as_view(),name='dataset-record'),
    url(r'^disease_abbr/$',views.disease_abbr_list,name='disease-abbr-list'),
    url(r'^gene_info/$',views.GeneList.as_view(),name='gene-list'),
    url(r'^gene_info/(?P<gene_name>[^/]+)/$',views.GeneDetail.as_view(),name='gene-info'),
    url(r'^gene_plot/strip/(?P<gene_name>[^/]+)/$',views.general_plot_strip,name='gene-plot-strip'),
    url(r'^gene_plot/bar/(?P<gene_name>[^/]+)/$',views.general_plot_bar,name='gene-plot-bar'),
    url(r'^global_variable/(?P<variable>[^/]+)/$',views.get_global_variable,name='global-variable'),
])
