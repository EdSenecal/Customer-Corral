
from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.user import User
from flask_app.models.customer import Customer

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
        return render_template('index.html')
#default route for loginpage

@app.route ('/test')
def test():
    return render_template ("test.html")
    


@app.route ("/register",methods=["POST"])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']),
            'company': request.form['company']
        }
    id = User.create(data)
    session ['users_id'] = id
    return redirect ("/dashboard")

#validations for creating a user

@app.route ('/dashboard')
def dashboard():
    data = {
        "id": session['users_id']
    }
    return render_template ("dashboard.html", user=User.get_by_id(data), customer = Customer.get_all() )
# shows = Show.get_all()  route for the dashboard
# 

@app.route ('/login', methods=["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash ("invalid Password", "login")
        return redirect ("/")
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash ("invalid Passord", "login")
        return redirect ("/")
    session ["users_id"] = user.id
    return redirect ('/dashboard')
#login validations for checking password

@app.route ('/logout')
def logout():
    session.clear()
    return redirect ('/')
#route for clearing session of saved user id
