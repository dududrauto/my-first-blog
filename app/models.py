# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import django
import datetime
import django.utils.timezone
from geoposition.fields import GeopositionField
import geocoder

# Create your models here.


class Mandado(models.Model):
    class Meta:
        verbose_name = 'Mandado'
        verbose_name_plural = 'Mandados'

    #                           DADOS DA ORIGEM
    comarca = models.ForeignKey('Comarca', null=True, blank=True)
    vara = models.ForeignKey('Vara', blank=True, null=True)
    processo = models.CharField(blank=True, null=True, max_length=35)
    #                           DADOS DE DESTINATARIO
    destinatario = models.CharField(max_length=100)
    cep = models.CharField(max_length=9, null=True, blank=True,
                           help_text='Alternativamente, preencha "Campos de Endereço".',)
    rua = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(verbose_name='Número da Casa', max_length=6)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50, default="Rio Grande do Sul")
    pais = models.CharField(max_length=50, default="Brasil")
    ajustado_mapa = models.BooleanField(default=False)
    endereco_ERRO = models.BooleanField(default=False)
    verificado_em_loco = models.BooleanField(default=False)
    complemento = models.TextField(null=True, blank=True)

    endereco_nao_mora = models.BooleanField(default=False)   #Se o destinatário não foi encontrado no endereço 1,
                                                            #se ainda não verificado ou positivo 0

    #                           DADOS MANDADO
    numero_mandado = models.IntegerField(verbose_name="Número do Mandado", unique=True)
    ano_mandado = models.CharField(max_length=4, default=str(datetime.date.today().year))
    codigo_mandado = models.CharField(max_length=20, null=True, blank=True)
    data = models.DateField(default=django.utils.timezone.datetime.now, help_text="Data de recebimento.")
    oficial = models.ForeignKey('Oficial', related_name='mandados',
                                help_text='Se em em branco, preenche automaticamente com o usuario atual.', null=True,
                                blank=True)
    ordem = models.ForeignKey('Ordem', default=2, null=True, blank=True,
                              help_text='Citacao, Intimacao, Penhora, Avaliacao, Busca e Ap, etc...')
    audiencia = models.DateField(blank=True, null=True)
    conducao = models.CharField(verbose_name='Condução', max_length=4, blank=True, null=True, default='AJG',
                                choices=(('AJG', 'AJG'),
                                         ('OK', 'Vinculada'),
                                         ('PAGA', 'Não Vinculada'),
                                         ('NO', 'Não Paga'),))
    status_cumprimento = models.ForeignKey('Estatus_Cumprimento', null=True, blank=True, default= 2)  # inserir 1 Recebido
    cumprimento = models.BooleanField(default=True)  # 1_pendente, 0_cumprido
    cor_urgencia = models.CharField(max_length=2, choices=(('1', 'vermelho'),
                                                           ('2', 'amarelo'),
                                                           ('3', 'verde')), default='1')
    rota = models.IntegerField(default=0)
    owner = models.ForeignKey('auth.User', related_name='mands', null=True, blank=True)
    position = GeopositionField(help_text='SALVE E CONTINUE EDITANDO, para visualizar posição no mapa!', blank=True, null=True)
    geo_verificado = models.BooleanField('Localização Verificada', default=False)

    def __str__(self):
        return str(self.codigo_mandado)

    def save(self, *args, **kwargs):
        if not self.position and not self.verificado_em_loco:
            location = "%s, %s, %s, %s, %s" % (self.rua, self.numero, self.cidade, self.estado, self.cep)
            import geoposition
            g = geocoder.google(location)   #geocode endereço
            try:
                self.latitude = g.latlng[0]     #salva local
                self.longitude = g.latlng[1]
            except:
                g = geocoder.google("contabilista vitor brum, alvorada")
                self.latitude = g.latlng[0]     #salva local
                self.longitude = g.latlng[1]

            self.position = geoposition.Geoposition(g.latlng[0], g.latlng[1])   #salva mapa
        elif (not self.verificado_em_loco) and ((self.latitude != self.position.latitude) or (self.longitude != self.position.longitude)):
            self.latitude = self.position.latitude
            self.longitude = self.position.longitude
            self.ajustado_mapa = True
        elif self.verificado_em_loco:
            self.position.latitude = self.latitude
            self.position.longitude = self.longitude
            self.ajustado_mapa = False
        super(Mandado, self).save()


