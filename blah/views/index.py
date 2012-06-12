from .util import render_posts

def index():
    return render_posts("home", "index")
