from flask import g, render_template, request, url_for
from pymongo import DESCENDING

def get():
    page = int(request.args.get("page", 1))

    posts = g.db.posts.find().sort('datetime', DESCENDING).skip((page - 1) * 10).limit(10)

    newer = None
    older = None
    
    if page > 1:
        if page == 2:
            newer = url_for("index")
        else:
            newer = url_for("index", page=page - 1)

    if posts.count() > page * 10:
        older = url_for("index", page=page + 1)

    return render_template("index.html", posts=posts, newer=newer, older=older)
