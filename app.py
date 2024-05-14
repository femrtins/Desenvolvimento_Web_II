import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=200), nullable=False)
    email = db.Column(db.String(length=200), nullable=False, unique=True)
    senha = db.Column(db.String(length=200), nullable=False)


@app.route('/') #Configurar rota quando o servidor é iniciado
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

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    senha_confirmacao = request.form['senha_comparacao']

    user = Pessoa.query.filter_by(email=email).first()
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect("/cadastro")
    
    if senha != senha_confirmacao:
        flash('Senhas não são iguais')
        return redirect("/cadastro")

    
    novoUsuario = Pessoa(nome=nome, email=email, senha=senha)
    db.session.add(novoUsuario)
    db.session.commit()

    return render_template('cadastro.html', nome=novoUsuario.nome, email=novoUsuario.email, senha=novoUsuario.senha)