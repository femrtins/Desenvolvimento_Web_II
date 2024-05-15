import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'

#Configurar banco de dados
db = SQLAlchemy(app)
class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=200), nullable=False)
    email = db.Column(db.String(length=200), nullable=False, unique=True)
    senha = db.Column(db.String(length=200), nullable=False)

#Configurar rota quando o servidor é iniciado
@app.route('/') 
def page_home():
    return render_template("home.html")

@app.route('/produtos')
def page_produto():
    pessoas = Pessoa.query.all()
    return render_template("produtos.html", pessoas = pessoas)

@app.route('/login')
def page_login():
    return render_template("login.html")

@app.route('/cadastro')
def page_cadastro():
    return render_template("cadastro.html")

@app.route('/perfil')
def page_perfil():
    return render_template("perfil_usuario.html")


'''
Cadastrar usuário no banco de dados

! mudar a forma de saber se as senhas são iguais para o javascript, para que a página não atualize
! mudar para que primeiro o usuário coloque o e-mail, pressione continuar e seja direcionado para 
outra pagina onde ele precisará inserir as outras informações, para que a página não seja atualizada
e ele perca todos os dados se já existir um email igual no bd.
! mudar para que a senha seja salva com criptografia no banco de dados. OK

'''
@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    senha_confirmacao = request.form['senha_comparacao']

    user = Pessoa.query.filter_by(email=email).first()
    # Se o usuário não é encontrado, ele é redirecionado para a página de cadastro e recebe
    # a mensagem que o endereço de e-mail já exite
    if user:         
        flash('Esse e-mail já existe')
        return redirect("/cadastro")
    
    # Se as senhas não são iguais o usuário é redirecionado para a página de cadastro e recebe
    # a mensagem que as senhas não são iguais
    if senha != senha_confirmacao:
        flash('As senhas não são iguais')
        return redirect("/cadastro")
    
    #Cria um novo usuário e insere no banco de dados
    novoUsuario = Pessoa(nome=nome, email=email, senha=generate_password_hash(senha, method='pbkdf2'))
    db.session.add(novoUsuario)
    db.session.commit()

    return redirect('/login')


'''
Login

! fazer o checkbox de lembrar do usuário funcionar

'''
@app.route('/form-login', methods=['POST'])
def formLogin():
    email = request.form['email']
    senha = request.form['senha']

    # Tem que fazer isso funcionar ainda
    remember = True if request.form.get('remember') else False

    user = Pessoa.query.filter_by(email=email).first()

    # Checa se o usuário já existe
    # Pega a senha dada pelo usuário passa o hash e compara com a senha no bd
    if not user or not check_password_hash(user.senha, senha):
        flash('Erro! Confira seus dados e tente novamente')
        # Se o usuário não existe ou a senha está errada, atualiza a pagina
        return redirect('/login') 

    # Se os anteriores passarem manda o usuário para o seu perfil
    return redirect('/perfil')
