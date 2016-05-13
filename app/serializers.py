__author__ = 'Dudu'

from django.forms import widgets
from rest_framework import serializers
from app.models import Mandado, Oficial #, Endereco, Telefone
from django.contrib.auth.models import User

'''
criar igual par o oficial para os demais campos que nao forem char
dai fica bao!
'''

class MandadoSerializer(serializers.ModelSerializer):
    oficial = serializers.ReadOnlyField(source='oficial.usuario.username')
    class Meta:
        model = Mandado
        fields = (
            'id',
            'comarca',
            'vara',
            'processo',
            'conducao',
            'ano_mandado',
            'numero_mandado',
            'n_mandado',
            'data',
            'oficial',
            'ordem',
            'audiencia',
            'destinatario',
            'ddd',
            'telefone',
            'cep',
            'estado',
            'cidade',
            'bairro',
            'rua',
            'numero_rua',
            'complemento',
            'latitude',
            'longitude',
            'status_cumprimento',
            )


class OficialSerializer(serializers.ModelSerializer):
    mandados = serializers.PrimaryKeyRelatedField(many=True, queryset=Mandado.objects.all())
    class Meta:
        model = Oficial
        fields = (
            'id',
            'usuario',
            'telefone',
            'mandados',
        )



'''
class EnderecoSerializer(serializers.ModelSerializer):
    rua = serializers.StringRelatedField()
    bairro = serializers.StringRelatedField()
    class Meta:
        model = Endereco
        fields = (
            'id',
            'rua',
            'bairro',
            'numero',
            'complemento',
        )


class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = (
            'id',
            'ddd',
            'telefone',
        )
'''
