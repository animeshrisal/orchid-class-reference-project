from flask import Flask, render_template, session, request
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(host="localhost", user="root", passwd="", database="todo")

cursor = db.cursor(buffered=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/posts")
def posts_list():
    pass


@app.route("/posts/<id>/detail")
def posts_detail(id):
    pass


@app.route("/posts/<id>/update")
def posts_update(id):
    pass


@app.route("/posts/<id>/delete")
def posts_delete(id):
    pass



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
