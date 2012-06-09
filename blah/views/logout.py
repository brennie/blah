from flask import flash, g, redirect, request, session, url_for

def get():
    if "user" in session.keys():
        del session["user"]
        flash("You have been logged out.", "success")

    return redirect(url_for("index"))
