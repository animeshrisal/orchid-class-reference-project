from flask import Flask, render_template, session, request
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(host="localhost", user="root", passwd="", database="todo")

cursor = db.cursor(buffered=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/admin/login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin():
    return render_template("admin.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/posts")
def posts_list():
    return render_template("post_list.html")

@app.route("/posts/create")
def posts_create():
    return render_template("post_create.html")

@app.route("/posts/<id>/detail")
def posts_detail(id):
    return render_template("post_detail.html")


@app.route("/posts/<id>/update")
def posts_update(id):
    return render_template("post_update.html")


@app.route("/posts/<id>/delete")
def posts_delete(id):
        return render_template("post_delete.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
