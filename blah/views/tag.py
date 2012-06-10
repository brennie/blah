from flask import g, render_template, request, url_for
from pymongo import DESCENDING

def get(tag):
    page = int(request.args.get("page", 1))

    posts = g.db.posts.find({'tags': tag}).sort('datetime', DESCENDING).skip((page - 1) * 10).limit(10)

    newer = None
    older = None
    
    if page > 1:
        if page == 2:
            newer = url_for("tag", tag=tag)
        else:
            newer = url_for("tag", tag=tag, page=page - 1)

    if posts.count() > page * 10:
        older = url_for("tag", tag=tag, page=page + 1)
    
    return render_template("tag.html", posts=posts, newer=newer, older=older)
