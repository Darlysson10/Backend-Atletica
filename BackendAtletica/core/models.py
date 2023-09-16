from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    qtdEstoqueInicial = models.IntegerField()
    qtdVendidaTotal = models.IntegerField()
    qtdSaldo = models.IntegerField() #é a diferença do qtdEstoqueInicial - qtdVendida
    categoria = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Venda(models.Model):
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    idVenda = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    dataVenda = models.DateTimeField(auto_now_add=True)
    idVendedor = models.ForeignKey('Administrador', on_delete=models.CASCADE)
    idComprador = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    metodoPagamento = models.CharField(max_length=100)
    qtdVendido = models.IntegerField()
    

    def __str__(self):
        return self.produtos

#classe carrinho, não precisa de persistência de dados, será armazenado na sessão

class Administrador(models.Model):
    nome = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    diretoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Eventos(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Candidato (models.Model):
    
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    periodo = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Carrinho (models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    idUsuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.produtos