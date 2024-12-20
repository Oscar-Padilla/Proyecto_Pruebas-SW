from flask import Flask
from flask_restful import Api
from api.controllers import (
    Users, User, Articles, Article, Categories, ArticleCategories, ArticleRatings
)
from api.extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbProyecto.db'
db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

#APIS USUARIOS
api.add_resource(Users, "/api/users/")
api.add_resource(User, "/api/users/<int:user_id>")

#APIS ARTICULOS
api.add_resource(Articles, "/api/articles/")
api.add_resource(Article, "/api/articles/<int:article_id>")

# APIS CATEGORIAS
api.add_resource(Categories, "/api/categories/")

# APIS RELACIÓN ARTÍCULO-CATEGORÍA
api.add_resource(ArticleCategories, "/api/article-categories/")

# APIS CALIFICACIONES DE ARTÍCULOS
api.add_resource(ArticleRatings, "/api/article-ratings/")

@app.route('/')
def hello():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)
