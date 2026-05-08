from flask import Blueprint, request, jsonify
from .models import db, User
from . import bcrypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400
    
    new_user = User(username=data['username'], email=data['email'], 
                    password=data['password'], role=data.get('role', 'user'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Registration successful"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return jsonify(access_token=token, role=user.role), 200
    return jsonify({"msg": "Invalid credentials"}), 401