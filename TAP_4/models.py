from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    def __repr__(self):
        return f'<User {self.username}'