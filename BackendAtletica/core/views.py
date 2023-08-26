from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Produto
from .serializers import ProdutoSerializer

# Create your views here.
class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

#TODO - Criar as views para as outras classes