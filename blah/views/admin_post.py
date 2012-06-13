from datetime import datetime
from flask import flash, g, redirect, request, render_template, session, url_for

from .util import require_login

@require_login(action="create")
def admin_post(action):
    if request.method == "GET":
        return _get(action)
    elif request.method == "POST":
        return _post(action)

def _get(action):
    if action == "create":
       return render_template("admin_post.html")

    abort(404)

def _post(action):
    if action == "create":
        post = {"author": session["user"]["name"],
                "content": request.form["content"],
                "datetime": datetime.now(),
                "tags": request.form["tags"].split(),
                "title": request.form["title"]}

        postid = g.db.posts.insert(post)

        flash("Post successfully posted.", "success")
        
        return redirect(url_for("admin_post", action="create"))

    abort(404)
