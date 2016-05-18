# coding=utf-8
from django.contrib import admin
from app.models import Mandado, Oficial, Aviso, Atendimento, Ordem, Modelo, Telefone
import datetime
from django.template import Context, Template, loader


class TelefoneInline(admin.TabularInline):
    model = Telefone
    extra = 1

'''
class EnderecoInline(admin.TabularInline):
    model = Endereco
    extra = 1

'''
class AtendimentoInline(admin.TabularInline):
    model = Atendimento
    extra = 1

def export_aviso(modeladmin, request, queryset):
    f=open('testeefile.csv', 'w')
    for m in queryset:
        strr=u';'+u';'+m.numero_mandado+u';'+m.audiencia+u';'+m.destinatario+u';'+m.rua+u';'+m.numero_rua+u';'+m.bairro+u';'+m.complemento+u';'+m.telefone+u';'+u'\n'
        safe = strr#unicodedata.normalize('NFKD', strr).encode('ascii', 'ignore')
        f.write(safe)
    f.close()

export_aviso.short_description = "marque mandados para mala direta"

def make_av(modeladmin, request, queryset):
    queryset.update(status_cumprimento='AV')
make_av.short_description = "marque os mandados para avisados"

def make_dv(modeladmin, request, queryset):
    queryset.update(status_cumprimento='DV')
make_dv.short_description = "marque os mandados para devolvidos"

def make_URG(modeladmin, request, queryset):
    queryset.update(status_cumprimento='rd')
make_URG.short_description = "marque os mandados para Urgentes"

def make_N(modeladmin, request, queryset):
    queryset.update(status_cumprimento='pu')
make_N.short_description = "marque os mandados para Normal"

def make_con(modeladmin, request, queryset):
    queryset.update(status_cumprimento='gr')
make_con.short_description = "marque os mandados para com Conducao"

def make_cert(modeladmin, request, queryset):
    queryset.update(status_cumprimento='CE')
make_cert.short_description = "marque os mandados para Certificar"

def make_OfX(modeladmin, request, queryset):
    queryset.update(oficial=1)#"2 cristian" "1 drauto" "3 eu mesmo" "4 kleber"
make_OfX.short_description = "transfere para oficial x, provisorio"##provisorio so p nao carregar no ifone...

class MandadoAdmin(admin.ModelAdmin):

    list_display = ['n_mandado', 'data', 'audiencia', 'destinatario', 'rua', 'bairro', 'ordem', 'conducao', 'status_cumprimento']
    ordering = ['n_mandado']
    search_fields = ['numero_mandado', 'destinatario', 'rua']
    list_editable = ['conducao', 'status_cumprimento']#['status_cumprimento', 'conducao']
    list_filter = ['audiencia', 'conducao', 'status_cumprimento', 'data']#
    list_max_show_all = 1000
    fieldsets = (
         (None, {#1
                 'classes': ('wide',),
                 'fields': (('n_mandado', 'destinatario'),
                            ('cep', 'numero_rua'),
                            ('audiencia', 'status_cumprimento', 'conducao', 'ordem'),
                            )# 'aviso') criar em seguida
         }),
         ('Campos de Endereço', {
             'classes': ('wide',),#ou collapse, melhor mostrnado para conferir
             'fields': (('estado', 'cidade', 'rua', 'bairro', 'complemento'),)# ('ddd', 'telefone',))
         }),
         ('Campos Complementares', {
             'classes': ('collapse',),
             'fields': ('processo', 'comarca', 'vara', 'ano_mandado',
                        'data', 'oficial', 'latitude', 'longitude', )#'status_cumprimento', 'owner')
         }),
    )

    class Media:
        js = (
            'admin/js/cep.js',
        )

    actions = [export_aviso, make_av, make_dv, make_N, make_URG, make_con, make_cert, make_OfX]

    inlines = [TelefoneInline,] #EnderecoInline,

    '''
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', # jquery
            'js/myscript.js',       # project static folder
            'app/js/myscript.js',   # app static folder
        )
    '''
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'oficial', None) is None:
            obj.oficial = Oficial.objects.get(usuario=request.user)
        obj.owner = request.user
        obj.numero_mandado = str(obj.n_mandado)
        obj.save()

    def queryset(self, request):
        qs = super(MandadoAdmin, self).queryset(request)

        # Se for superusuario, mostre todos os comentarios
        if request.user.is_superuser:
            return qs

        return qs.filter(oficial__usuario=request.user)


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
#admin.site.register(Endereco)
#admin.site.register(Rua)
#admin.site.register(Bairro)
admin.site.register(Atendimento)
admin.site.register(Mandado, MandadoAdmin)
admin.site.register(Telefone)
admin.site.register(Oficial)
admin.site.register(Ordem)
admin.site.register(Aviso, AvisoAdmin)
admin.site.register(Modelo)
#admin.site.register(Telefone)
#admin.site.register(models.Orden)
#admin.site.register(models.Pessoa)
#admin.site.register(models.Rua)