'''
class Mandado(models.Model):
    #                           DADOS DA ORIGEM
    comarca = models.ForeignKey('Comarca', null=True, blank=True)
    vara = models.ForeignKey('Vara', blank=True, null=True)
    processo = models.CharField(blank=True, null=True, max_length=35)
    #                           DADOS DE DESTINATARIO
    destinatario = models.CharField(max_length=100)
    endereco = models.ForeignKey('Endereco', blank=True, null=True)
    endereco_nao_mora = models.BooleanField(default=False)   #Se o destinatário não foi encontrado no endereço 1,
                                                            #se ainda não verificado ou positivo 0

    #                           DADOS MANDADO
    numero_mandado = models.IntegerField(verbose_name="Número do Mandado", unique=True)
    ano_mandado = models.CharField(max_length=4, default=str(datetime.date.today().year))
    codigo_mandado = models.CharField(max_length=20, null=True, blank=True)
    data = models.DateField(default=django.utils.timezone.now(), help_text="Data de recebimento.")
    oficial = models.ForeignKey('Oficial', related_name='mandados',
                                help_text='Se em em branco, preenche automaticamente com o usuario atual.', null=True,
                                blank=True)
    ordem = models.ForeignKey('Ordem', default=2, null=True, blank=True,
                              help_text='Citacao, Intimacao, Penhora, Avaliacao, Busca e Ap, etc...')
    audiencia = models.DateField(blank=True, null=True)
    conducao = models.CharField(verbose_name='Condução', max_length=4, blank=True, null=True, default='AJG',
                                choices=(('AJG', 'AJG'),
                                         ('OK', 'Vinculada'),
                                         ('PAGA', 'Não Vinculada'),
                                         ('NO', 'Não Paga'),))




    # alteração DB em 17/05/2016
    # ddd = models.CharField(max_length=3, default='051')
    # telefone = models.CharField(max_length=9, blank=True, null=True)

    #                               DADOS CUMPRIMENTO
    status_cumprimento = models.ForeignKey('Estatus_Cumprimento', null=True, blank=True)  # inserir 1 Recebido
    cumprimento = models.BooleanField(default=True)  # 1_pendente, 0_cumprido
    cor_urgencia = models.CharField(max_length=2, choices=(('1', 'vermelho'),
                                                           ('2', 'amarelo'),
                                                           ('3', 'verde')), default='1')
    rota = models.CharField(max_length=3, default='0')
    owner = models.ForeignKey('auth.User', related_name='mands', null=True, blank=True)

    def __str__(self):
        return str(self.ano_mandado) + '/' + str(self.numero_mandado)


"""
    def save(self, request=None, *args, **kwargs):
        self.owner = request.user
        super(Mandado, self).save(*args, **kwargs) # Call the "real" save() method.
"""


class Endereco(models.Model):
    cep = models.ForeignKey('CEP', null=True, blank=True)
    numero = models.CharField(verbose_name='Número da Casa', max_length=6)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    endereco_ERRO = models.BooleanField(default=False)
    verificado_em_loco = models.BooleanField(default=False)
    complemento = models.TextField(null=True, blank=True)

    def __str__(self):

        return str(self.cep)+', '+str(self.numero)


class CEP(models.Model):
    cep = models.CharField(max_length=9, null=True, blank=True,
                           help_text='Alternativamente, preencha "Campos de Endereço".',)
    rua = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50, default="Rio Grande do Sul")
    pais = models.CharField(max_length=50, default="Brasil")
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    ajustado_mapa = models.BooleanField(default=False)

    def __str__(self):
        return str(self.estado)+', '+str(self.cidade)+', '+str(self.rua).split(' - ')[0]
'''

class Estatus_Cumprimento(models.Model):
    estatus_cumprimento = models.CharField(max_length=20)
    descricao = models.TextField()
    exibir_mapa = models.BooleanField()
    cumprimento = models.BooleanField(default=False)

    def __str__(self):
        return str(self.estatus_cumprimento)


class Oficial(models.Model):
    class Meta:
        verbose_name = 'Oficial'
        verbose_name_plural = 'Oficiais'

    usuario = models.OneToOneField(User)
    telefone = models.DecimalField(max_digits=10, decimal_places=0, )
    email = models.EmailField(null=True, blank=True)
    cpf = models.CharField(max_length=11, default='12345678901')
    #endereco = models.ForeignKey(Endereco, null=True, blank=True)
    comarca = models.ForeignKey('Comarca', null=True, blank=True)

    def __str__(self):
        return str(self.usuario.first_name) + ' ' + str(self.usuario.last_name)


class Ordem(models.Model):
    ordem = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)
    diligencia_positiva = models.ForeignKey('Tipo_Diligencia', null=True, blank=True)

    def __str__(self):
        return str(self.ordem)


