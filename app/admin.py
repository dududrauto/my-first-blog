# coding=utf-8
from django.contrib import admin
from app.models import *#Mandado, Oficial, Endereco, CEP, Ordem, Modelo_Documento, Telefone
import datetime
from django.template import Context, Template, loader
from app.printing import MyPrint
from io import BytesIO
from django.http import HttpResponse
from django import forms

class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1


#######################
def make_add_rel(modeladmin, request, queryset):
    x = queryset[0].relatorio
    b=open(x._get_url(), 'r')
    relatorio = b.read().splitlines()
    b.close()
    x.close()
    for mm in relatorio[1:]:
        mm = str(mm)
        mm=mm.split(';')
        mandado = Mandado()
        data_str = mm[0].replace("b'", "")
        day, month, year = data_str.split('/')
        mandado.data = datetime.date(int(year)+2000, int(month), int(day))
        mandado.numero_mandado = int(mm[1])
        mandado.destinatario = mm[2].upper()
        mandado.rua = 'RUA '+mm[3].upper()
        mandado.numero = mm[4]
        mandado.cidade = 'Alvorada'
        try:
            day, month, year = mm[5].split('/')
            mandado.audiencia = datetime.date(int(year)+2000, int(month), int(day))
        except:
            pass
        mandado.ordem = Ordem.objects.get(id=int(mm[6]))
        mandado.owner = request.user
        mandado.oficial = queryset[0].oficial
        mandado.codigo_mandado = '003/'+str(mandado.data.year)+'/'+str(mandado.numero_mandado)
        mandado.geo_verificado = False
        try:
            mandado.save()
        except:
            pass
        #print(mandado)
        #print(mandado.latitude)

make_add_rel.short_description = "incluir relatorio"


#######################
def export_aviso(modeladmin, request, queryset):
    f=open(str(request.user)+"_"+'relatorio.csv', 'w')
    for m in queryset:
        strr=u';'+u';'+str(m.numero_mandado)+u';'+str(m.audiencia)+u';'+str(m.destinatario)+u';'+str(m.rua)+u';'+str(m.numero_rua)+u';'+m.bairro+u';'+m.complemento+u';'+u'\n'
        safe = strr#unicodedata.normalize('NFKD', strr).encode('ascii', 'ignore')
        f.write(safe)
    f.close()

export_aviso.short_description = "marque mandados para mala direta"
'''
def make_av(modeladmin, request, queryset):
    queryset.update(status_cumprimento=1)
make_av.short_description = "marque os mandados para avisados"
'''

def make_av(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Avisos.pdf"'#se comentar essa linha o arquivo abre no navegador

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_avisos(request, queryset)

    response.write(pdf)
    return response

make_av.short_description = "fazer avisos para os mandados"

def make_certidao(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Avisos.pdf"'#se comentar essa linha o arquivo abre no navegador

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_certidao(request, queryset)

    response.write(pdf)
    return response

make_certidao.short_description = "fazer certidoes para os mandados"



def make_pendente(modeladmin, request, queryset):
    queryset.update(status_cumprimento=2)
make_pendente.short_description = "marque os mandados para PENDENTES"

def make_nao_cumprido(modeladmin, request, queryset):
    queryset.update(status_cumprimento=6)
make_nao_cumprido.short_description = "marque os mandados para NÃO CUMPRIDO"

def make_vermelho(modeladmin, request, queryset):
    queryset.update(cor_urgencia=1)
make_vermelho.short_description = "marque os mandados para VERMELHO"

def make_amarelo(modeladmin, request, queryset):
    queryset.update(cor_urgencia=2)
make_amarelo.short_description = "marque os mandados para AMARELO"

def make_verde(modeladmin, request, queryset):
    queryset.update(cor_urgencia=3)
make_verde.short_description = "marque os mandados para VERDE"

'''
def make_con(modeladmin, request, queryset):
    queryset.update(status_cumprimento=5)
make_con.short_description = "marque os mandados para com Conducao"

def make_cert(modeladmin, request, queryset):
    queryset.update(status_cumprimento=6)
make_cert.short_description = "marque os mandados para Certificar"

def make_OfX(modeladmin, request, queryset):
    queryset.update(oficial=1)#"2 cristian" "1 drauto" "3 eu mesmo" "4 kleber"
make_OfX.short_description = "transfere para oficial x, provisorio"##provisorio so p nao carregar no ifone...
'''




class MandadoAdmin(admin.ModelAdmin):
    list_display = ['numero_mandado', 'ajustado_mapa', 'audiencia', 'destinatario', 'cidade', 'rua', 'numero', 'ordem',
                    'conducao', 'status_cumprimento']
    ordering = ['numero_mandado']
    search_fields = ['numero_mandado', 'destinatario', 'rua']
    list_editable = []
    list_filter = ['status_cumprimento', 'audiencia', 'conducao', 'ordem']
    list_max_show_all = 1000
    readonly_fields = ('ajustado_mapa', 'verificado_em_loco', )
    fieldsets = ((None, {#1
                 'classes': ('wide',),
                 'fields': (('numero_mandado', 'destinatario', ),
                            ('cep', 'cidade', 'bairro',),
                            ('rua', 'numero'), 'complemento',
                            ('audiencia', 'status_cumprimento', 'conducao', 'ordem'),
                            ('position', ),
                            ('ajustado_mapa',), ('verificado_em_loco',),
                            )}),
         ('Campos Complementares', {
             'classes': ('collapse',),
             'fields': (('processo', 'comarca', 'vara'),('ano_mandado', 'codigo_mandado'), ('estado', 'pais'),
                        ('cor_urgencia', 'rota'),
                        ('latitude', 'longitude'), ('ajustado_mapa', 'verificado_em_loco', 'endereco_ERRO', 'endereco_nao_mora'),
                        ('data', 'oficial', 'owner'))
         }),
    )

    class Media:
        js = (
            'admin/js/cep.js',
        )

    actions = [make_av, make_pendente, make_nao_cumprido, make_amarelo, make_verde, make_vermelho, export_aviso]#

    inlines = [TelefoneInline,]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'oficial', None) is None:
            obj.oficial = Oficial.objects.get(usuario=request.user)
        obj.owner = request.user
        obj.codigo_mandado = str(obj.oficial.comarca.cod_comarca)+'/'+str(obj.ano_mandado)+'/'+str(obj.numero_mandado)
        rua = obj.rua.split(' - ')[0]
        obj.rua = rua
        obj.save()


    def get_queryset(self, request):
        qs = super(MandadoAdmin, self).get_queryset(request)
        # Se for superusuario, mostre todos os comentarios
        if request.user.is_superuser:
            return qs

        return qs.filter(oficial__usuario=request.user)


class DiligenciaAdmin(admin.ModelAdmin):
    list_display = ['mandado', '__str__', 'data_diligencia', 'hora_diligencia', 'not_editar_documento', ]
    ordering = ['mandado__numero_mandado']
    search_fields = ['mandado__numero_mandado']
    list_editable = []
    list_filter = ['editar_documento', 'imprimir', 'tipo_diligencia',]
    list_max_show_all = 1000
    fieldsets = (
         (None, {#1
                 'classes': ('wide',),
                 'fields': ('mandado', 'tipo_diligencia', 'documento',
                            )}),
         ('Campos Complementares', {
             'classes': ('collapse',),
             'fields': ('editar_documento', 'data_diligencia', 'hora_diligencia', 'latitude', 'longitude',
                        'data_agendamento', 'hora_agendamento'),
         }),
    )
    readonly_fields = ('mandado', 'tipo_diligencia', 'data_diligencia', 'hora_diligencia', 'latitude', 'longitude', 'data_agendamento',
                       'hora_agendamento', 'editar_documento')

    class Media:
        pass

    actions = [make_certidao, ]

    def save_model(self, request, obj, form, change):
        obj.editar_documento = False
        obj.save()

    def get_queryset(self, request):
        qs = super(DiligenciaAdmin, self).get_queryset(request)
        # Se for superusuario, mostre todos os comentarios
        if request.user.is_superuser:
            return qs

        return qs.filter(mandado__oficial__usuario=request.user, tipo_diligencia__diligencia_cumprida=True)



class CEPAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'admin/js/cep.js',
        )


