from flask import flash, g, render_template, redirect, request, session, url_for
from werkzeug.security import check_password_hash

def get():
    if "user" in session.keys():
        return redirect(url_for("index"))

    return render_template("login.html")

def post():
    if "user" in session.keys():
        return redirect(url_for("index"))

    user = g.db.users.find_one({"email": request.form["email"]})

    if user is not None and check_password_hash(user["pass"], request.form["password"]):
        flash("You were successfully logged in.", "success")

        session["user"] = {"_id": user["_id"], "name": user["name"]}
        return redirect(url_for("index"))

    flash("Incorrect email address and/or password.", "error")
    return render_template("login.html")
