from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import CSRFProtect
from forms import SignupForm, LoginForm
from database import create_connection, create_tables, insert_user, search_user
import hashlib

app = Flask("__main__")
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure secret key
csrf = CSRFProtect(app)

# Initialize the database and create tables
# create_tables()

@app.route('/')
def index():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = search_user(username)

            if user:
                if user[5] == password:
                    # Passwords match - user is authenticated
                    user_data = {
                        'name': user[1],
                        'username': user[2],
                        'phone': user[3],
                        'email': user[4],
                        'usertype': user[6],
                        'dateofbirth': user[7]
                    }
                    return render_template('welcome.html', **user_data)
                else:
                    # Invalid username or password - return a JSON response
                    flash("Invalid username or password", 'error')
                    return render_template('login.html', form=form)
            else:
                # User not found - return a JSON response
                flash("User not found", 'error')
                return render_template('login.html', form=form)
    elif request.method == 'GET':
        # Render the login page on GET requests
        return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            username = form.username.data
            phone = form.phone.data
            email = form.email.data
            password = form.password.data
            usertype = form.usertype.data
            dateofbirth = form.dateofbirth.data

            # Use the database function to insert user data
            insert_user(name, username, phone, email, password, usertype, dateofbirth)
            flash("Signup successful for: " + username)
            return redirect(url_for('index'))
    elif request.method == 'GET':
        # Render the signup page on GET requests
        return render_template('signup.html', form=form)

@app.route('/welcome')
def welcome(user):
    # Replace with logic to fetch user data based on the currently logged-in user
    user_data = {
        'name': 'John Doe',
        'username': 'johndoe',
        'phone': '123-456-7890',
        'email': 'johndoe@example.com',
        'usertype': 'client',
        'dateofbirth': 'January 1, 1990'
    }

    return render_template('welcome.html', **user_data)

@app.route('/logout')
def logout():
    # Implement your logout logic here, e.g., clearing session data
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8080)

