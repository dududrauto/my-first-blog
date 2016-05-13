# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime

# Create your models here.
class Mandado(models.Model):

    #                           DADOS COMARCA/VARA
    comarca = models.DecimalField(max_digits=3, decimal_places=0, default="003")
    vara = models.CharField(max_length=20, blank=True, null=True)

    #                           DADOS PROCESSO
    processo = models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0)
    conducao = models.CharField(verbose_name='Condução', max_length=4, blank=True, null=True, default='AJG',
                                choices=(('AJG', 'Assistência Judiciária Gratuita'),
                                         ('OK', 'Recolhida Vinculada'),
                                         ('PAGA', 'Falta Vincular'),
                                         ('NO', 'Não Paga'),))

    #                           DADOS MANDADO
    ano_mandado = models.CharField(max_length=4, default=str(datetime.date.today().year))
    numero_mandado = models.CharField(max_length=8)#models.IntegerField()#
    n_mandado = models.IntegerField(verbose_name="Número do Mandado", unique=True)#
    data = models.DateField(default=datetime.date.today(), help_text="Data de recebimento.")
    oficial = models.ForeignKey('Oficial', related_name='mandados', help_text='Se em em branco, preenche automaticamente com o usuario atual.', null=True, blank=True)
    ordem = models.ForeignKey('Ordem', default=2, help_text='Citacao, Intimacao, Penhora, Avaliacao, Busca e Ap, etc...')
    audiencia = models.DateField(blank=True, null=True)


    #                           DADOS DESTINATARIO
    destinatario = models.CharField(max_length=100)
    ddd = models.CharField(max_length=3, default='051')
    telefone = models.CharField(max_length=9, blank=True, null=True)
    cep = models.CharField(max_length=9, null=True, blank=True, help_text='Alternativamente, preencha "Campos de Endereço".')
    pais = models.CharField(max_length=50, default="Brasil")
    estado = models.CharField(max_length=50, default= "Rio Grande do Sul")
    cidade = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50, null=True, blank=True)
    rua = models.CharField(max_length=100, null=True, blank=True)
    numero_rua = models.CharField(verbose_name='Número da Casa', max_length=6)
    complemento = models.CharField(max_length=20, null=True, blank=True) #####   AUMENTAR!!!!!
    latitude = models.CharField(max_length=30, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)

    #                               DADOS CUMPRIMENTO
    status_cumprimento = models.CharField(max_length=2,
                                          default='pu',
                                          choices=(('rd', 'Urgente'), ('gr', '$'), ('pu', 'Normal'),
                                                   ('AV', 'Avidado'), ('DV', 'Devolvido'), ('CE', "Certificar"), ),
                                          verbose_name='Status')


    '''  choices=(('RC', 'Recebido'),
                                                   ('AV', 'Avisado'),
                                                   ('CP', 'Cumprido Positivo'),
                                                   ('NN', 'Negativa Numero'),
                                                   ('NE', 'Negativa de Endereço'),
                                                   ('CE', 'Contrafé Endereço'),
                                                   ('NC', 'Não Cumprido')'''
    owner = models.ForeignKey('auth.User', related_name='snippets', null=True, blank=True)

    def __unicode__(self):
        return unicode(str(self.ano_mandado)+'/'+str(self.numero_mandado))#unicode para corrigir o erro que dava no popup inserindo mandado
                                                                #Error with admin popups: expected a character buffer object
'''
    def save(self, request=None, *args, **kwargs):
        self.owner = request.user
        super(Mandado, self).save(*args, **kwargs) # Call the "real" save() method.
'''





class Ordem(models.Model):#acho que aqui vai ficar bem com revese relations field, um para muitos, ou seja foreignkey aqui para mandados
    #dai os tipos são cada um... (citação, intimação, penhora, busca e apreensão...) podendo assim combinar o que for...
    #não sei dai no serializers como que vai ficar..., se vou usar igual para o usuário chamando related field, set, ou outra forma
    tipo = models.CharField(max_length=10,)#criar um p cada com modelos especificos
    modelo = models.ForeignKey('Modelo')

    def __unicode__(self):
        return unicode(str(self.tipo))


