from crypt import methods
from tokenize import String
from flask import Flask, render_template, request, redirect, request_finished, url_for, flash, session
from flask_mysqldb import MySQL
from wtforms import Form, StringField, validators, TextAreaField, PasswordField
from datetime import datetime

"""
host:localhost
user:flask
password:AAa3706580!!
database:Chat
"""

#Register Form
class RegisterForm(Form):
    
    name = StringField("Name and Surname", validators=[validators.DataRequired(), validators.Length(min = 3, max = 32)])
    username = StringField("Username", validators=[validators.DataRequired(), validators.Length(min = 3, max = 16)])
    email = StringField("E-mail", validators=[validators.Email(message = "E-mail address is not correct")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Password must be contains 8-16 character"), validators.Length(min = 8, max = 16)])
    re_password = PasswordField("Retype Password", validators=[validators.EqualTo(fieldname="password",message="Passwords didn't match")])

class LoginForm(Form):

    username = StringField("Enter the Username or Mail Address", validators=[validators.DataRequired(message="Please Fill Here")])
    password = PasswordField("Enter the Password", validators=[validators.DataRequired(message="Plase Fill Here")])


app = Flask(__name__)
app.secret_key = "dev"


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "flask"
app.config["MYSQL_PASSWORD"] = "AAa3706580!!"
app.config["MYSQL_DB"] = "Chat"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysqlCon = MySQL(app = app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods = ["GET", "POST"])
def register():

    registerForm = RegisterForm(request.form)
    
    if request.method == "POST" and registerForm.validate():

        cursor = mysqlCon.connection.cursor()
        
        insertQuery = "INSERT INTO user_info(name, username, email, password, createdDate) VALUES(%s,%s,%s,%s,%s)"

        cursor.execute(insertQuery, (registerForm.name.data, registerForm.username.data, registerForm.email.data, registerForm.password.data, datetime.strftime(datetime.now(),"%Y-%m-%d")))
        mysqlCon.connection.commit()
        
        cursor.close()
        
        flash("Successfully Signed Up", "success")

        return redirect(url_for("index"))

    else:
        return render_template("register.html", form = registerForm)

@app.route("/login", methods = ["GET", "POST"])
def login():

    loginForm = LoginForm(request.form)

    if request.method == "POST" and loginForm.validate():
        
        cursor = mysqlCon.connection.cursor()

        loginQuery = "SELECT * FROM user_info WHERE username=%s OR email=%s AND password=%s"

        result = cursor.execute(loginQuery,(loginForm.username.data, loginForm.username.data, loginForm.password.data))

        if result > 0:
            data = cursor.fetchone()
            flash("Successfully Logged in", "success")
            session["loggedin"] = True
            session["username"] = loginForm.username.data
            return redirect(url_for("index"))
        else:
            flash("Incorrect Entry", "danger")
            return redirect(url_for("login"))

    else:
        return render_template("login.html", form = loginForm)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")