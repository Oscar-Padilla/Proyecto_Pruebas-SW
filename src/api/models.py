from .extensions import db

# class UserModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def _repr_(self):
#         return f"User (username = {self.username}, email: {self.email})>"

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
 