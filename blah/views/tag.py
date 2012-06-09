from flask import g, render_template
from markdown import markdown
from pymongo import DESCENDING

def get(tag):
    posts = g.db.posts.find({'tags': tag}).sort('datetime', DESCENDING).limit(10)

    return render_template("tag.html", posts=posts, tag=tag, md=markdown)
