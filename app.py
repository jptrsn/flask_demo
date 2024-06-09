# app.py

from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database with the app
db.init_app(app)

# Create tables within the app context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    # users = [
    #     { 'username': 'Johhny Test', 'email': 'johhnytest@myemailisfake'},
    #     { 'username': 'Andrew Bits', 'email': 'andrew@andybits' }
    # ]
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
