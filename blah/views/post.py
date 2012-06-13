from bson import ObjectId
from datetime import datetime
from flask import abort, current_app, flash, g, render_template, redirect, request, session, url_for
from hashlib import sha1
from pymongo import ASCENDING
from time import time
import requests

from .util import validate_email

def post(id):
    if request.method == "GET":
        return _get(id)
    elif request.method == "POST":
        return _post(id)

def _get(id):
    post = g.db.posts.find_one({"_id": ObjectId(id)})
    comments = g.db.comments.find({"post": ObjectId(id)}).sort("datetime", ASCENDING)

    if post is None:
        abort(404)

    return render_template("post.html", post=post, comments=comments)

def _post(id):
    comment = {}
    comment["post"] = ObjectId(id)
    comment["content"] = request.form["content"]
    comment["datetime"] = datetime.now()
    
    if len(request.form["content"]) == 0:
        flash("A comment is required", "error")
        return redirect(url_for("post", id=id))

    if "user" in session.keys():
        comment["author"] = {
            "_id": session["user"]["_id"],
            "name": session["user"]["name"]
        }
        
        comment["verified"] = True
        
        g.db.comments.insert(comment)

        flash("Your comment was posted.", "success")
        
    else:
        error = False

        comment["author"] = {
            "email": request.form["email"],
            "name": request.form["name"]
        }
        
        recaptcha = {
            "privatekey": current_app.config["RECAPTCHA_PRIVATE"],
            "remoteip": request.remote_addr,
            "challenge": request.form["recaptcha_challenge_field"],
            "response": request.form["recaptcha_response_field"]
        }

        verified = requests.post("http://www.google.com/recaptcha/api/verify", data=recaptcha).content
        
        if verified.startswith("false"):
            flash("Incorrect captcha response.", "error")

            return redirect(url_for("post", id=id))

        if not validate_email(request.form["email"]):
            flash("You provided a malformed email address.", "error")

            return redirect(url_for("post", id=id))


    g.db.comments.insert(comment)

    flash("Your comment was successfully posted.")
   
    return redirect(url_for("post", id=id))
