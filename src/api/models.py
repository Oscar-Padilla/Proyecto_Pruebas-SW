from .extensions import db

# Modelo de Usuario
class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Relación con Artículo
    articles = db.relationship('ArticleModel', back_populates='user')

    def __repr__(self):
        return f"<User (username = {self.username}, email = {self.email})>"


# Modelo de Artículo
class ArticleModel(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relación inversa con Usuario
    user = db.relationship('UserModel', back_populates='articles')

    def __repr__(self):
        return f"<Article (title = {self.title}, user = {self.user.username})>"
 
#Modelo de Categorias
class CategoriesModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Category (name = {self.name})>"

#Modelo de relacion muchos a muchos articulos y categorias 
class ArticleCategoriesModel(db.Model):
    __tablename__ = 'article_categories'

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)

    def __repr__(self):
        return f"<ArticleCategory (article_id = {self.article_id}, category_id = {self.category_id})>"

#Modelo calificaciones de articulos
class ArticleRatingModel(db.Model):
    __tablename__ = 'article_ratings'

    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<ArticleRating (article_id = {self.article_id}, user_id = {self.user_id}, rating = {self.rating})>" 