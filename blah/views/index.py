from flask import g, render_template
from pymongo import DESCENDING

def get():
    posts = g.db.posts.find().sort('datetime', DESCENDING).limit(10)

    return render_template("index.html", posts=posts)
