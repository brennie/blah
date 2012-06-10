from datetime import datetime
from flask import flash, g, redirect, request, render_template, session, url_for

from .util import require_login

@require_login()
def get(*args):
    return render_template("admin.html")

@require_login(next_view="admin.get")
def post(action):
    if action == "create":
        # Create a post
        post = {"author": session["user"]["name"],
                "content": request.form["content"],
                "datetime": datetime.now(),
                "tags": request.form["tags"].split(),
                "title": request.form["title"]}

        postid = g.db.posts.insert(post)

        print postid

        flash("Post %s successfully posted." % postid, "success")
        
        return redirect(url_for("admin.get"))

    return redirect(url_for("admin.get"))
