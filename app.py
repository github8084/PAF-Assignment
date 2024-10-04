from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, unset_jwt_cookies
)
from email_validator import validate_email, EmailNotValidError
from datetime import timedelta

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'PAF_jwt_secret_key'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Input validation function start here
def validate_signup_input(data):
    if not data:
        return "Invalid input, JSON data is required.", False
    
    email = data.get('email')
    password = data.get('password')
    
    # Validate email
    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return str(e), False
    
    # Validate password
    if not password or len(password) < 6:
        return "Password must be at least 6 characters long.", False
    
    return None, True

# Validate sign-in input
def validate_signin_input(data):
    if not data:
        return "Invalid input, JSON data is required.", False

    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return "Email and password are required.", False
    
    return None, True

# Input validation function end here

# Initialize DB
def init_db():
    db.create_all()

# Sign-up Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    error_msg, valid = validate_signup_input(data)
    if not valid:
        return jsonify({"msg": error_msg}), 400

    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201

# Sign-in Route
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()

    error_msg, valid = validate_signin_input(data)
    if not valid:
        return jsonify({"msg": error_msg}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

# Refresh Token Route
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200

# Protected Route (requires JWT)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    identity = get_jwt_identity()
    return jsonify(logged_in_as=identity), 200

# Logout Route
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has expired"}), 401

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000,debug=True)