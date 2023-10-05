from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Produto, Venda, Eventos, Carrinho, Candidato, Usuario
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from .validators import evento_validator

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
@permission_classes([IsAdminOrReadOnly])
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
    def create (self, request):
        serializer = serializers.ProdutoSerializer(data=request.data)
        if serializer.is_valid() and request.user.is_staff:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
@permission_classes([IsAdminOrReadOnly])
class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = serializers.VendaSerializer
    def list(self, request):
        if request.user.is_staff:
            vendas = Venda.objects.all()
            serializer = serializers.VendaSerializer(vendas, many=True)
            return Response(serializer.data)
        else:
            return Response({'mensagem': 'Você não tem permissão para acessar essa página'})

@api_view(['POST'])
@permission_classes([IsGuest])
def register(request):
    if request.method == 'POST' and not request.user.is_staff:
        serializer = serializers.UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsGuest])
def login(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username,password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuário ou senha inválidos'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'mensagem': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'error': 'Não foi possível realizar o logout'}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminOrReadOnly])
class EventosViewSet(viewsets.ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = serializers.EventosSerializer
    def create(self, request):
        if not request.user.is_staff:
            return Response({'mensagem': 'Você não tem permissão para acessar essa página'})
        serializer = serializers.EventosSerializer(data=request.data)
        validacao_resposta, codigo_validacao = evento_validator.Evento_Validator.validate(self, request)
        if serializer.is_valid() and codigo_validacao == 200:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif codigo_validacao == 400:
            return Response(validacao_resposta, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        eventos = Eventos.objects.all()
        serializer = serializers.EventosSerializer(eventos, many=True)
        return Response(serializer.data)
    def get_by_id(self, request, pk):
        evento = Eventos.objects.get(id=pk)
        serializer = serializers.EventosSerializer(evento)
        return Response(serializer.data)
    def destroy(self, request, pk):
        if not request.user.is_staff:
            return Response({'mensagem': 'Você não tem permissão para acessar essa página'})
        evento = Eventos.objects.get(id=pk)
        evento.delete()
        return Response({'mensagem': 'Evento deletado com sucesso'})

@permission_classes([IsAdminOrReadOnly])
class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer
    def list(self, request):
        if request.user.is_staff:
            administradores = Usuario.objects.filter(is_staff=True)
            serializer = serializers.UsuarioAsAdminSerializer(administradores, many=True)
            return Response(serializer.data)
        else:
            return Response({'mensagem': 'Você não tem permissão para acessar essa página'})
    def create(self, request):
        return Response({'mensagem': 'Não é possível criar um administrador por aqui'})

@permission_classes([IsAdminOrReadOnly])
class PublicAdministradorViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = serializers.UsuarioAdminPublicSerializer
    def list(self, request):
        membros = Usuario.objects.filter(is_staff=True)
        serializer = serializers.UsuarioAdminPublicSerializer(membros, many=True)
        return Response(serializer.data)
    

@permission_classes([IsAuthenticated])
class CarrinhoViewSet(viewsets.ModelViewSet):
    queryset = Carrinho.objects.all()
    serializer_class = serializers.CarrinhoSerializer
    def list(self, request):
            carrinho = Carrinho.objects.filter(idUsuario=request.user)
            serializer = serializers.CarrinhoSerializer(carrinho, many=True)
            return Response(serializer.data)
    def create(self, request):
        serializer = serializers.CarrinhoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(idUsuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        carrinho = Carrinho.objects.get(id=pk, idUsuario=request.user)
        carrinho.delete()
        return Response({'mensagem': 'Produto removido do carrinho com sucesso'})
    def update(self, request, pk=None):
        carrinho = Carrinho.objects.get(id=pk)
        serializer = serializers.CarrinhoSerializer(carrinho, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsGuest])
class CandidatoViewSet(viewsets.ModelViewSet):
    queryset = Candidato.objects.all()
    serializer_class = serializers.CandidatoSerializer
    
    def create(self, request):
        serializer = serializers.CandidatoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self, request, *args, **kwargs):
        return Response({'mensagem': 'Não é possível listar os candidatos por aqui'})
    
@permission_classes([IsAdminOrReadOnly])
class BancoEsperaViewSet(viewsets.ModelViewSet):
    queryset = Candidato.objects.all()
    serializer_class = serializers.CandidatoSerializer
    def list(self, request):
        if request.user.is_staff:
            candidato = Candidato.objects.all()
            serializer = serializers.CandidatoSerializer(candidato, many=True)
            return Response(serializer.data)
        else:
            return Response({'mensagem': 'Você não tem permissão para acessar essa página'})
    def create(self, request):
        return Response({'mensagem': 'Não é possível criar um candidato por aqui'})