class AtendimentoAdmin(admin.ModelAdmin):
    fields = ['data', 'inicio', 'fim']#'oficial',
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'oficial', None) is None:
            oj = Oficial.objects.get(usuario=request.user)
            obj.oficial = oj
        obj.save()

    def get_queryset(self, request):
        from django.utils import datetime_safe
        qs = super(AtendimentoAdmin, self).get_queryset(request)
        # Se for superusuario, mostre todos os comentarios
        if request.user.is_superuser:
            return qs
        oj = Oficial.objects.get(usuario=request.user)

        return qs.filter(oficial=oj, data__gt=datetime_safe.date.today())


class RelatorioAdmin(admin.ModelAdmin):
    actions = [make_add_rel, ]#


'''
class AvisoAdmin(admin.ModelAdmin):
#    inlines = [AtendimentoInline]


    def queryset(self, request):
        qs = super(AvisoAdmin, self).queryset(request)
        # Se for superusuario, mostre todos os comentarios
        if not request.user.is_superuser:
            qs = qs.filter(oficial__usuario=request.user)
        for av in qs:
            html = ''
            for mand in av.mandado_set.all():
                template = loader.get_template('modelo_aviso.html')
                context = Context({"mandado": mand,
                                   #"agendamento_set": av.agendamento_set.all(),
                                   #"endereco": mand.endereco_set.all()
                                   })
                html += template.render(context)
            if html:
                av.aviso = html.replace("\n", "")
                av.save()
        return qs
'''
'''
  fields = (
            'id',
            'comarca',          ok 3
            'vara',             ok 3
            'processo',         ok 3
            'conducao',         ok 1
            'ano_mandado',      ok 3
            'numero_mandado',   ok 1
            'data',             ok 3
            'oficial',          ok 3
            'ordem',            ok 1
            'audiencia',        ok 1
            'destinatario',     ok 1
            'ddd',              ok 1
            'telefone',         ok 1
            'cep',              ok 1
            'cidade',           ok 2
            'bairro',           ok 2
            'rua',              ok 2
            'numero_rua',       ok 1
            'complemento',      ok 2
            'latitude',         ok 3
            'longitude',        ok 3
            'status_cumprimento',ok 3
            )
'''



# Register your models here.
admin.site.register(Mandado, MandadoAdmin)
#admin.site.register(Endereco)
#admin.site.register(CEP, CEPAdmin)
admin.site.register(Estatus_Cumprimento)
admin.site.register(Oficial)
admin.site.register(Ordem)
admin.site.register(Telefone)
admin.site.register(Modelo_Documento)
admin.site.register(Diligencia, DiligenciaAdmin)
admin.site.register(Tipo_Diligencia)
admin.site.register(Comarca)
admin.site.register(Vara)
admin.site.register(Atendimento, AtendimentoAdmin)
#admin.site.register(Foto)
#admin.site.register(Audio)
admin.site.register(Relatorio, RelatorioAdmin)

