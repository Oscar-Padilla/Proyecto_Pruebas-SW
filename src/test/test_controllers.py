import pytest
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
#from unittest.mock import MagicMock, patch, Mock
#from api.controllers import Users, User, Articles, Article
from api.models import UserModel, ArticleModel, db


# @pytest.fixture
# def app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['TESTING'] = True
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     yield app
#     with app.app_context():
#         db.drop_all()
    
# @pytest.fixture
# def client(app):
#     return app.test_client()

# def test_users_list(client):
#     response = client.get('/users/')
#     assert response.status_code == 404

# def test_user_get_not_found(client):
#     response = client.get('/users/999')  # Non-existent user ID
#     assert response.status_code == 404

# def test_verify_email(client):
#     mock_users_repository = MagicMock()
#     mock_users_repository.get_all.return_value = {
#             "email": "john@usebouncer.com",
#             "status": "deliverable",
#             "reason": "accepted_email",
#             "domain": {
#                 "name": "usebouncer.com",
#                 "acceptAll": "no",
#                 "disposable": "no",
#                 "free": "no"
#             },
#             "account": {
#                 "role": "no",
#                 "disabled": "no",
#                 "fullMailbox": "no"
#             },
#             "dns": {
#                 "type": "MX",
#                 "record": "aspmx.l.google.com."
#             },
#             "provider": "google.com",
#             "score": 100,
#             "toxic": "unknown"
#             }
#     assert mock_users_repository.get_all.return_value["status"] == "deliverable"
#     assert mock_users_repository.get_all.return_value["reason"] == "accepted_email"

import pytest
from flask import Flask, json
from flask_restful import Api
from api.models import UserModel, ArticleModel, db
from api.controllers import Users, User, Articles, Article

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    api = Api(app)
    api.add_resource(User, '/api/users/<int:user_id>')
    api.add_resource(Users, '/api/users/')
    api.add_resource(Article, '/api/articles/<int:article_id>')
    api.add_resource(Articles, '/api/articles/')
    return app.test_client()

# Test para obtener lista de usuarios
def test_users_list(client):
    response = client.get('/api/users/')
    assert response.status_code == 200

# Test para obtener un usuario por ID
def test_user_get(client, app):
    with app.app_context():
        user = UserModel(id=1, username="test_user", email="test@example.com")
        db.session.add(user)
        db.session.commit()

    response = client.get('/api/users/1')
    assert response.status_code == 200
    assert "test_user" in response.get_data(as_text=True)

# Test para obtener un usuario que no existe
def test_user_get_not_found(client):
    response = client.get('/api/users/999')
    assert response.status_code == 404

# Test para crear un usuario
def test_create_user(client, app):
    user_data = {
        "username": "new_user",
        "email": "new_user@example.com"
    }
    
    response = client.post('/api/users/', json=user_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['username'] == 'new_user'
    assert data['email'] == 'new_user@example.com'

# Test para actualizar un usuario
def test_update_user(client, app):
    with app.app_context():
        user = UserModel(id=1, username="test_user", email="test@example.com")
        db.session.add(user)
        db.session.commit()

    updated_data = {
        "username": "updated_user",
        "email": "updated_user@example.com"
    }

    response = client.patch('/api/users/1', json=updated_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'updated_user'
    assert data['email'] == 'updated_user@example.com'

# Test para eliminar un usuario
def test_delete_user(client, app):
    with app.app_context():
        user = UserModel(id=1, username="test_user", email="test@example.com")
        db.session.add(user)
        db.session.commit()

    response = client.delete('/api/users/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'User deleted'

# Test para crear un artículo
def test_create_article(client, app):
    with app.app_context():
        user_data = {
        "username": "new_user",
        "email": "new_user@example.com"
        }


        user = UserModel(username="john_doe", email="john_doe@example.com")
        db.session.add(user)
        db.session.commit()

        article_data = {
            "title": "New Article",
            "description": "This is a new article.",
            "user_id": user.id
        }

    response = client.post('/api/articles/', json=article_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Article'
    assert data['description'] == 'This is a new article.'
    assert data['user_id'] == user.id

# Test para obtener un artículo
def test_article_get(client, app):
    with app.app_context():
        user = UserModel(username="john_doe", email="john_doe@example.com")
        db.session.add(user)
        db.session.commit()

        article_data = {
            "title": "New Article",
            "description": "This is a new article.",
            "user_id": user.id 
        }

    response0 = client.post('/api/articles/', json=article_data)
    assert response0.status_code == 201 
    data = json.loads(response0.data)
    assert data['title'] == 'New Article'
    assert data['description'] == 'This is a new article.'
    assert data['user_id'] == user.id

    response = client.get(f'/api/articles/{data["id"]}')
    assert response.status_code == 200 


# Test para obtener un artículo que no existe
def test_article_get_not_found(client):
    response = client.get('/api/articles/999')
    assert response.status_code == 404

# Test para eliminar un artículo
def test_delete_article(client, app):
    with app.app_context():
        user = UserModel(username="john_doe", email="john_doe@example.com")
        db.session.add(user)
        db.session.commit()

        article_data = {
            "title": "New Article",
            "description": "This is a new article.",
            "user_id": user.id 
        }

    response0 = client.post('/api/articles/', json=article_data)
    assert response0.status_code == 201 
    data = json.loads(response0.data)
    assert data['title'] == 'New Article'
    assert data['description'] == 'This is a new article.'
    assert data['user_id'] == user.id

    response = client.delete(f'/api/articles/{data["id"]}')
    assert response.status_code == 200 