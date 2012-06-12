from bson import ObjectId
from flask import abort, g, render_template
from pymongo import DESCENDING

def post(id):
    post = g.db.posts.find_one({"_id": ObjectId(id)})

    if post is None:
        abort(404)

    return render_template("post.html", post=post)
