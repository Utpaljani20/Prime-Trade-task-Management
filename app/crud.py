from flask import Blueprint, request, jsonify
from .models import db, Task
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

crud_bp = Blueprint('crud', __name__)

@crud_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_task = Task(title=data['title'], description=data.get('description'), user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg": "Task added!"}), 201

@crud_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    claims = get_jwt()
    if claims.get("role") == 'admin':
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()
    # Yahan status bhi return karna zaroori hai list mein dikhane ke liye
    return jsonify([{"id":t.id, "title":t.title, "description":t.description, "status": t.status} for t in tasks]), 200

@crud_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    task = Task.query.get_or_404(task_id)
    
    if str(task.user_id) != str(user_id) and claims.get("role") != 'admin':
        return jsonify({"msg": "Permission denied"}), 403
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task deleted successfully"}), 200

# SIRF EK BAAR RAKHO ISKO:
@crud_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    task = Task.query.get_or_404(task_id)

    if str(task.user_id) != str(user_id):
        return jsonify({"msg": "Unauthorized"}), 403

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)

    db.session.commit()
    return jsonify({"msg": "Task updated successfully"}), 200