from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module  return results
from flask import flash, redirect


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$") 

class User:
    db = "customercorral"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.password = data["password"]
        self.email = data["email"]
        self.company = data["company"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        

        

#class constructor establishes the rows of the database in python
    @classmethod
    def create(cls, data):
        query = "insert into users (first_name, last_name, password, email, company) VALUES (%(first_name)s, %(last_name)s,%(password)s, %(email)s,%(company)s )"
        return connectToMySQL(cls.db).query_db(query,data)
    #create runs sql to create the rows, only needs the values that aren't provided by the server.  
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:     
            users.append (cls(row))
        return users
#get all function pulls all users, gets passed to other methods to parse data


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s "
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls (results[0])
#get by email function searches for a matching email that gets passed in, in our app fromt he form data

    @staticmethod
    def validate_user(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid
#validation for the email using the regex template, ensures the email is valid in terms of form.  I'm assuming actual db's pole against the email servers to validate.

    @classmethod
    def get_by_id (cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
#get by id queries the db users for a specific id
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s "
        results = connectToMySQL(User.db).query_db(query, user)
        if len (results) >= 1:
            flash ('email already taken.',"register")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash ("invalid email!", "register")
            is_valid = False
        if len (user ["first_name"]) < 3:
            flash ("first name must be more than 3", "register")
            is_valid = False
        if len (user ["last_name"]) < 3:
            flash ("last name must be more than 3", "register")
            is_valid = False
        if len (user ["password"]) < 8:
            flash ("passwords must be more than 8", "register")
            is_valid = False
        if len (user ["company"]) < 1:
            flash ("company must not be blank", "register")
            is_valid = False
        if user ["password"] != user ["confirm"]:
            is_valid = False
            flash ("passwords dont match", "register")
        return is_valid
# validate register checks the form fields for a user registration and confirms it meets certain requirements.  

