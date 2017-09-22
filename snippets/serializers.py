__author__ = 'Dudu'
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User, Group

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser', 'snippets', 'password', 'email')

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