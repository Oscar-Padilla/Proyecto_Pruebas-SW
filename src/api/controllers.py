from flask import Flask, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from api.models import UserModel, ArticleModel, db
import json, re

#USUARIOOOOOOOOOS
user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True, help="Username is required")
user_args.add_argument("email", type=str, required=True, help="Email is required")

userFields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()

        if not args['username'] or args['username'].isspace():
            return {'error': 'Username cannot be empty'}, 400
        if not args['email'] or args['email'].isspace():
            return {'error': 'Email cannot be empty'}, 400

        email = args['email'].strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'error': 'Invalid email format'}, 400

        user = UserModel(username=args["username"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users, 200

class User(Resource):
    @marshal_with(userFields)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        return user, 200

    @marshal_with(userFields)
    def patch(self, user_id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        user.username = args["username"]
        user.email = args["email"]
        db.session.commit()
        return user, 200

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200




#ARTICULOOOOOOOOOS
article_args = reqparse.RequestParser()
article_args.add_argument("user_id", type=int, required=True, help="User ID is required")
article_args.add_argument("title", type=str, required=True, help="Title is required")
article_args.add_argument("description", type=str, required=False, help="Description of the article")

articleFields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "user_id": fields.Integer
}

class Articles(Resource):
    @marshal_with(articleFields)
    def post(self):
        args = article_args.parse_args()

        if not args['title'] or args['title'].isspace():
            return {'error': 'Title cannot be empty'}, 400

        article = ArticleModel(title=args["title"], description=args["description"], user_id=args["user_id"])
        db.session.add(article)
        db.session.commit()
        return article, 201

    @marshal_with(articleFields)
    def get(self):
        articles = ArticleModel.query.all()
        return articles, 200

class Article(Resource):
    @marshal_with(articleFields)
    def get(self, article_id):
        article = ArticleModel.query.filter_by(id=article_id).first()
        if not article:
            return {'message': 'Article not found'}, 404
        return article, 200

    @marshal_with(articleFields)
    def patch(self, article_id):
        args = article_args.parse_args()
        article = ArticleModel.query.filter_by(id=article_id).first()
        if not article:
            return {'message': 'Article not found'}, 404
        article.title = args["title"]
        article.description = args["description"]
        db.session.commit()
        return article, 200

    def delete(self, article_id):
        article = ArticleModel.query.filter_by(id=article_id).first()
        if not article:
            return {'message': 'Article not found'}, 404
        db.session.delete(article)
        db.session.commit()
        return {'message': 'Article deleted'}, 200
