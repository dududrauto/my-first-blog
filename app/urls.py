__author__ = 'Dudu'
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = patterns('',
                       #url(r'^(?P<id>[0-9]+)/$', views.article,),
                       url(r'^mandado/$', views.MandadoList.as_view(), name='lista_mandado'),
                       url(r'^mandado/(?P<pk>[0-9]+)/$', views.MandadoDetail.as_view(), name='detalhes_Mandado'),
                       url(r'^oficial/$', views.OficialList.as_view(), name='lista_Oficial'),
                       url(r'^oficial/(?P<pk>[0-9]+)/$', views.OficialDetail.as_view(), name='detalhes_oficial'),
                       url(r'^telefone/$', views.TelefoneList.as_view(), name='lista_telefone'),
                       url(r'^telefone/(?P<pk>[0-9]+)/$', views.TelefoneDetail.as_view(), name='detalhes_telefone'),
                       #url(r'^cep/$', views.CepList.as_view()),
                       #url(r'^cep/(?P<pk>[0-9]+)/$', views.CepDetail.as_view()),
                       #Expressão regular funcionou para o cep na url url(r'^cep/(?P<pk>[0-9]+-[0-9]+)/$', views.cep_detail),
                       #url(r'^endereco/$', views.EnderecoList.as_view()),
                       #url(r'^endereco/(?P<pk>[0-9]+)/$', views.EnderecoDetail.as_view()),
                       url(r'^diligencia/$', views.DiligenciaList.as_view()),
                       url(r'^diligencia/(?P<pk>[0-9]+)/$', views.DiligenciaDetail.as_view()),
                       url(r'^diligenciasmandado/(?P<pk>[0-9]+)/$', views.DiligenciasMandado.as_view()),
                       url(r'^tipo_diligencia/$', views.TipoDiligenciaList.as_view()),
                       url(r'^tipo_diligencia/(?P<pk>[0-9]+)/$', views.TipoDiligenciaDetail.as_view()),
                       url(r'^estatus_cumprimento/$', views.EstatusCumprimentoList.as_view()),
                       url(r'^estatus_cumprimento/(?P<pk>[0-9]+)/$', views.EstatusCumprimentoDetail.as_view()),
                       url(r'^vara/$', views.VaraList.as_view()),
                       url(r'^vara/(?P<pk>[0-9]+)/$', views.VaraDetail.as_view()),
                       url(r'^comarca/$', views.ComarcaList.as_view()),
                       url(r'^comarca/(?P<pk>[0-9]+)/$', views.ComarcaDetail.as_view()),
                       url(r'^ordem/$', views.OrdemList.as_view()),
                       url(r'^ordem/(?P<pk>[0-9]+)/$', views.OrdemDetail.as_view()),
                       url(r'^foto/$', views.FotoList.as_view()),
                       url(r'^foto/(?P<pk>[0-9]+)/$', views.FotoDetail.as_view()),
                       url(r'^audio/$', views.AudioList.as_view()),
                       url(r'^audio/(?P<pk>[0-9]+)/$', views.AudioDetail.as_view()),
                       url(r'^pdf/$', views.print_users),

                       )
urlpatterns = format_suffix_patterns(urlpatterns)