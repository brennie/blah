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

"""Create posts."""

from bson import ObjectId
import bson.errors
from datetime import datetime
from flask import abort, flash, g, redirect, request, render_template, session, url_for

from .util import require_login

@require_login(action="create")
def admin_post(action):
    """Show post form or create a post in the db, depending on the request
    method.
    """
    if request.method == "GET":
        return _get(action)

    elif request.method == "POST":
        return _post(action)

def invalid_post_id():
    """An invalid post ID was used."""
    return flash_and_redirect("Invalid post ID")

def invalid_comment_id():
    """An invalid comment ID was used."""
    return flash_and_redirect("Invalid comment ID")

def flash_and_redirect(message):
    """Flash the specified message and redirect to the admin panel.

    Parameters:
        message: the error message to flash."""
    flash(message, "error")
    return redirect(url_for("admin"))

def _get(action):
    """Show the post form."""
    if action == "create":
       return render_template("admin_create.html")

    elif action == "edit":
        post_id = request.args.get("id", None)
        if post_id is None:
            return redirect(url_for("admin"))

        try:
            post = g.db.posts.find_one({"_id": ObjectId(post_id)})
        except bson.errors.InvalidId:
            return invalid_post_id()

        if post is None:
            return invalid_post_id()

        post['tags'] = " ".join(post['tags'])
        return render_template("admin_edit.html", post=post)

    elif action == "moderate":
        post_id = request.args.get("id", None)
        if post_id is None:
            return redirect(url_for("admin"))

        try:
            post = g.db.posts.find_one({"_id": ObjectId(post_id)})
        except bson.errors.InvalidId:
            return invalid_post_id()
    
        comments = g.db.comments.find({"post": post["_id"]})
        return render_template("admin_moderate.html", post=post, comments=comments)

    elif action == "delete":
        post_id = request.args.get("id", None)
        if post_id is None:
            return redirect(url_for("admin"))

        try:
            post = g.db.posts.find_one({"_id": ObjectId(post_id)})
        except bson.errors.InvalidId:
            return invalid_post_id()

        return render_template("admin_delete.html", post=post)

    abort(404)

def _post(action):
    """Create a post in the db."""

    if action == "create":
        post = {"author": session["user"]["name"],
                "content": request.form["content"],
                "datetime": datetime.now(),
                "tags": request.form["tags"].split(),
                "title": request.form["title"]}

        postid = g.db.posts.insert(post)

        flash("Post successfully posted.", "success")
        
        return redirect(url_for("admin_post", action="create"))

    elif action == "edit":
        try:
            post_id = ObjectId(request.form['id'])
        
        except bson.errors.InvalidId:
            return invalid_post_id()

        if g.db.posts.find_one({"_id": post_id}) is None:
            return invalid_post_id()

        post = {"author": session["user"]["name"],
                "content": request.form["content"],
                "tags": request.form["tags"].split(),
                "title": request.form["title"]}

        # We use $set so that we do not overwrite the datetime field
        g.db.posts.update({"_id": post_id}, {"$set": post})
        flash("Post successfully edited.", "success")

        return redirect(url_for("admin"))

    elif action == "moderate":
        try:
            comment_id = ObjectId(request.form['id'])

        except bson.errors.InvalidId:
            return invalid_comment_id()

        if g.db.comments.find_one({"_id": comment_id}) is None:
            return invalid_comment_id()

        g.db.comments.remove(comment_id)
        flash("Comment successfully removed.", "success")

        return redirect(url_for("admin_post", action="moderate", id=request.form['post']))

    elif action == "delete":
        try:
            post_id = ObjectId(request.form['id'])

        except bson.errors.InvalidId:
            return invalid_post_id()

        if post_id is None:
            return redirect(url_for("admin"))

        if g.db.posts.find_one({"_id": post_id}) is None:
            return invalid_post_id()

        g.db.posts.remove(post_id)
        flash("Post successfully removed.", "success")

        return redirect(url_for("admin"))

    abort(404)
