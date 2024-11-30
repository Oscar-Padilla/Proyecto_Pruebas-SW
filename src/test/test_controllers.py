import pytest
from flask import Flask, json
from flask_restful import Api
from api.models import UserModel, ArticleModel, CategoriesModel, ArticleCategoriesModel, ArticleRatingModel, db
from api.controllers import Users, User, Articles, Article, Categories, ArticleCategories, ArticleRatings

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
    api.add_resource(Categories, '/api/categories/')
    api.add_resource(ArticleCategories, '/api/article-categories/')
    api.add_resource(ArticleRatings, '/api/article-ratings/')
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

# Test para crear una categoría
def test_create_category(client, app):
    category_data = {
        "name": "Technology"
    }

    response = client.post('/api/categories/', json=category_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'Technology'

# Test para obtener lista de categorías
def test_get_categories(client):
    response = client.get('/api/categories/')
    assert response.status_code == 200

# Test para crear relación entre artículo y categoría
def test_create_article_category_relation(client, app):
    with app.app_context():
        user = UserModel(username="john_doe", email="john_doe@example.com")
        db.session.add(user)
        db.session.commit()

        article = ArticleModel(title="New Article", description="This is a new article.", user_id=user.id)
        category = CategoriesModel(name="Technology")
        db.session.add(article)
        db.session.add(category)
        db.session.commit()

        relation_data = {
            "article_id": article.id,
            "category_id": category.id
        }

    response = client.post('/api/article-categories/', json=relation_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Relation created successfully'

# Test para obtener todas las relaciones entre artículos y categorías
def test_get_article_categories(client):
    response = client.get('/api/article-categories/')
    assert response.status_code == 200

# Test para calificar un artículo
def test_create_article_rating(client, app):
    with app.app_context():
        user = UserModel(username="john_doe", email="john_doe@example.com")
        db.session.add(user)
        db.session.commit()

        article = ArticleModel(title="New Article", description="This is a new article.", user_id=user.id)
        db.session.add(article)
        db.session.commit()

        rating_data = {
            "article_id": article.id,
            "user_id": user.id,
            "rating": 4
        }

    response = client.post('/api/article-ratings/', json=rating_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['rating'] == 4

# Test para obtener todas las calificaciones de artículos
def test_get_article_ratings(client):
    response = client.get('/api/article-ratings/')
    assert response.status_code == 200

#Test de psoibles errores

# Test para error de email vacío
def test_create_user_invalid_email(client):
    user_data = {
        "username": "new_user",
        "email": ""  # Email vacío
    }
    response = client.post('/api/users/', json=user_data)
    assert response.status_code == 400

# Test para error de formato de email inválido
def test_create_user_invalid_email_format(client):
    user_data = {
        "username": "new_user",
        "email": "invalid_email"  # Email con formato incorrecto
    }
    response = client.post('/api/users/', json=user_data)
    assert response.status_code == 400

# Test para error de nombre de usuario vacío
def test_create_user_invalid_username(client):
    user_data = {
        "username": "",  # Nombre de usuario vacío
        "email": "new_user@example.com"
    }
    response = client.post('/api/users/', json=user_data)
    assert response.status_code == 400

# Tests de Artículos

# Test para error de título vacío
def test_create_article_invalid_title(client):
    article_data = {
        "title": "",  # Título vacío
        "description": "This is a new article.",
        "user_id": 1
    }
    response = client.post('/api/articles/', json=article_data)
    assert response.status_code == 400

# Test para crear artículo con usuario no existente
def test_create_article_invalid_user(client):
    article_data = {
        "title": "New Article",
        "description": "This is a new article.",
        "user_id": 9999  # Usuario no existente
    }
    response = client.post('/api/articles/', json=article_data)
    assert response.status_code == 404

# Tests de Calificación de Artículos

# Test para error de calificación fuera de rango (menor que 1)
def test_create_rating_invalid_low(client):
    rating_data = {
        "article_id": 1,
        "user_id": 1,
        "rating": 0  # Calificación fuera de rango
    }
    response = client.post('/api/article-ratings/', json=rating_data)
    assert response.status_code == 400

# Test para error de calificación fuera de rango (mayor que 5)
def test_create_rating_invalid_high(client):
    rating_data = {
        "article_id": 1,
        "user_id": 1,
        "rating": 6  # Calificación fuera de rango
    }
    response = client.post('/api/article-ratings/', json=rating_data)
    assert response.status_code == 400

# Tests de Categorías

# Test para crear categoría sin nombre
def test_create_category_invalid_name(client):
    category_data = {
        "name": ""  # Nombre vacío
    }
    response = client.post('/api/categories/', json=category_data)
    assert response.status_code == 400

# Test para crear relación artículo-categoría sin IDs válidos
def test_create_article_category_invalid_ids(client):
    relation_data = {
        "article_id": 9999,  # Artículo no existente
        "category_id": 9999   # Categoría no existente
    }
    response = client.post('/api/article-categories/', json=relation_data)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Article ID not found'
    #assert data['error'] == 'Category ID not found'

# Test para crear relación artículo-categoría con datos válidos
def test_create_article_category_valid(client, app):
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
        article_id = json.loads(response.data)["id"]

        category_data = {
            "name": "Tech"
        }
        response = client.post('/api/categories/', json=category_data)
        assert response.status_code == 201
        category_id = json.loads(response.data)["id"]

        relation_data = {
            "article_id": article_id,
            "category_id": category_id
        }
        response = client.post('/api/article-categories/', json=relation_data)
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Relation created successfully'

