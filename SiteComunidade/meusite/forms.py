from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from meusite.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    """
    Formulário para criar uma nova conta de usuário.
    Valida o e-mail, a senha e confirma se a senha foi digitada corretamente.
    """
    username = StringField("Nome do Usuário", validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo("senha")])
    submit_btn_criarConta = SubmitField('Criar Conta')

    def validate_email(self, email):
        """
        Valida o e-mail fornecido para garantir que não seja duplicado.
        """
        usuario_criar_conta = Usuario.query.filter_by(email=email.data).first()
        if usuario_criar_conta:
            raise ValidationError('E-mail já cadastrado, use novo e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    """
    Formulário para o login do usuário.
    Valida o e-mail e a senha inseridos, e permite ao usuário manter os dados de login.
    """
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField("Lembrar dados de acesso")
    submit_btn_login = SubmitField('Acessar Conta')


class FormEditarPerfil(FlaskForm):
    """
    Formulário para editar as informações do perfil do usuário.
    Permite editar o nome de usuário, e-mail, foto de perfil e cursos.
    """
    username = StringField("Nome do Usuário", validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto do Perfil', validators=[FileAllowed(['jpg', 'png'])])

    # Campos de cursos
    curso_excel = BooleanField("Curso Excel")
    curso_vba = BooleanField("Curso VBA")
    curso_powerbi = BooleanField("Curso Power BI")
    curso_python = BooleanField("Curso Python")
    curso_word = BooleanField("Curso Word")
    curso_sql = BooleanField("Curso SQL")

    submit_btn_editarPerfil = SubmitField('Aplicar')

    def validate_email(self, email):
        """
        Valida o e-mail para garantir que o novo e-mail não seja o mesmo de outro usuário.
        Se o usuário tentar editar para um e-mail que já existe, a validação falha.
        """
        if current_user.email != email.data:  # Verifica se o e-mail está sendo alterado
            usuario_criar_conta = Usuario.query.filter_by(email=email.data).first()
            if usuario_criar_conta:
                raise ValidationError('E-mail já existe com esse E-mail, cadastre outro E-mail')


class FormCriarPost(FlaskForm):
    """
    Formulário para criar um novo post.
    Permite o título e o corpo do post.
    """
    titulo = StringField("Título do Post", validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui !', validators=[DataRequired()])
    btn_post = SubmitField('Criar Post')
