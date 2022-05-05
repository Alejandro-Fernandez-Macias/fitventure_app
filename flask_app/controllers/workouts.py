from flask_app import app
from flask import render_template, redirect, session, request, flash, json, jsonify
from flask_app.controllers.users import dashboard
from..models.workout import Workout
from..models.user import User
from flask_app.config.mysqlconnection import connectToMySQL
# import mysql.connector


@app.route('/create')
def create_form():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id' : session['user_id']
    }
    user = User.get_one(data)
    return render_template('create.html', user = user)

@app.route('/workout/new', methods = ["POST"])
def create_workout():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect('/create')
    data = {
        'name' : request.form['name'],
        'length' : request.form['length'],
        'type' : request.form['type'],
        'instructions' : request.form['instructions'],
        'user_id' : session['user_id']
    }
    Workout.save(data)
    return redirect('/dashboard')

@app.route('/workout/<int:workout_id>')
def get_one(workout_id):
    data = {
        'id' : workout_id
    }
    workout = Workout.get_one(data)
    return redirect ('/dashboard', workout = workout)

@app.route('/workout/update', methods = ['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Workout.validate_workout(request.form):
        return redirect ('/create')
    data = {
        'name': request.form['name'],
        'length' : request.form['length'],
        'type': request.form['type'],
        'instructions' : request.form['instructions'],
        # 'user_id' : request.form['user_id'],
        'id': request.form['id']
    }
    Workout.update(data)
    return redirect('/dashboard')

@app.route('/workout/edit/<int:id>')
def edit_form(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    user_data = {
    'id' : session['user_id']
    }
    workout =Workout.get_one(data)
    user = User.get_one(user_data)
    return render_template('edit.html', workout = workout, user = user )

@app.route('/workout/view/<int:workout_id>')
def view_workout(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : workout_id
    }
    user_data = {
        'id': session['user_id']
    }
    workout = Workout.get_one_workout(data)
    user = User.get_one(user_data)
    return render_template('view.html', workout = workout, user = user)

@app.route('/workout/delete/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    Workout.destroy(data)
    return redirect('/dashboard')

@app.route('/workout/like/<int:workout_id>')
def add_likes(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id' : session['user_id'],
        'workout_id' : workout_id
    }
    Workout.add_like(data)
    return redirect('/dashboard')

@app.route('/workout/unlike/<int:workout_id>')
def unlike(workout_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id' : session['user_id'],
        'workout_id' : workout_id
    }
    Workout.get_liked_workout(data)
    # User.get_user_liked_workout()
    Workout.unlike(data)
    User.get_user_liked_workout()
    return redirect('/dashboard')

@app.route('/chart/progress')
def chart():
    if 'user_id' not in session:
        return redirect('/login-page')
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="root",
                               database="fitventure_db")
    mycursor = mydb.cursor()
    # Fecthing Data From mysql to my python progame
    mycursor.execute("SELECT * FROM workouts")
    result = mycursor.fetchall
    users = []
    workouts =[]

    for i in mycursor:
        users.append(i[1])

    mycursor2 = mydb.cursor()
    mycursor2.execute("SELECT user_id from workouts")
    for j in mycursor2:
        workouts.append(j[0])

    print("ID of workouts = ", users)
    print("Name of workouts = ", workouts)

    lables = users
    values = workouts
    return render_template('graphs.html', user=user, labels = lables, values = values)