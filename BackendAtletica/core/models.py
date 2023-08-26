from django.db import models

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

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)


class Eventos(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    local = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class BancoEspera (models.Model):
    idUsuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
