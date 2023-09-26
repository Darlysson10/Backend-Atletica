# Backend Atletica
## Árvore de diretórios
```bash
├──  BackendAtletica (pasta principal do projeto)
│    ├── BackendAtletica
│    │   ├── asgi.py
│    │   ├── __init__.py
│    │   ├── __pycache__
│    │   ├── settings.py
│    │   ├── urls.py
│    │   └── wsgi.py
│    ├── core
│    ├── manage.py
│    ├── .env
├── venv    
├── .gitignore
├── README.md
├── requirements.txt
```
## Como rodar o projeto
### Criar ambiente virtual na pasta raiz do projeto
```bash
python -m venv venv
```
### Ativar ambiente virtual
```bash
venv\Scripts\activate.bat # Windows
source venv/bin/activate # Linux
```
### Instalar dependências
```bash
pip install -r requirements.txt
```
### Acesse a pasta do projeto
```bash
cd BackendAtletica
```

### Criar arquivo .env
Você pode copiar o arquivo .env.template e renomear para .env na pasta do principal BackendAtletica. Preencha com os campos do seu banco de dados Postgres.
### Criar banco de dados
```bash
python manage.py makemigrations
python manage.py migrate
```
### Criar super usuário
```bash
python manage.py createsuperuser
```
### Rodar servidor
```bash
python manage.py runserver
```
### Endpoints
```bash
/produtos/
/vendas/
/eventos/
/administradores/ # Somente super usuário
/membros/
/carrinho/
/bancoespera/
/inscricao/
/register/
/login/
/logout/
```