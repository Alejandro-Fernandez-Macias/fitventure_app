from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user

db = 'fitventure_db'

class Workout:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.length = data['length']
        self.type = data['type']
        self.instructions= data['instructions']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.likes = 0
        self.creator = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO workouts ( name, length, type, instructions, user_id ) VALUES ( %(name)s, %(length)s, %(type)s,%(instructions)s, %(user_id)s );"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM workouts WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = f"UPDATE workouts SET name = %(name)s, length = %(length)s, type = %(type)s, instructions =  %(instructions)s WHERE id = %(id)s ;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM workouts;"
        results = connectToMySQL(db).query_db(query)
        all_workouts = []
        for row in results:
            print(row['name'])
            all_workouts.append(cls(row))
        return all_workouts

    @classmethod
    def get_user_created_workouts(cls):
        query = 'SELECT * FROM users JOIN workouts ON workouts.user_id = users.id;'
        results = connectToMySQL(db).query_db(query)
        workouts = []
        # print(results)
        for workout in results:
            creator =user.User(workout)
            workout_data = {
                'id': workout['workouts.id'],
                'name' : workout['name'],
                'length' : workout['length'],
                'type' : workout['type'],
                'instructions' : workout['instructions'],
                'created_at' : workout['created_at'],
                'updated_at' : workout['updated_at'],
                'user_id' : workout['user_id']
            }
            creator.workout = Workout(workout_data)
            workouts.append(creator)
        return workouts

    @classmethod
    def get_one_workout(cls, data):
        query = "SELECT * FROM workouts JOIN users on workouts.user_id = users.id WHERE workouts.id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        workout = cls(results[0])
        for row in results:
            user_data = {
                'id' : row['id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
        workout.creator = user.User(user_data)
        return workout

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM  workouts WHERE id = %(id)s"
        result = connectToMySQL(db).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_likes(cls):
        query = "SELECT wo.id, wo.name, wo.length, wo.type, wo.instructions, wo.user_id, wo.created_at, wo.updated_at, count(l.workout_id) AS likes FROM workouts wo LEFT JOIN likes l ON wo.id = l.workout_id GROUP BY wo.id,  wo.name, wo.length, wo.type, wo.instructions, wo.user_id, wo.created_at, wo.updated_at"
        results = connectToMySQL(db).query_db(query)
        workouts = []
        for row in results:
            workout = cls(row)
            workout.creator = user.User.get_one({'id' : row['user_id']})
            workout.likes = row['likes']
            workouts.append(workout)
        return workouts

    @classmethod
    def get_liked_workout(cls, data):
        query = "SELECT workouts.* FROM workouts LEFT JOIN likes ON workouts.id = likes.workout_id WHERE likes.user_id = %(user_id)s"
        results = connectToMySQL(db).query_db(query, data)
        workouts = []
        for row in results:
            workouts.append(cls(row))
        return workouts


    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO likes (user_id, workout_id) VALUES ( %(user_id)s, %(workout_id)s )"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def unlike(cls, data):
        query = "Update likes SET workout_id = %(workout_id)s - 1 WHERE %(workout_id)s > 0;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_workout(workout):
        is_valid = True
        if len(workout['name']) < 3:
            flash("*Name must be at least 3 characters long", "workout")
            is_valid = False
        if len( workout['length'] ) < 3:
            is_valid = False
            flash("*Length must be at least 3 characters long", "workout")
        if len(workout['type']) < 3:
            flash("*Type must be at least 3 characters long", "workout")
            is_valid = False
        if ['instructions'] == "":
            flash("*Instructions must not be empty")
            is_valid = False
        return is_valid