class Oficial(models.Model):
    usuario = models.ForeignKey(User, unique=True)
    telefone = models.DecimalField(max_digits=10, decimal_places=0,)

    def __unicode__(self):
        return unicode(str(self.usuario.first_name) + ' ' + str(self.usuario.last_name))


class Atendimento(models.Model):
    oficial = models.ForeignKey('Oficial')
    dia = models.DateField()
    horario = models.TimeField(verbose_name='das')
    fim = models.TimeField(verbose_name='às')

    def __unicode__(self):
        return self.dia.strftime("%d/%m/%y") + ' (' + self.horario.strftime('%H:%M') + ' -> ' + self.fim.strftime('%H:%M')+ ')'


class Aviso(models.Model):
    oficial = models.ForeignKey('Oficial')
    atendimento = models.ForeignKey('Atendimento')
    aviso = HTMLField(default="Aqui será inserido automaticamente para mandados relacionados!")# modelo_aviso.html
    data_aviso = models.DateField(auto_now=True)#data criação/edição

    def __unicode__(self):
        a = self.agendamento_set.all()[0]
        return str(self.oficial.usuario)+': '+a.dia.strftime("%d/%m/%y")+' ('+a.horario.strftime('%H:%M')+' -> '+a.fim.strftime('%H:%M')+')'


class Documento(models.Model):
    oficial = models.ForeignKey('Oficial')
    mandado = models.ForeignKey(Mandado)
    documento = HTMLField()
    atendimento = models.ForeignKey('Atendimento', blank=True, null=True)
    modelo = models.ForeignKey('Modelo')
    data = models.DateField(default=datetime.datetime.now())


class Modelo(models.Model):
    nome = models.CharField(max_length=50)
    modelo = HTMLField()

    def __unicode__(self):
        return unicode(self.nome)


'''
class Endereco(models.Model):
    mandado = models.ForeignKey('Mandado', related_name='endereco')
    rua = models.ForeignKey("Rua")
    bairro = models.ForeignKey("Bairro", blank=True, null=True)
    numero = models.IntegerField()
    complemento = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.rua) + ", " + str(self.bairro) + ", " + str(self.numero))


class Rua(models.Model):
    rua = models.CharField(max_length=30)
    min_num = models.IntegerField(blank=True, null=True)
    max_num = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.rua)


class Bairro(models.Model):
    bairro = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode(self.bairro)


class Telefone(models.Model):
    ddd = models.DecimalField(default='051', max_digits=3, decimal_places=0, null=True, blank=True)
    telefone = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True)
    mandado = models.ForeignKey(Mandado, blank=True, null=True, related_name='telefone')

    def save(self, *args, **kwargs):
        """
        """
        if self.telefone:
            super(Telefone, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.mandado.destinatario + ': ' + str(self.ddd) + '-' + str(self.telefone))


class Status(models.Model):
    mandado = models.ForeignKey(Mandado)
    oficial = models.ForeignKey('Oficial')
    status = models.CharField(max_length=2, choices=(('CP', 'Cumprido Positivo'),
                                                     ('CN', 'Cumprido Negativo'),
                                                     ('NC', 'Devolver a pedido'),
                                                     ('PC', 'Parcialmente Cumprido'),
                                                     ('MR', 'Mandado Recebido'),
                                                     ('RD', 'Mandado Redistribuido'),
                                                     ('DN', 'Diligencia Negativa'),
                                                     ('AV', 'Mandado Avisado'),
                                                     ('AG', 'Cumprimento Agendado'),))


    def __unicode__(self):
        return unicode(str(self.oficial.usuario) + ':' + str(self.mandado.numero)+' -> '+str(self.status))



'''
