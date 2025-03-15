from meusite import database, login_manager
from datetime import datetime
from flask_login import UserMixin

# Função do Flask-Login para carregar um usuário a partir do banco de dados
# O Flask-Login usa esta função para carregar um usuário baseado no id do usuário armazenado na sessão
@login_manager.user_loader
def load_usuario(id_usuario):
    """
    Função chamada pelo Flask-Login para carregar o usuário da sessão.
    Recebe o id do usuário como argumento e retorna o objeto `Usuario` correspondente no banco de dados.
    """
    return Usuario.query.get(int(id_usuario))  # Retorna o usuário pelo id fornecido


# Modelo de Usuário no banco de dados
# O modelo `Usuario` herda de `UserMixin` para fornecer os métodos necessários ao Flask-Login
class Usuario(database.Model, UserMixin):
    """
    Classe que representa um usuário no banco de dados.
    O modelo `Usuario` é associado a um banco de dados relacional e permite a manipulação de dados relacionados ao usuário.
    """
    id = database.Column(database.Integer, primary_key=True)  # ID do usuário, chave primária
    username = database.Column(database.String, nullable=False)  # Nome de usuário, campo obrigatório
    email = database.Column(database.String, nullable=False, unique=True)  # E-mail do usuário, único e obrigatório
    senha = database.Column(database.String, nullable=False)  # Senha do usuário, obrigatória
    foto_perfil = database.Column(database.String, default='default.jpg', nullable=False)  # Foto de perfil, com valor padrão
    posts = database.relationship('Post', backref='autor_post', lazy=True)  # Relacionamento com o modelo `Post`
    cursos = database.Column(database.String, nullable=False, default='Não Informado')  # Cursos do usuário, com valor padrão

    # O `__repr__` é um método especial que define a forma como o objeto será representado
    def __repr__(self):
        return f"<Usuario {self.username}>"  # Retorna uma string representando o nome do usuário

    # Função de contar Post por usuario dentro da classe Usuarios
    def contar_posts(self):
        return len(self.posts)













# Modelo de Post no banco de dados
# O modelo `Post` representa uma postagem feita por um usuário na plataforma
class Post(database.Model):
    """
    Classe que representa um post realizado por um usuário.
    Contém o título, conteúdo e a data de criação do post.
    """
    id = database.Column(database.Integer, primary_key=True)  # ID do post, chave primária
    titulo = database.Column(database.String, nullable=False)  # Título do post, obrigatório
    corpo = database.Column(database.Text, nullable=False)  # Corpo do post (conteúdo), obrigatório
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)  # Data de criação, com valor padrão sendo o momento atual
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)  # ID do usuário, chave estrangeira referenciando o modelo `Usuario`

    # O `__repr__` define a representação do objeto Post em formato de string
    def __repr__(self):
        return f"<Post {self.titulo} - {self.id_usuario}>"

