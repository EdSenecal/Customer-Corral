
from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.customer import Customer
from flask_app.models.user import User




@app.route ('/new/customer')
def new_customer():
    if 'users_id' not in session:
        return redirect ('/logout')
    data = {"id":session ['users_id']
    }
    print (data)
    return render_template ('customer.html', user=User.get_by_id(data))


@app.route('/create/customer',methods=['POST'])
def create_customer():
    if 'users_id' not in session:
        return redirect ('/logout')
    if not Customer.validate_customer(request.form):
        return redirect ('/new/customer')
    data = {
        "first_name":request.form ['first_name'],
        "last_name":request.form ['last_name'],
        "email": request.form ['email'],
        "users_id": session['users_id']
    }
    print(data)
    Customer.create(data)
    return redirect('/dashboard')
#route for creating a new customer, calls on the method validate customer which needs to be written


@app.route('/show/customer/<int:id>')
def customer (id):
    if 'users_id' not in session:
        return redirect ('/logout')
    data = {"id":session ['users_id']
    }
    s ={
        "id":id

    }
    return render_template("show_customer.html", user = User.get_by_id(data), customer = Customer.get_one_by_id(s))

@app.route('/customer/edit/<int:id>')
def edit (id):

    if 'users_id' not in session:
        return redirect ('/logout')
    data = {
        "id":session ['users_id']
    }
    customer={
        "id":id
    }

    return render_template("update_customer.html", customer = Customer.get_one(customer), user = User.get_by_id(data))


@app.route('/customer/update/', methods=["POST"])
def update():
    if 'users_id' not in session:
        return redirect ('/logout')
    if not Customer.validate_customer(request.form):
        
        return redirect ('/dashboard')
#this is how the platform does it, i can't find how to validate and repopulate with the same information.  
#i've tried storing a variable in session and loading from that, and couldn't crack it
# also i've 
    data = {
        "first_name":request.form ['first_name'],
        "last_name":request.form ['last_name'],
        "email": request.form ['email'],
        "id": request.form ['id'],
            }
    print(data)
    Customer.update(data)
    return redirect("/dashboard")

@app.route('/customer/destroy/<int:id>')
def destroy(id):
    data ={'id': id }
    Customer.destroy(data)
    return redirect('/dashboard')

