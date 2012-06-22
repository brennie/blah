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

from datetime import datetime
from flask import flash, g, redirect, request, render_template, session, url_for

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

def _get(action):
    """Show the post form."""
    if action == "create":
       return render_template("admin_post.html")

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

    abort(404)
