__author__ = 'Dudu'
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = patterns('',
                       #url(r'^(?P<id>[0-9]+)/$', views.article,),
                       url(r'^$', views.MandadoList.as_view(), name='lista_mandado'),
                       url(r'^(?P<pk>[0-9]+)/$', views.MandadoDetail.as_view(), name='detalhes_Mandado'),
                       url(r'^oficiais/$', views.OficialList.as_view(), name='lista_Oficial'),
                       url(r'^oficiais/(?P<pk>[0-9]+)/$', views.OficialDetail.as_view(), name='detalhes_oficial'),
                       url(r'^telefone/$', views.TelefoneList.as_view(), name='lista_telefone'),
                       url(r'^telefone/(?P<pk>[0-9]+)/$', views.TelefoneDetail.as_view(), name='detalhes_telefone'),
                       )
urlpatterns = format_suffix_patterns(urlpatterns)