from django.urls import re_path as url
from backends import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

urlpatterns = format_suffix_patterns([
    url(r'^datasets/$',views.TCGADataSetList.as_view(),name='dataset-list'),
    url(r'^datasets/(?P<db_name>[^/]+)/$',views.TCGADataSetDetail.as_view(),name='dataset-detail'),
    url(r'^datasets/(?P<db_name>[^/]+)/(?P<pk>[0-9]+)/$',views.TCGADataSetRecord.as_view(),name='dataset-record'),
    url(r'^disease_abbr/$',views.disease_abbr_list,name='disease-abbr-list'),
    url(r'^gene_info/$',views.GeneList.as_view(),name='gene-list'),
    url(r'^gene_info/(?P<gene_name>[^/]+)/$',views.GeneDetail.as_view(),name='gene-info'),
    url(r'^similar_genes/(?P<gene_name>[^/]+)/$',views.get_similar_gene_info,name='similar-genes'),
    url(r'^differential_genes/(?P<dataset>[^/]+)/$',views.diffrential_expression_by_ANOVA,name='differential-genes'),
    url(r'^differential_genes/(?P<dataset>[^/]+)/(?P<Log2FC>[0-9.]+)&(?P<p_adj>[0-9.]+)/$',views.diffrential_expression_by_ANOVA,name='differential-genes'),
    url(r'^survival_analysis/(?P<gene_name>[^/]+)/(?P<input_str>[^/]+)/$',views.survival_analysis,name='survival-analysis'),
    url(r'^survival_analysis/(?P<gene_name>[^/]+)/(?P<input_str>[^/]+)/(?P<High_cutoff>[0-9.]+)&(?P<Low_cutoff>[0-9.]+)/$',views.survival_analysis,name='survival-analysis'),
    url(r'^gene_plot/strip/(?P<gene_name>[^/]+)/$',views.general_plot_strip,name='gene-plot-strip'),
    url(r'^gene_plot/bar/(?P<gene_name>[^/]+)/$',views.general_plot_bar,name='gene-plot-bar'),
    url(r'^box_plot/(?P<gene_name>[^/]+)/(?P<input_str>[^/]+)/$',views.box_plot,name='gene-plot-box'),
    url(r'^pca/elbow_plot/(?P<input_str>[^/]+)/$',views.pca_elbow,name='pca-elbow-plot'),
    url(r'^pca/elbow_plot/(?P<input_str>[^/]+)/(?P<gene_str>[^/]+)/$',views.pca_elbow,name='pca-elbow-plot'),
    url(r'^pca/visual/(?P<input_str>[^/]+)/$',views.pca_2d,name='pca-2d'),
    url(r'^pca/visual/(?P<input_str>[^/]+)/(?P<gene_str>[^/]+)/$',views.pca_2d,name='pca-elbow-plot'),
    url(r'^global_variable/(?P<variable>[^/]+)/$',views.get_global_variable,name='global-variable'),
])
