from FlaskBlogApp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)    
    name = db.Column(db.String(15), nullable=True)
    surname = db.Column(db.String(15), nullable=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    recommender = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(36), nullable=False)
    profile_image = db.Column(db.String(30), default='default_profile_image.jpg')
    contact_username = db.Column(db.String(15), unique=False, nullable=False)
    articles = db.relationship('Article', backref='author', lazy=True)
    offers = db.relationship('Offer', backref='author', lazy=True)    

    def __repr__(self):
        return f"{self.username}: {self.email}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'email': self.email,
            'recommender': self.recommender,
            'profile_image': self.profile_image,
            'contact_username': self.contact_username
        }


class Article(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    article_title = db.Column(db.String(50), nullable=False)
    article_body = db.Column(db.Text(), nullable=False)
    article_image = db.Column(db.String(30), nullable=False, default='default_article_image.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __searchable__ = ['article_title', 'article_body']

    def __repr__(self):
        return f"{self.date_created}: {self.article_title}"
    def to_dict(self):
        return {
            'id': self.id,
            'article_title': self.article_title,
            'article_body': self.article_body,
            'article_image': self.article_image
        }


class Offer(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    offer_title = db.Column(db.String(50), nullable=False)
    offer_type = db.Column(db.String(50), nullable=False)
    offer_location = db.Column(db.String(50), nullable=False)
    offer_body = db.Column(db.Text(), nullable=False)
    offer_image = db.Column(db.String(30), nullable=False, default='default_offer_image.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    views_count = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'offer_title': self.offer_title,
            'offer_type': self.offer_type,
            'offer_location': self.offer_location,
            'offer_body': self.offer_body,
            'offer_image': self.offer_image
        }


class Opinion(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    sender = db.Column(db.String(150), unique=True, nullable=False)
    recipient = db.Column(db.String(150), unique=True, nullable=False)
    option = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    


    def __repr__(self):
        return f"{self.date_created}: {self.offer_title}"