class Telefone(models.Model):
    ddd = models.CharField(default='051', max_length=3, null=True, blank=True)
    telefone = models.CharField(max_length=9, null=True, blank=True)
    contato = models.CharField(max_length=50, blank=True, null=True)
    mandado = models.ForeignKey(Mandado, blank=True, null=True, related_name='telefone')
    #endereco = models.ForeignKey(Endereco, blank=True, null=True, related_name='telefone')
    oficial = models.ForeignKey('Oficial', related_name='lista_telefones',
                                help_text='Se em em branco, preenche automaticamente com o usuario atual.', null=True,
                                blank=True)

    def save(self, *args, **kwargs):
        """
        """
        if self.telefone:
            super(Telefone, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.mandado.destinatario) + ': ' + str(self.ddd) + '-' + str(self.telefone)


class Modelo_Documento(models.Model):
    nome = models.CharField(max_length=50)
    modelo = HTMLField()
    descricao = models.TextField()
    editar_sempre = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Diligencia(models.Model):
    mandado = models.ForeignKey(Mandado)
    data_diligencia = models.DateField('Data da Diligência',default=django.utils.timezone.datetime.now)#datetime.today())
    hora_diligencia = models.TimeField(default=django.utils.timezone.datetime.now)#datetime.now())
    tipo_diligencia = models.ForeignKey("Tipo_Diligencia", blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    data_agendamento = models.DateField(blank=True, null=True)
    hora_agendamento = models.TimeField(blank=True, null=True)
    documento = HTMLField(blank=True, null=True)
    editar_documento = models.BooleanField(default=False)
    not_editar_documento = models.BooleanField('Editar Certidão', default=True)#inversão do flag, para exibir corretamente no admin
    rendered = models.BooleanField(default=False)
    imprimir = models.BooleanField(default=False)

    def __str__(self):
        return str(self.mandado.codigo_mandado)+' '+str(self.tipo_diligencia)

    def save(self, request=None, *args, **kwargs):
        from django import template
        if not self.rendered:   #para não desfazer a edição do documento, cria o documento só na primeira vez
            #super(Diligencia, self).save(*args, **kwargs) # Call the "real" save() method.
            t = template.Template(self.tipo_diligencia.modelo_documento.modelo)
            c = template.Context({'mandado':self.mandado, "diligencia":self})
            self.documento = t.render(c)
            self.imprimir = True    # vai para false quando gera o pdf da certidao no arquivo printing
            self.rendered = True
        self.not_editar_documento = not self.editar_documento
        super(Diligencia, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Certidão"
        verbose_name_plural = "Certidões"


class Tipo_Diligencia(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    modelo_documento = models.ForeignKey(Modelo_Documento, null=True, blank=True)
    estatus_cumprimento = models.ForeignKey(Estatus_Cumprimento)
    diligencia_positiva = models.BooleanField(default=False)
    diligencia_parcial = models.BooleanField(default=False)
    diligencia_negativa = models.BooleanField(default=False)
    diligencia_nao_cumprida = models.BooleanField(default=False)
    diligencia_cumprida = models.BooleanField(default=False)
    endereco_ERRO = models.BooleanField(default=False)
    diligencia_nao_mora = models.BooleanField(default=False)
    verificado_em_loco = models.BooleanField(default=False)
    diligencia_externa = models.BooleanField(default=False)
    diligencia_coletiva = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)


class Comarca(models.Model):
    nome = models.CharField(max_length=50)
    cod_comarca = models.CharField(max_length=5)
    #endereco = models.ForeignKey(Endereco, null=True, blank=True)

    def __str__(self):
        return str(self.nome)


class Vara(models.Model):
    nome = models.CharField(max_length=50)
    comarca = models.ForeignKey(Comarca, null=True, blank=True)

    def __str__(self):
        return str(self.nome)


class Foto(models.Model):
    diligencia = models.ForeignKey(Diligencia, null=True, blank=True)
    foto = models.ImageField()
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Foto'+' '+str(self.diligencia)


class Audio(models.Model):
    diligencia = models.ForeignKey(Diligencia, null=True, blank=True)
    audio = models.BinaryField()
    descricao = models.TextField()

    def __str__(self):
        return 'Audio'+' '+str(self.diligencia)


class Atendimento(models.Model):
    oficial = models.ForeignKey(Oficial)#, null=True, blank=True)
    data = models.DateField()
    inicio = models.TimeField(null=True, blank=True)
    fim = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.oficial)+' Atendimento'+' '+str(self.data)


class Relatorio(models.Model):
    oficial = models.ForeignKey(Oficial, null=True, blank=True)
    relatorio = models.FileField()

    def __str__(self):
        return 'Mandados:'+' '+str(self.relatorio)+' '+str(self.oficial)