from flask import g, render_template
from markdown import markdown
from pymongo import DESCENDING

def get():
    posts = g.db.posts.find().sort('datetime', DESCENDING).limit(10)

    return render_template("index.html", posts=posts, md=markdown)
