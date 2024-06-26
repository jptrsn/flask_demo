# app.py

from flask import Flask, render_template, request, redirect, url_for, jsonify
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

@app.route('/find_user', methods=['GET', 'POST'])
def find_user():
    user = None
    if request.method == 'POST':
        username = request.form['username']
        # Search for the user in the database
        user = User.query.filter_by(username=username).first()
        return render_template('find_user.html', user=user)
    return render_template('find_user_form.html')

@app.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
