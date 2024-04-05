from flask import jsonify,Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
from pyparsing import wraps
from model import recommend_songs
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
app.config['SECRET_KEY'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
app.config['WTF_CSRF_ENABLED'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    songs = db.relationship('Song', backref='user', lazy='dynamic')

# Song model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('lol')
        print(request)
        print('lol')
        username = request.json["username"]
        password = request.json["password"]

        if User.query.filter_by(username=username).first() is not None:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        song_name = request.form['song_name']
        song_year = int(request.form['song_year'])
        song_list = [{'name': song_name, 'year': song_year}]
        data = pd.read_csv("./input/data.csv")
        recommended_songs = recommend_songs(song_list, data)
        # Store recommended songs in the database
        for song in recommended_songs:
            new_song = Song(name=song['name'], year=song['year'], user_id=current_user.id)
            db.session.add(new_song)
        db.session.commit()
        return render_template('result.html', songs=recommended_songs)
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8000,debug=True)