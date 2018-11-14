from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
import json
import re # the "re" module will let us perform some regular expression operations
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from mysqlconnection import connectToMySQL
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "008f1818-b9a9-4c67-bd0e-752c56cbaf74"


# @app.route("/")
# def index():
#     return render_template("choose.html")

# @app.route("/reg")
# def register():
#     return render_template("index.html")

# @app.route("/log")
# def login():
#     return render_template("login.html")

@app.route("/processReg/<username>/<password>/<password_confirm>")
def processreg(username, password, password_confirm):

    print(username, password, password_confirm)
    print("************************************************")
    if len(username) < 1:
        print("win")
        return json.dumps({'success': False})
        # return json.dumps({'success': False, 'error': "please complete all required fields prior to submission"})
    if len(password) < 1:
        return json.dumps({'success': False, 'error': "password must be at least 8 characters"})
    if len(password_confirm) < 1:
        return json.dumps({'success': False, 'error': "password must be at least 8 characters"})
    if password_confirm != password:
        return json.dumps({'success': False, 'error': "password fields do not match"}) 
    else:
        pw_hash = bcrypt.generate_password_hash(password)
        print(pw_hash)
        data = {
            'username': username,
            'password_hash': pw_hash
        }
        mysql = connectToMySQL("iosShoppingListHackathon")
        query = "SELECT username From users WHERE username = '"+username+"'"
        print (query)
        new_username_id = mysql.query_db(query, data)
        print (new_username_id)
        if new_username_id:
            flash("Username is already in database!")
            return redirect('/reg')

        mysql = connectToMySQL("iosShoppingListHackathon")
        query = "INSERT INTO users(username, password) VALUES(%(username)s, %(password_hash)s);"
        new_username_id = mysql.query_db(query, data)

        print(new_username_id)

        return json.dumps({'success': True})


@app.route("/processlog/<username>/<password>")
def processlog(username, password):
    print(username, password)
    if len(username) < 1:
        return json.dumps({'success': False, 'error': "please complete all required fields"})
    if len(password) < 1:
        return json.dumps({'success': False, 'error': "please complete all required fields"})
    else:
        mysql = connectToMySQL("iosShoppingListHackathon")
        query = "SELECT * From users WHERE username = %(username)s;"
        data = { 'username': username }
        print (query)
        result = mysql.query_db(query, data)
        print (result)
        if result:
            if bcrypt.check_password_hash(result[0]['password'], password):
                session['userid'] = result[0]['id']
                flash("logged in")# just pass a string to flass function broski
                return json.dumps({'success': True})
            else:
                print("MONEY")
                return json.dumps({'success': False, 'error': "Password didn't match"})
        else:
            return json.dumps({'success': False, 'error': "Username not found"})


# @app.route("/result", methods=['Get'])
# def result():
#     return render_template("index2.html")

# @app.route("/main", methods=['Get'])
# def main():
#     if not session:
#         return redirect('/')
#     return render_template("main.html")

# @app.route("/logout", methods=['Get'])
# def logout():
#     session.clear()
#     return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)