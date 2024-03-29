# services/users/project/api/users.py

from flask import Blueprint, jsonify, request, render_template
from project.api.models import User
from project import db
from sqlalchemy import exc


users_blueprint = Blueprint('users', __name__, template_folder='./templates')


#  area de servicios

@users_blueprint.route('/orders/ping', methods=['GET'])
def ping_pong():
    return jsonify({
       'status': 'success',
       'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                username=username,
                email=email,
                password=password,
            ))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Disculpe. Este email ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Obtener detalles de ususario unico"""
    response_object = {
        'status': 'fail',
        'message': 'user not exists'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                    }
            }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Obteniendo todos los usuarios"""
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)
