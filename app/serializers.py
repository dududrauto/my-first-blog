__author__ = 'Dudu'

from django.forms import widgets
from rest_framework import serializers
from app.models import Mandado, Oficial, Telefone, Diligencia, Tipo_Diligencia,\
    Estatus_Cumprimento, Foto, Audio, Vara, Comarca, Ordem, Json_sync
from django.contrib.auth.models import User, Group
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)


class MandadoSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    oficial = serializers.ReadOnlyField(source='oficial.usuario.username')

    class Meta:
        model = Mandado
        list_serializer_class = BulkListSerializer
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
            'diligencia_parcial',
            'diligencia_negativa',
            'diligencia_nao_cumprida',
            'diligencia_cumprida',
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
            'exibir_mapa',
            'cumprimento',
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
            'id',
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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id','url', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'snippets', 'password', 'email')

    def create(self, validated_data):
        # colocar aqui as configurações do usuario que quero, ver a parte dos grupos e fazer oficial sempre
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.is_staff = True
        user.is_superuser = False
        user.groups.set([Group.objects.get(name='Oficial'),])

        user.save()
        return user
