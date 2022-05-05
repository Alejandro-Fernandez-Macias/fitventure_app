from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math

db = "fitventure_db"

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.sender = data['sender']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def time_span(self):
        now = datetime.now()
        ongoing = now - self.created_at
        print(ongoing.days)
        print(ongoing.total_seconds())
        if ongoing.days > 0:
            return f"{ongoing.days} days ago"
        elif (math.floor(ongoing.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(ongoing.total_seconds() / 60) / 60)} hours ago"
        elif ongoing.total_seconds() >= 60:
            return f"{math.floor(ongoing.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(ongoing.total_seconds())} seconds ago"


    @classmethod
    def get_all_with_users(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages. * FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        messages=[]
        for row in results:
            messages.append(cls(row))
        return messages


    @classmethod
    def save_message(cls, data):
        query = "INSERT INTO messages ( content, sender_id, receiver_id ) VALUES ( %(content)s, %(sender_id)s, %(receiver_id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)