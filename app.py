from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from database import db
from models import User, Note

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Replace with your secret key

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

# Authentication routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('register'))
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', notes=notes)

# CRUD routes for notes
@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('notes'))
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

@app.route('/note/<int:id>', methods=['GET'])
@login_required
def note_detail(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You do not have permission to view this note')
        return redirect(url_for('notes'))
    return render_template('note_detail.html', note=note)

@app.route('/note/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note')
        return redirect(url_for('notes'))
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect(url_for('notes'))
    return render_template('note_form.html', note=note)

@app.route('/note/<int:id>/delete', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note')
        return redirect(url_for('notes'))
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes'))

if __name__ == '__main__':
    app.run(debug=True)
