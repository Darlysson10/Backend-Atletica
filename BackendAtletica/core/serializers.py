from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Produto

# Serializers define the API representation.
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('nome', 'preco', 'descricao', 'qtdEstoqueInicial', 'qtdVendidaTotal', 'qtdSaldo', 'categoria')

#TODO - Criar os serializers para as outras classes        