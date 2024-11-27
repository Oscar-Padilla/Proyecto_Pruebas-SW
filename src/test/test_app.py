# import pytest
# import unittest
# from flask import Flask, json
# from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy
# from unittest.mock import MagicMock, patch, Mock
# from api.controllers import Users, User
# from api.models import UserModel, db

# @patch.object(User, 'get')
# def test_user_get(mock_get):
#     mock_user = Mock()
#     mock_user.id = 1
#     mock_user.username = 'XXXX'
#     mock_user.email = 'XXXXXXXXXXXX'
#     mock_get.return_value = mock_user

#     result = User.get()
#     assert result == mock_user
#     assert result.id == 1
#     assert result.username == 'XXXX'
#     assert result.email == 'XXXXXXXXXXXX'
#     mock_get.assert_called_once_with()

# class TestUser(unittest.TestCase):
#     def setUp(self):
#        self.app = Flask(__name__)
#        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#        self.api = Api(self.app)
#        self.api.add_resource(User, '/users/<int:user_id>')
#        self.client = self.app.test_client()
#        #set up the aplication context
#        self.app_context = self.app.app_context()
#        self.app_context.push()
#        #initialize the database
#        db.init_app(self.app)
#        db.create_all()
    
#     @patch('api.controllers.UserModel.query')
#     def test_get(self, mock_query):
#         mock_query.filter_by.return_value.first.return_value = UserModel(id=1, username='test', email='test@test.com')

#         response = self.client.get('/users/1')

#         self.assertEqual(response.status_code, 200)
#         self.assertIn('test', response.get_data(as_text=True))
#         self.assertIn('test@test.com', response.get_data(as_text=True))

import pytest
from flask import Flask, json
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from api.controllers import Users, User, Articles, Article
from api.models import UserModel, ArticleModel, db


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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

# ------------------------------------------
# Pruebas para las rutas de usuarios
# ------------------------------------------

def test_get_user(client, app):
    with app.app_context():
        user = UserModel(id=1, username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()

    response = client.get('/api/users/1')

    assert response.status_code == 200
    assert 'test_user' in response.get_data(as_text=True)
    assert 'test@example.com' in response.get_data(as_text=True)

def test_get_user_not_found(client):
    response = client.get('/api/users/999')

    assert response.status_code == 404

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

# ------------------------------------------
# Pruebas para las rutas de artículos
# ------------------------------------------

def test_create_article(client, app):
    with app.app_context():
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

def test_get_article(client, app):
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

def test_get_article_not_found(client):
    response = client.get('/api/articles/999')

    assert response.status_code == 404

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