

from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash, redirect
from flask_app.models import user



class Customer:
    db = "customercorral"
    def __init__(self, data):
        self.id = data ["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        # self.phone_number = data["phone_number"]
        self.email = data["email"]
        self.posted_by = data["users_id"]
        
        



#class constructor establishes the rows of the database in python
    @classmethod
    def create(cls, data):
        print("this ran")
        
        query = "insert into customers (first_name, last_name, email, users_id) VALUES (%(first_name)s,%(last_name)s, %(email)s,%(users_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    #create runs sql to create the rows, only needs the values that aren't provided by the server.  

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM customers;"
        results = connectToMySQL(cls.db).query_db(query)
        all_customers = []
        for row in results:
            print(row['first_name'])
            all_customers.append (cls(row))
        return all_customers
#get all function pulls all users, gets passed to other methods to parse data

    @classmethod
    def validate_customer(cls,customer):
        print (customer)
        is_valid = True
        if len (customer['first_name']) < 3:
            flash ("first_name must be more than 3 charecters)","customer")
            is_valid = False
        
        if len (customer['last_name']) < 3:
            flash ("last_name must be more than 3 charecters","customer")
            is_valid = False
        
        #phone numbers proved an insurmountable task
        
        # if len (customer['phone_number']) >= 10:
        #     flash ("phone_number is required ","customer")
        #     is_valid = False
        # if len (customer['phone_number']) <= 8:
        #     flash ("phone_number is required ","customer")
        #     is_valid = False
        
        # if len (customer['email']) < 1:
        #     flash ("email must be more than 1 charecters ","customer")
        #     is_valid = False
        #Orignially I had an email validation, but deceided against it as some customers will not have an email.  
        return is_valid
        
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM customers WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update (cls,data):
        query = "UPDATE customers SET first_name = %(first_name)s ,last_name= %(last_name)s, email= %(email)s WHERE id = %(id)s;"
        print(query)
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM customers left join users on users.id = customers.users_id WHERE customers.id =%(id)s ;"
        results = connectToMySQL (cls.db).query_db(query,data)
        print(results)
        return results[0]
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM customers WHERE id = %(id)s;"
        results = connectToMySQL (cls.db).query_db(query,data)
        print(results)
        return cls (results[0])


    # @classmethod
    # def get_by_id (cls, data):
    #     query = "SELECT * FROM users WHERE id = %(id)s;"
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     return cls(results[0])
#get by id queries the db users for a specific id