from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Produto, Venda, Usuario, Eventos, Carrinho, Candidato
# Serializers define the API representation.
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('__all__')

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ('__all__')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'nome', 'cpf', 'telefone', 'endereco', 'matricula']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario(
            username=validated_data['username'],
            email=validated_data['email'],
            nome=validated_data['nome'],
            cpf=validated_data['cpf'],
            telefone=validated_data['telefone'],
            endereco=validated_data['endereco'],
            matricula=validated_data['matricula']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UsuarioAdminPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nome', 'diretoria']

class UsuarioAsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome', 'cpf', 'telefone', 'endereco', 'matricula', 'diretoria']
        

class EventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ('__all__')


class CarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrinho
        fields = ('__all__')



class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = ('__all__')

#TODO - Criar os serializers para as outras classes        