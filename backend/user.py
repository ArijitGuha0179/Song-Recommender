from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

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

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user is None:
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello, {current_user.username}!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)