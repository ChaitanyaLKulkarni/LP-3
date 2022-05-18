from distutils.log import error
from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)


@app.route("/search")
def search():
    code = request.args.get('code')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        statement = "select * from data where data='" + code + "'"
        c.execute(statement)
        found = c.fetchall()
        if found == []:
            return f"Invalid Code<br>{statement}"
        else:
            return f"Wifi Connection Established<br>{statement}"
    except sqlite3.Error as e:
        return str(e) + f"<br>{statement}"
    finally:
        conn.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", loginLink="/login")

    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        statement = "select * from admin where username=(?) and password=(?)"
        c.execute(statement, (username, password))
        found = c.fetchone()
        if found == None:
            return render_template("login.html",  loginLink="/login", error="Invalid Credentials")
        else:
            return redirect("/admin")
    except sqlite3.Error as e:
        return str(e) + f"<br>{statement}"


@app.route("/login-vulnerable", methods=["GET", "POST"])
def loginVulnerable():
    if request.method == "GET":
        return render_template("login.html", loginLink="/login-vulnerable")

    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        statement = "select * from admin where username='" + \
            username + "' and password='" + password + "'"
        c.execute(statement)
        found = c.fetchone()
        if found == None:
            return render_template("login.html", loginLink="/login-vulnerable", error="Invalid Credentials")
        else:
            return redirect("/admin")
    except sqlite3.Error as e:
        return str(e) + f"<br>{statement}"


@app.route("/admin")
def adminPage():
    return render_template("admin.html")


@app.route("/create")
def addAdmin():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    try:
        statement = "CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
        c.execute(statement)

        # c.execute("DELETE * from admin")
        # conn.commit()

        # statement = "INSERT INTO admin (username,password) values('admin', 'securepassword')"
        # c.execute(statement)
        # conn.commit()

        statement = "SELECT * FROM admin"
        c.execute(statement)

        found = c.fetchall()
        if len(found) == 0:
            statement = "INSERT INTO admin (username,password) values('admin', 'securepassword')"
            c.execute(statement)
            conn.commit()
            found = c.fetchall("SELECT * FROM admin")

        conn.close()
        return {"found": found}
    except sqlite3.Error as e:
        return str(e) + f"<br>{statement}"


@app.route("/contact")
def contactPage():
    args = request.args
    return render_template("contact.html", **args)


@ app.route("/")
def main():
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
