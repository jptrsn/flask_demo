from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_demo"  # Replace with your MongoDB connection string
mongo = PyMongo(app)

app.secret_key = "your_secret_key"  # Replace with a strong, unique secret key

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("welcome"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/welcome")
def welcome():
    if "logged_in" in session and session["logged_in"]:
        return render_template("welcome.html", username=session["username"])
    else:
        return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        user = mongo.db.users.find_one({"username": username})

        if user:
            return render_template("signup.html", error="Username already exists")
        else:
            mongo.db.users.insert_one({"username": username, "password": hashed_password})
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)