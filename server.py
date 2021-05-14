from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)

@app.route("/")
def index():
    mysql = connectToMySQL('users_schema')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("read.html", users = users)

@app.route('/add_user')
def create():
    return render_template('create.html')

@app.route('/create', methods = ["POST"])
def add_user():
    mysql = connectToMySQL('users_schema')
    query = "INSERT INTO users (first_name,last_name,email) VALUES (%(fn)s, %(ln)s,%(email)s);"
    data = {
        'fn': request.form["fname"],
        'ln': request.form["lname"],
        'email': request.form['email']
    }
    mysql.query_db(query,data)
    return redirect("/")

@app.route('/<id>')
def show_one(id):
    mysql = connectToMySQL('users_schema')
    query = "SELECT * FROM users WHERE id=%(id)s;"
    data = {
        'id': id,
    }
    user = mysql.query_db(query,data)
    return render_template("read_one.html", id = id, user = user[0])

@app.route('/<id>/edit')
def edit(id):
    mysql = connectToMySQL('users_schema')
    query = "SELECT * FROM users WHERE id=%(id)s;"
    data = {
        'id': id,
    }
    user = mysql.query_db(query,data)
    return render_template("edit.html", id = id, user = user[0])

@app.route('/<int:id>/update', methods = ['POST'])
def update(id):
    mysql = connectToMySQL('users_schema')
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(email)s  WHERE id = %(id)s;"
    data = {
        'fn': request.form["fname"],
        'ln': request.form["lname"],
        'email': request.form['email'],
        'id': id,
    }
    print(id)
    users = mysql.query_db(query,data)
    return redirect("/")

@app.route('/<int:id>/delete')
def delete0(id):
    mysql = connectToMySQL('users_schema')
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        'id': id,
    }
    print(id)
    users = mysql.query_db(query,data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)