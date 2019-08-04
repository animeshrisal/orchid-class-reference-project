from flask import Flask, render_template, session, request, flash, redirect
import mysql.connector
import os
import hashlib

app = Flask(__name__)

db = mysql.connector.connect(host="localhost", user="root", passwd="", database="todo")

cursor = db.cursor(buffered=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    errors = {}
    if request.method == "POST":
        try:
            name = request.form['name']
            password = request.form['password']
            
            hash_obj = hashlib.sha1(password.encode("utf8"))
            hex_dig = hash_obj.hexdigest()

            if name == "":
                errors['name'] = "Name is empty"

            if password == "":
                errors['password'] = "Password is empty"

            if len(errors) is not 0:
                return render_template("register.html", errors=errors)

            cursor.execute("SELECT * from user where name = %s and hash = %s", (name,hex_dig))

            if cursor.rowcount == 0:
                errors['user'] = "User does not exist"
                return render_template("login.html", errors = errors)
            else:
                data = cursor.fetchone()
                session['user_id'] = data[0]
                session['user_name'] = data[1]
                return redirect("/profile")
            
        except Exception as e:
            flash(e)
            return render_template("error.html")

    return render_template("login.html", errors = errors)

@app.route("/register", methods = ['POST', 'GET'])
def register():
    errors = {}   
    if request.method == "POST":
        try:
            name = request.form['name']
            password = request.form['password']
            
            if name == "":
                errors['name'] = "Name is empty"

            if password == "":
                errors['password'] = "Password is empty"


            if len(errors) is not 0:
                return render_template("register.html", errors=errors)
            
            cursor.execute("SELECT * from user where name = %s", (name,))
            
            if cursor.rowcount is not 0:
                errors['exists'] = "User already exists"
                return render_template("register.html", errors=errors)

            hash_obj = hashlib.sha1(password.encode("utf8"))
            hex_dig = hash_obj.hexdigest()

            cursor.execute("INSERT INTO user(name, hash, isAdmin) values(%s, %s, 0)", (name, hex_dig))
            db.commit()
            
            return redirect('/login')
            
        except Exception as e:
            flash(e)
            return render_template("error.html")
        
    return render_template("register.html", errors=errors)

@app.route("/admin/login")
def admin_login():
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin():
    return render_template("admin.html")

@app.route("/profile")
def profile():
    cursor.execute("SELECT * from post where userId = %s", (session['user_id'],))
    data = cursor.fetchall()
    return render_template("profile.html", todo=data)

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
