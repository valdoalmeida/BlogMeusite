# from main import app
# from meusite import database
#
# with app.app_context():
#    database.create_all()

# CRIANDO USUARIO NO BANCO DE DADOS

# with app.app_context():
#     usuario = Usuario(username='Valdo', email='valdo@gmail.com', senha='123456')
#     usuario2 = Usuario(username='Beth', email='beth@gmail.com', senha='123456')
#     database.session.add(usuario2)
#     database.session.commit()

# with app.app_context():
#     meus_usuarios = Usuario.query.all()
#     print(meus_usuarios)
#
# for nome in meus_usuarios:
#     print(nome.id, nome.username, nome.email, nome.senha)


# CRIANDO POST NO BANCO DE DADOS

# with app.app_context():
#     meu_post =  Post(id_usuario=1, titulo='meu primeiro post', corpo='aprendendo python')
#     database.session.add(meu_post)
#     database.session.commit()

# with app.app_context():
#      meu_post = Post.query.first()
#      print("O Autor {} criou seu primeiro Post com o titulo \n{} e com a seguinte descrição \n{}".format(meu_post.autor_post.username, meu_post.titulo, meu_post.corpo))


#DELETAR TUDO QUE TEM NO BANCO E CRIAR DE NOVO
#
# with app.app_context():
#     database.drop_all()
#     database.create_all()