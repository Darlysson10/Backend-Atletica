from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Produto, Venda, Usuario, Eventos, Administrador

# Serializers define the API representation.
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('nome', 'preco', 'descricao', 'qtdEstoqueInicial', 'qtdVendidaTotal', 'qtdSaldo', 'categoria')

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ('produto', 'idVenda', 'valor', 'dataVenda', 'idVendedor', 'idComprador', 'metodoPagamento', 'qtdVendido')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nome', 'username', 'cpf', 'email', 'telefone', 'endereco', 'senha', 'matricula')

class EventosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = ('nome', 'descricao', 'data', 'local')

class AdiministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ('nome', 'username', 'cpf', 'email', 'telefone', 'endereco', 'senha', 'matricula', 'diretoria')


#TODO - Criar os serializers para as outras classes        