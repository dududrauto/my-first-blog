__author__ = 'Dudu'

from django.forms import widgets
from rest_framework import serializers
from app.models import Mandado, Oficial, Telefone, Diligencia, Tipo_Diligencia,\
    Estatus_Cumprimento, Foto, Audio, Vara, Comarca, Ordem
from django.contrib.auth.models import User


class MandadoSerializer(serializers.ModelSerializer):
    oficial = serializers.ReadOnlyField(source='oficial.usuario.username')

    class Meta:
        model = Mandado
        fields = (
            'id',
            'comarca',#
            'vara',#
            'processo',#
            'destinatario',#
            'cep',#
            'rua',#
            'numero',#
            'bairro',#
            'cidade',#
            'estado',#
            'pais',#
            'latitude',#
            'longitude',#
            'endereco_ERRO',#
            'verificado_em_loco',#
            'complemento',#
            'endereco_nao_mora',#
            'endereco_ERRO',#
            'verificado_em_loco',#
            'complemento',#
            'ajustado_mapa',#
            'endereco_nao_mora',#
            'numero_mandado',#
            'ano_mandado',#
            'codigo_mandado',#
            'data',#
            'oficial',#
            'ordem',#
            'audiencia',#
            'conducao',#
            'status_cumprimento',#
            'cumprimento',#
            'cor_urgencia',#
            'rota',#
            'owner',#
            )


class OficialSerializer(serializers.ModelSerializer):
    mandados = serializers.PrimaryKeyRelatedField(many=True, queryset=Mandado.objects.all())
    class Meta:
        model = Oficial
        fields = (
            'id',
            'usuario',
            'telefone',
            'email',
            'cpf',
            'endereco',
            'comarca',
            'mandados',
        )

'''
class CepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CEP
        fields = (
            'id',
            'cep',
            'rua',
            'bairro',
            'cidade',
            'estado',
            'pais',
            'latitude',
            'longitude',
            'ajustado_mapa'
        )

'''
class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = (
            'id',
            'ddd',
            'telefone',
            'mandado',
        )

'''
class EnderecoSerializer(serializers.ModelSerializer):
    cep_str = serializers.CharField(source='cep', read_only=True)
    class Meta:
        model = Endereco
        fields = (
            'id',
            'cep',
            'cep_str',
            'numero',
            'latitude',
            'longitude',
            'endereco_ERRO',
            'verificado_em_loco',
            'complemento',
        )
'''

class DiligenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diligencia
        fields = (
            'id',
            'mandado',
            'data_diligencia',
            'hora_diligencia',
            'tipo_diligencia',
            'latitude',
            'longitude',
            'data_agendamento',
            'hora_agendamento',
            'documento',
            'editar_documento',
        )


class Tipo_DiligenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_Diligencia
        fields = (
            'id',
            'nome',
            'descricao',
            'modelo_documento',
            'estatus_cumprimento',
            'diligencia_positiva',
            'diligencia_cumprida',
            'diligencia_parcial',
            'endereco_ERRO',
            'diligencia_nao_mora',
            'verificado_em_loco',
            'diligencia_externa',
            'diligencia_coletiva',
        )


class Estatus_CumprimetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estatus_Cumprimento
        fields = (
            'id',
            'estatus_cumprimento',
            'descricao',
            'flag_cumprimento',
        )


class OrdemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordem
        fields = (
            'id',
            'ordem',
            'descricao',
            'diligencia_positiva',
        )


class ComarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comarca
        fields = (
            'nome',
            'cod_comarca',
            'endereco',
        )


class VaraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vara
        fields = (
            'nome',
            'comarca',
        )


class FotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foto
        fields = (
            'diligencia',
            'descricao',
            'foto',
        )


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = (
            'diligencia',
            'descricao',
            'audio',
        )
