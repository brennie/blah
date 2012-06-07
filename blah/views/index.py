from flask import render_template, g

from pymongo import ASCENDING

def get():
    posts = g.db.posts.find().sort('date', ASCENDING).limit(10)

    return render_template("index.html", posts=posts)
