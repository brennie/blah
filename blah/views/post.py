# Copyright (c) 2012 Barret Rennie

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

    flash("Your comment was posted.", "success")
   
    return redirect(url_for("post", id=id))
