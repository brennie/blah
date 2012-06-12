from datetime import datetime
from flask import flash, g, redirect, request, render_template, session, url_for

from .util import require_login

@require_login(action="create")
def admin_post(action):
    if request.method == "GET":
        return get(action)
    elif request.method == "POST":
        return post(action)

def get(action):
    if action == "create":
       return render_template("admin_post.html")

    abort(404)

def post(action):
    if action == "create":
        post = {"author": session["user"]["name"],
                "content": request.form["content"],
                "datetime": datetime.now(),
                "tags": request.form["tags"].split(),
                "title": request.form["title"]}

        postid = g.db.posts.insert(post)

        flash("Post %s successfully posted." % postid, "success")
        
        return redirect(url_for("admin_post", action="create"))

    abort(404)
