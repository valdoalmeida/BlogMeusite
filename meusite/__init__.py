import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

# Cria a aplicação Flask
app = Flask(__name__)

# Definindo a chave secreta para a aplicação
# A chave secreta é usada para proteger sessões e cookies
app.config['SECRET_KEY'] = '9140a32b7f46b6c0742849a172cbad7e'




# Caminho absoluto para o banco de dados SQLite
# Isso cria um caminho para o arquivo 'banco.db' que estará na mesma pasta do script
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'banco.db')

# Verifica se o diretório onde o banco de dados será armazenado não existe
# Se não existir, cria o diretório
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))


if os.getenv("DATABASE_URL"):
    # Configuração da URI para o banco de dados SQLite
    # O banco de dados estará localizado no caminho 'db_path'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'



# Desativa a geração de alertas sobre modificações no banco de dados
# Isso evita o aparecimento de um alerta no console sempre que o SQLAlchemy detecta que a aplicação
# está modificando o banco de dados. Isso pode ser útil em ambientes de produção.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa as extensões do Flask

# Configura a base de dados com o SQLAlchemy
database = SQLAlchemy(app)

# Configura o Bcrypt para criptografar senhas
bcrypt = Bcrypt(app)

# Inicializa o LoginManager para gerenciar as sessões de login dos usuários
login_manager = LoginManager(app)

# Especifica a rota de login que o LoginManager irá redirecionar caso o usuário não esteja autenticado
login_manager.login_view = 'login'

# Categoria de mensagem para quando o usuário não estiver autenticado
login_manager.login_message_category = 'alert-info'

from meusite import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

inspect = sqlalchemy.inspect(engine)

if not inspect.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Banco de dados Criada")
else:
    print("Banco de dados já existente")
# Importa as rotas da aplicação (deve ser feito após a criação da aplicação)
from meusite import routes
