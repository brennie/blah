from .util import render_posts

def get():
    return render_posts("home", "index")
