from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Produto, Venda, Usuario, Eventos, Administrador, Carrinho
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
        fields = ('__all__')

class EventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ('__all__')

class AdiministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('__all__')

class AdministradorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('nome', 'diretoria')

class AdministradorAsAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('nome', 'username', 'cpf', 'email', 'telefone', 'endereco', 'matricula', 'diretoria')

class CarrinhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrinho
        fields = ('__all__')
        
#TODO - Criar os serializers para as outras classes        