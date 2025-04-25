from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config (match with XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_auth'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']

        table = 'admins' if user_type == 'admin' else 'users'

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM {table} WHERE username = %s AND password = %s", (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = username
            session['role'] = user_type
            return redirect('/dashboard')
        else:
            flash("Incorrect username/password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        password = request.form['password']

        table = 'admins' if user_type == 'admin' else 'users'

        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO {table}(username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        flash("Registered successfully!")
        return redirect('/')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'], role=session['role'])
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
