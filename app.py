import datetime, jwt, os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Testing values
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:password123@db:5432/db'
app.config['SECRET_KEY'] = 'secret-key-test-123'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), default='Adult')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_pw, user_type=data.get('user_type', 'Adult'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User creat"}), 201

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    user = User.query.filter_by(username=auth['username']).first()
    if not user or not check_password_hash(user.password, auth['password']):
        return jsonify({"message": "Invalid"}), 401
    
    token = jwt.encode({
        'iss': 'auth-service',
        'user_id': user.id,
        'user_type': user.user_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

if __name__ == '__main__':
    #with app.app_context():
    #    db.create_all()
    app.run(host='0.0.0.0', port=5000)
