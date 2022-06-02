from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.secret_key = "1234"

app.config["MYSQL_HOST"] = 'sql10.freesqldatabase.com'
app.config["MYSQL_USER"] = "sql10497116"
app.config["MYSQL_PASSWORD"] = "9aXw2kECyh"
app.config["MYSQL_DB"] = "sql10497116"

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if "email" in request.form and "password" in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM tabelas WHERE email=&s AND senha=%s", (email, password))
            info = cursor.fetchone()
            print(info)
            if info is not None:
                if info['email'] == email and info['senha'] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('profile'))
            else:
                return "login unsuccessfull"
    return render_template("login.html")


@app.route('/new', methods=['GET', 'POST'])
def new_user():
    print(request.form)
    if request.method == "POST":
        if "email" in request.form and "name" in request.form and "cpf" in request.form:
            if "password" in request.form:
                email = request.form['email']
                name = request.form['name']
                cpf = request.form['cpf']
                password = request.form['password']
                cur = db.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute("INSERT INTO sql10497116.tabelas(email, name, CPF, senha) VALUES (%s,%s,%s,%s)", (email, name, cpf, password))
                db.connection.commit()
                return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/new/profile')
def profile():
    if session['loginsuccess']:
        return render_template("profile.html")


@app.route('/new/logout')
def logout():
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
