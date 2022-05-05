from flask_app import app
from flask import render_template, redirect, session, request, flash
from..models.user import User
from..models.workout import Workout
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
    }
    user_id = User.save(data)
    user_in_db=User.get_by_email(data)
    session['user_id'] = user_id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['email'] = user_in_db.email
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login-page')
    data = {
        'id' : session['user_id']
    }

    user = User.get_one(data)
    workouts = Workout.get_likes()
    creator = Workout.get_user_created_workouts()
    likes = Workout.get_liked_workout({'user_id':session['user_id']})
    return render_template('dashboard.html', user= user, creator = creator, workouts = workouts, likes = likes)

@app.route('/login/user', methods=['POST'])
def login_form():
    data = {
        'email' : request.form['email'],
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/login-page')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/login-page')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['email'] = user_in_db.email
    return redirect('/dashboard')

@app.route('/login-page')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash(" You Have Logged out Successfully !! ")
    session.clear()
    flash(" You Have Logged out Successfully !! ")
    return redirect('/login-page')

@app.route('/user/update/<int:user_id>', methods = ['POST'])
def update_user(user_id):
    if not User.validate_user_edit(request.form):
        flash("*Your Form Submission was Unsuccesful !")
        return redirect('/dashboard')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    user_id = User.update(data, user_id)
    flash("*Your Account Info was Successfully Updated !")
    return redirect('/dashboard')

@app.route('/user/edit/<int:user_id>')
def edit_user_form(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id" : session['user_id']
    }
    user = User.get_one(user_data)
    return render_template('account.html', user = user)