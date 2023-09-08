from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Produto, Venda, Usuario, Eventos, Administrador, Carrinho
from . import serializers
from django.contrib.auth.decorators import user_passes_test
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_staff

class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.user.is_staff:
            return True
        return  not request.user

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = serializers.ProdutoSerializer
    def retrieve (self, request, pk=None):
        try:
            produto = Produto.objects.get(id=pk)
            serializer = serializers.ProdutoSerializer(produto)
            return Response(serializer.data)
        except:
            return Response({'mensagem': 'Produto não encontrado'})
        
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = serializers.VendaSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer
    permission_classes = [IsGuest]

    def create(self, request):
        serializer = serializers.UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            if len(self.queryset.filter(username=serializer.validated_data['username'])) == 0:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'mensagem': 'Usuário já cadastrado'})
        return Response(serializer.errors)

class EventosViewSet(viewsets.ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = serializers.EventosSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = serializers.AdiministradorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        administrador = Administrador.objects.all()
        if request.user.is_staff:
            serializer = serializers.AdministradorAsAdminListSerializer(administrador, many=True)
        else:
            serializer = serializers.AdministradorListSerializer(administrador, many=True)
        return Response(serializer.data)

class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = serializers.CarrinhoSerializer


#TODO - GET: Mudar para uma consulta que é feita pelo id do usuário logado