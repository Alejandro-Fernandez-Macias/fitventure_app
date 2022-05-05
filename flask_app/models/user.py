from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt
from flask_app.models.workout import Workout
bcrypt = Bcrypt(app)

db = "fitventure_db"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = " INSERT INTO users ( first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def update(cls, data, id):
        query =f"UPDATE users SET first_name= %(first_name)s, last_name= %(last_name)s, email= %(email)s, password= %(password)s WHERE id = {id};"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = connectToMySQL(db).query_db(query, data)
        if data == ():
            return False
        else:
            return cls(data[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_liked_workout(cls):
        query = "SELECT * FROM users LEFT JOIN likes ON users.id = likes.user_id"
        results = connectToMySQL(db).query_db(query)
        users = []
        for row in results:
            user = cls(row)
            user.workouts = Workout.get_liked_workout({'user_id' : row['user_id']})
        return users


    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash("*First Name must have letters only and be at least 2 characters long")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("*Last Name must have letters only and be at least 2 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("*Email is an invalid address!")
            is_valid = False
        if User.get_by_email({'email' : data['email']}):
            flash('*Email is already in use')
            is_valid = False
        if len(data['password']) < 8:
            flash("*Password must be at least 8 characters long")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('*Password and Confirm Password do not match')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user_edit(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash("*First Name must have letters only and be at least 2 characters long")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("*Last Name must have letters only and be at least 2 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("*Email is an invalid address!")
            is_valid = False
        # if User.get_by_email({'email' : data['email']}):
        #     flash('*Email is already in use')
        #     is_valid = False
        if len(data['password']) < 8:
            flash("*Password must be at least 8 characters long")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('*Password and Confirm Password do not match')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not EMAIL_REGEX.match({'email' : data['email']}):
            flash("*Invalid Email/Password")
            is_valid = False
        return is_valid