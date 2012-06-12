from .util import render_posts

def tag(t):
    return render_posts("posts tagged '%s'" % t, "tag", {"tags": t}, tag=t)
