from flask import render_template, redirect, url_for, request, flash, abort
from meusite import app, database, bcrypt
from meusite.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from meusite.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image



# ROTA PRINCIPAL - Página inicial do site
@app.route('/')
def meuSite():
    """
    Rota obrigatória que renderiza a página inicial do site (home.html).
    """
    post = Post.query.order_by(Post.id.desc())

    return render_template('home.html', post=post)


# ROTA PARA VISUALIZAR OS USUÁRIOS
@app.route('/usuarios')
@login_required
def usuario():
    """
    Rota que lista todos os usuários cadastrados no sistema.
    Requer que o usuário esteja logado para acessar.
    """
    lista_usuarios = Usuario.query.all()  # Consulta todos os usuários no banco de dados
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


# ROTA PARA LOGIN E CRIAÇÃO DE CONTA
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para login do usuário e criação de uma nova conta.
    O usuário pode logar ou criar uma nova conta na mesma página.
    """
    form_login = FormLogin()  # Formulário para login
    form_criarConta = FormCriarConta()  # Formulário para criar uma nova conta

    # Verifica se o formulário de login foi enviado e válido
    if form_login.validate_on_submit() and 'submit_btn_login' in request.form:
        usuario_login = Usuario.query.filter_by(email=form_login.email.data).first()

        # Verifica se o email existe e a senha é válida
        if usuario_login and bcrypt.check_password_hash(usuario_login.senha, form_login.senha.data):
            login_user(usuario_login, remember=form_login.lembrar_dados.data)
            flash(f"Login efetuado com sucesso para {form_login.email.data}", 'alert-success h6 text-center')
            param_next = request.args.get('next')  # Redireciona após o login, caso haja uma página específica
            return redirect(param_next) if param_next else redirect(url_for('meuSite'))
        else:
            flash("Falha no login, Usuário ou Senha inválidos", 'alert-danger h6 text-center')

    # Se o formulário de criar conta for válido, cria um novo usuário
    if form_criarConta.validate_on_submit() and 'submit_btn_criarConta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarConta.senha.data).decode('utf-8')
        usuario_criar_conta = Usuario(username=form_criarConta.username.data, email=form_criarConta.email.data,
                                      senha=senha_cript)
        database.session.add(usuario_criar_conta)
        database.session.commit()
        flash(f'Conta criada com sucesso para o E-mail {form_criarConta.email.data}', 'alert-success h6')
        return redirect(url_for('meuSite'))

    return render_template('login.html', form_login=form_login, form_criarConta=form_criarConta)


# ROTA DE LOGOUT
@app.route('/sair')
@login_required
def sair():
    """
    Rota para efetuar logout do usuário.
    """
    logout_user()  # Finaliza a sessão do usuário
    flash("Logout efetuado com sucesso", 'alert-primary h6 text-center')
    return redirect(url_for('meuSite'))


# ROTA PARA EXIBIR O PERFIL DO USUÁRIO
@app.route('/perfil')
@login_required
def perfil():
    """
    Rota para exibir o perfil do usuário logado.
    Mostra a foto de perfil e outras informações.
    """
    img_perfil = url_for('static', filename=f'img_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', img_perfil=img_perfil)





# ROTA PARA CRIAR UM NOVO POST
@app.route('/post/criar', methods=['GET', 'POST'])  # Define a URL da rota e os métodos HTTP permitidos (GET e POST)
@login_required  # Garante que apenas usuários logados possam acessar essa rota
def criar_post():
    """
    Esta rota permite que um usuário crie um novo post.
    Apenas usuários logados podem acessar essa funcionalidade.
    """

    # Cria uma instância do formulário para criação de post
    form = FormCriarPost()

    # Verifica se o formulário foi submetido corretamente e validado
    if form.validate_on_submit():
        # Cria um novo post com os dados do formulário
        post = Post(
            titulo=form.titulo.data,  # Obtém o título do formulário
            corpo=form.corpo.data,  # Obtém o conteúdo do post
            autor_post=current_user  # Associa o post ao usuário atualmente logado
        )

        # Adiciona o post ao banco de dados e confirma a transação
        database.session.add(post)
        database.session.commit()

        # Exibe uma mensagem de sucesso para o usuário
        flash('Post criado com sucesso!', 'alert-success h6')

        # Redireciona o usuário para a página inicial após criar o post
        return redirect(url_for('meuSite'))

    # Se o formulário não for submetido ou houver erro, renderiza a página de criação do post
    return render_template('criar_post.html', form=form)






# Função para salvar a imagem de perfil do usuário
def salvar_imagem(imagem):
    """
    Esta função salva a imagem de perfil enviada pelo usuário.
    A imagem é renomeada para evitar duplicatas, redimensionada para 400x400 pixels
    e salva na pasta 'static/img_perfil'.
    """

    # Gera um código aleatório em hexadecimal para evitar nomes de arquivos repetidos
    codigo = secrets.token_hex(8)

    # Separa o nome e a extensão original da imagem (ex: "foto.jpg" -> nome="foto", extensão=".jpg")
    nome, extensao = os.path.splitext(imagem.filename)

    # Cria um novo nome de arquivo concatenando o nome original, o código gerado e a extensão original
    nome_arquivo = nome + codigo + extensao

    # Define o caminho completo onde a imagem será salva
    caminho_completo = os.path.join(app.root_path, 'static/img_perfil', nome_arquivo)

    # Define o tamanho desejado para a imagem (400x400 pixels)
    tamanho = (400, 400)

    # Abre a imagem, redimensiona e mantém as proporções
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    # Salva a imagem redimensionada no caminho especificado
    imagem_reduzida.save(caminho_completo)

    # Retorna o nome do arquivo salvo para ser armazenado no banco de dados
    return nome_arquivo






# Função para atualizar os cursos selecionados pelo usuário
def atualizar_cursos(form):
    """
    Coleta os cursos que o usuário marcou no formulário e retorna como uma única string.
    Cada curso será separado por ponto e vírgula (;).
    """
    lista_cursos = []  # Lista para armazenar os cursos selecionados

    # Percorre todos os campos do formulário
    for campo in form:
        # Verifica se o campo faz parte dos cursos e se foi marcado pelo usuário
        if 'curso' in campo.name and campo.data:
            lista_cursos.append(campo.label.text)  # Adiciona o nome do curso à lista

    # Retorna os cursos como uma string separada por ponto e vírgula
    return ';'.join(lista_cursos)






# Rota para editar o perfil do usuário
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required  # Garante que apenas usuários logados possam acessar essa rota
def editar_perfil():
    """
    Permite que o usuário edite suas informações de perfil, como:
    - Nome de usuário
    - E-mail
    - Foto de perfil
    - Cursos cadastrados
    """
    form = FormEditarPerfil()  # Cria uma instância do formulário de edição de perfil

    # Se o formulário foi enviado corretamente (POST)
    if form.validate_on_submit():
        # Atualiza os dados do usuário com os valores do formulário
        current_user.email = form.email.data
        current_user.username = form.username.data

        # Se o usuário enviou uma nova foto de perfil, salva a imagem
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)  # Salva a nova imagem no sistema
            current_user.foto_perfil = nome_imagem  # Atualiza o caminho da imagem no banco de dados

        # Atualiza os cursos selecionados pelo usuário
        current_user.cursos = atualizar_cursos(form)

        # Salva todas as alterações no banco de dados
        database.session.commit()

        # Exibe uma mensagem de sucesso na tela
        flash("Perfil atualizado com sucesso", 'alert-primary h6 text-center')

        # Redireciona o usuário de volta para a página do perfil
        return redirect(url_for('perfil'))

    # Se a requisição for GET, pré-preenche o formulário com os dados atuais do usuário
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    # Obtém o caminho da imagem de perfil do usuário para exibição na página
    img_perfil = url_for('static', filename=f'img_perfil/{current_user.foto_perfil}')

    # Renderiza a página de edição de perfil com o formulário preenchido
    return render_template('editar_perfil.html', img_perfil=img_perfil, form=form)







# Rota para visualizar e editar um post existente
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required  # Garante que apenas usuários logados possam acessar essa rota
def exibir_post(post_id):
    """
    Rota que exibe um post específico e permite a edição caso o usuário seja o autor.
    """
    post = Post.query.get(post_id)  # Busca o post no banco de dados pelo ID

    # Verifica se o usuário atual é o autor do post
    if current_user == post.autor_post:
        form = FormCriarPost()  # Instancia o formulário para edição do post

        # Se a requisição for GET, preenche o formulário com os dados atuais do post
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo

        # Se a requisição for POST e os dados forem válidos, atualiza o post
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()  # Salva as alterações no banco de dados
            flash('Post atualizado com sucesso', 'alert-success')  # Mensagem de sucesso
            return redirect(url_for('meuSite'))  # Redireciona para a página inicial

    else:
        form = None  # Usuários que não são autores não podem editar o post

    # Renderiza a página do post com o formulário (caso o usuário possa editar)
    return render_template('post.html', form=form, post=post)







# Rota para excluir um post, identificada pelo 'post_id'
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
def excluir_post(post_id):
    # Recupera o post do banco de dados com base no 'post_id'
    post = Post.query.get(post_id)

    # Verifica se o usuário atual é o autor do post
    if current_user == post.autor_post:
        # Se o usuário for o autor, exclui o post do banco de dados
        database.session.delete(post)
        database.session.commit()

        # Exibe uma mensagem de sucesso
        flash("Post excluído com sucesso", 'alert-danger')

        # Redireciona o usuário para a página principal do site
        return redirect(url_for('meuSite'))
    else:
        # Se o usuário não for o autor do post, aborta a ação com erro 403 (sem permissão)
        abort(403)

