"""Diario educativo con SQLite, usuarios y entradas privadas."""
import os
import secrets
from flask import Flask, render_template, request, redirect, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DIARY_DATABASE_URI', 'sqlite:///diary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_email = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_email'] = email
            return redirect('/index')
        error = 'Nombre de usuario o contraseña incorrectos'
    return render_template('auth.html', title='Entrar al diario', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if '@' not in email or len(password) < 8:
            error = 'Introduce un correo y una contraseña de al menos 8 caracteres.'
        elif User.query.filter_by(email=email).first():
            error = 'Ese correo ya está registrado.'
        else:
            db.session.add(User(email=email, password=generate_password_hash(password)))
            db.session.commit()
            return redirect('/')
    return render_template('auth.html', title='Crear cuenta', error=error)

@app.route('/index')
def index():
    email = session.get('user_email')
    if not email:
        return redirect('/')
    cards = Card.query.filter_by(user_email=email).order_by(Card.id).all()
    return render_template('index.html', cards=cards)

@app.route('/create')
def create():
    if not session.get('user_email'):
        return redirect('/')
    return render_template('create.html')

@app.route('/form_create', methods=['POST'])
def form_create():
    email = session.get('user_email')
    if not email:
        return redirect('/')
    fields = {key: request.form.get(key, '').strip() for key in ('title', 'subtitle', 'text')}
    if not all(fields.values()):
        abort(400)
    db.session.add(Card(**fields, user_email=email))
    db.session.commit()
    return redirect('/index')

@app.route('/card/<int:id>')
def card(id):
    email = session.get('user_email')
    if not email:
        return redirect('/')
    card = Card.query.filter_by(id=id, user_email=email).first_or_404()
    return render_template('card.html', card=card)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
