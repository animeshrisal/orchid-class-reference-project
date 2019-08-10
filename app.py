from flask import Flask, render_template, session, request, flash, redirect
import mysql.connector
import os
import hashlib

app = Flask(__name__)

db = mysql.connector.connect(host="localhost", user="root", passwd="", database="todo")

cursor = db.cursor(buffered=True)

def check_authentication():
    if session['user_id']:
        return True
    else:
        return False
        

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():

    #The error variable is a dictionary that holds the values when an error occurs. 
    #Since the page is loading for the first time there are no errors so its empty
    #The code is the same for the other functions as well

    errors = {}
    if request.method == "POST":
        try:
            name = request.form['name']
            password = request.form['password']
            
            hash_obj = hashlib.sha1(password.encode("utf8"))
            hex_dig = hash_obj.hexdigest()

            #If the names or password fields are empty it will create a dictionary that holds the error message
            #You can create your own error messages such as password field not being long enough
            if name == "":
                errors['name'] = "Name is empty"

            if password == "":
                errors['password'] = "Password is empty"

            #The logic checks how many errors are present in the error dictionary. If 0 that means no error, but if its more than 0 that means some error has occured
            #If the error has occured then it will render the template along with the error. Any code below it will not execute
            if len(errors) is not 0:
                return render_template("register.html", errors=errors)

            cursor.execute("SELECT * from user where name = %s and hash = %s", (name,hex_dig))

            #Here it checks if the user exists or not
            if cursor.rowcount == 0:
                errors['user'] = "User does not exist"
                return render_template("login.html", errors = errors)
            else:
                data = cursor.fetchone()
                session['user_id'] = data[0]
                session['user_name'] = data[1]
                return redirect("/profile")
            
        except Exception as e:
            #If any error occurs that hasn't been handled then it will render an error page
            #The flash function will show you in the console what error has occured
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

            #When registering a user, they will be a customer and not an admin so the value of isAdmin is always set to 0
            cursor.execute("INSERT INTO user(name, hash, isAdmin) values(%s, %s, 0)", (name, hex_dig))
            db.commit()
            
            return redirect('/login')
            
        except Exception as e:
            flash(e)
            return render_template("error.html")
        
    return render_template("register.html", errors=errors)

@app.route("/admin/login", methods = ["POST", "GET"])
def admin_login():
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

            #Here the query also checks if the user is an admin or not
            cursor.execute("SELECT * from user where name = %s and hash = %s and isAdmin = 1", (name,hex_dig))

            if cursor.rowcount == 0:
                errors['user'] = "Admin does not exist"
                return render_template("admin_login.html", errors = errors)
            else:
                data = cursor.fetchone()
                session['user_id'] = data[0]
                session['user_name'] = data[1]
                session['is_admin'] = True
                return redirect("/admin/dashboard")
            
        except Exception as e:
            flash(e)
            return render_template("error.html")

    return render_template("admin_login.html", errors = errors)


@app.route("/admin/dashboard")
def admin():
    #Check if the user is an admin or not. If not then redirect them to the login page
    if 'is_admin' not in session.keys():
        return redirect('/admin/login')

    # Here it returns all the user that aren't an admin
    cursor.execute("SELECT * from user where isAdmin = 0")
    data = cursor.fetchall()
    return render_template("admin.html", users = data)

    
@app.route("/admin/<id>/delete", methods = ["GET", "POST"])
def admin_delete(id):
    if request.method == "POST":
        cursor.execute("DELETE from user where id = %s", (id,))
        db.commit()
        return redirect("/admin/dashboard")
    
    return render_template("admin_delete.html", user_id = id) 


@app.route("/profile")
def profile():
    
    if 'user_id' not in session.keys():
        return redirect('/login')

    cursor.execute("SELECT * from post where userId = %s", (session['user_id'],))
    data = cursor.fetchall()
    return render_template("profile.html", todo=data)

@app.route("/posts")
def posts_list():
    return render_template("post_list.html")

@app.route("/posts/create", methods=["POST", "GET"])
def posts_create():
    if 'user_id' not in session.keys():
        return redirect('/login')

    errors = {}

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        if title == "":
            errors['title'] = "Title is empty"

        if description == "":
            errors['description'] = "Description is empty"

        if len(errors) is not 0:
            return render_template("/posts/post_create.html", errors=errors)
        
        cursor.execute(
            "INSERT into post(title, description, userId) values(%s, %s, %s)",
            (title, description, session["user_id"]),
        )
        db.commit()
        return redirect("/profile")

    return render_template("/posts/post_create.html", errors = errors)


@app.route("/posts/<id>/detail")
def posts_detail(id):
    if 'user_id' not in session.keys():
        return redirect('/login')

    cursor.execute("SELECT * from post where id = %s", (id,))
    data = cursor.fetchone()
    return render_template("posts/post_detail.html", todo=data)


@app.route("/posts/<id>/update", methods=["POST", "GET"])
def posts_update(id):
    if 'user_id' not in session.keys():
        return redirect('/login')

    cursor.execute("SELECT * from post where id = %s", (id,))
    data = cursor.fetchone()
    errors = {}
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        if title == "":
            errors['title'] = "Enter a valid title"

        if description == "":
            errors['description'] = "Enter a valid description"

        if len(errors) is not 0:
            return render_template("/posts/post_update.html", errors=errors, form_data=data)

        cursor.execute(
            "update post set title = %s, description = %s where id = %s",
            (title, description, id),
        )
        db.commit()
        return redirect("/profile")

    return render_template("/posts/post_update.html", errors = errors, form_data=data)


@app.route("/posts/<id>/delete", methods = ["POST", "GET"])
def post_delete(id):
    if 'user_id' not in session.keys():
        return redirect('/login')

    if request.method == "POST":
        cursor.execute("DELETE from post where id = %s", (id,))
        db.commit()
        return redirect("/profile")

    return render_template("/posts/post_delete.html", post_id = id)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
