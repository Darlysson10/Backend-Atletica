from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Produto, Venda, Usuario, Eventos, Administrador, Carrinho
from .serializers import ProdutoSerializer, VendaSerializer, UsuarioSerializer, EventosSerializer, AdiministradorSerializer, CarrinhoSerializer
from django.contrib.auth.decorators import user_passes_test
from rest_framework import permissions

class MinhaPermissao(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

#criar uma função post de onde se cria um serializer e esse serializer é jogado numa função de tratamento dos dados recebidos
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    def retrieve (self, request, pk=None):
        try:
            produto = Produto.objects.get(id=pk)
            serializer = ProdutoSerializer(produto)
            return Response(serializer.data)
        except:
            return Response({'mensagem': 'Produto não encontrado'})


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

class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = CarrinhoSerializer
    #TODO - GET: Mudar para uma consulta que é feita pelo id do usuário logado