from .util import render_posts

def get(tag):
    return render_posts("posts tagged '%s'" % tag, "tag", {"tags": tag}, tag=tag)
