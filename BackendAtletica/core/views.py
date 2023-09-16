from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Produto, Venda, Usuario, Eventos, Administrador, Carrinho, Candidato
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated

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

#criar uma função post de onde se cria um serializer e esse serializer é jogado numa função de tratamento dos dados recebidos
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

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = serializers.UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
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


class EventosViewSet(viewsets.ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = serializers.EventosSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = serializers.AdiministradorSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
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
        carrinho = Carrinho.objects.get(id=pk)
        carrinho.delete()
        return Response({'mensagem': 'Produto removido do carrinho com sucesso'})
    def update(self, request, pk=None):
        carrinho = Carrinho.objects.get(id=pk)
        serializer = serializers.CarrinhoSerializer(carrinho, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CandidatoViewSet(viewsets.ModelViewSet):
    queryset = Candidato.objects.all()
    serializer_class = serializers.CandidatoSerializer
    
    def create(self, request):
        serializer = serializers.CandidatoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        if request.user.is_staff:
            candidato = Candidato.objects.all()
            serializer = serializers.CandidatoSerializer(candidato, many=True)
            return Response(serializer.data)
        else:
            return Response({'mensagem': 'Você não tem permissão para acessar essa página'})
#TODO - GET: Mudar para uma consulta que é feita pelo id do usuário logado