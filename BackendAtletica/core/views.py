from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Produto, Venda, Usuario, Eventos, Administrador
from .serializers import ProdutoSerializer, VendaSerializer, UsuarioSerializer, EventosSerializer, AdiministradorSerializer
from django.contrib.auth.decorators import user_passes_test
from rest_framework import permissions

class MinhaPermissao(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [MinhaPermissao]

class EventosViewSet(viewsets.ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = EventosSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdiministradorSerializer
    permission_classes = [MinhaPermissao]

#TODO - Criar as views para as outras classes