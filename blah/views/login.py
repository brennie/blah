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

from flask import flash, g, render_template, redirect, request, session, url_for
from werkzeug.security import check_password_hash

def login():
    if request.method == "GET":
        return _get()
    elif request.method == "POST":
        return _post()

def _get():
    if "user" in session.keys():
        return redirect(url_for("index"))

    return render_template("login.html", next=request.args.get("next"))

def _post():
    if "user" in session.keys():
        return redirect(url_for("index"))

    user = g.db.users.find_one({"email": request.form["email"]})

    if user is not None and check_password_hash(user["pass"], request.form["password"]):
        flash("You were successfully logged in.", "success")

        session["user"] = {"_id": user["_id"], "name": user["name"]}

        return redirect(request.form.get("next", url_for("index")))

    flash("Incorrect email address and/or password.", "error")
    return redirect(url_for("login.get"))
