from django.contrib import admin
from .models import Usuario, Produto, Venda, Eventos, Candidato

admin.site.register(Usuario)
admin.site.register(Produto)
admin.site.register(Venda)
admin.site.register(Eventos)
admin.site.register(Candidato)

# Register your models here.
