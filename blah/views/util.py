from flask import flash, g, redirect, request, render_template, session, url_for
from pymongo import DESCENDING
import re

_email_re = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$", re.I)

def validate_email(email):
    """Naive email validation.

    Parameters:
        email: The email to validate.
    """

    return bool(_email_re.match(email))

def render_posts(title, view_name, spec=None, **kwargs):
    """Render a set of posts filtered by spec.

    Parameters:
        title: The title of the page.
        view_name: The name of the view used to generate filtering. If there
                   other pages, they will use this to get the url.
        spec: The filter to give to g.db.posts.find().
        kwargs: These arguments are passed to calls to url_for().
    """
    
    page = int(request.args.get("page", 1))

    posts = g.db.posts.find(spec).sort("datetime", DESCENDING).skip((page - 1) * 10).limit(10)

    newer = None
    older = None

    if page > 1:
        if page == 2:
            newer = url_for(view_name, **kwargs)
        else:
            newer = url_for(view_name, page=page - 1, **kwargs)

    if posts.count() > page * 10:
        older = url_for(view_name, page=page + 1, **kwargs)

    return render_template("posts.html", title=title, posts=posts, newer=newer, older=older)

def require_login(next_view=None, **url_args):
    """Returns a decorator to wrap a view so that the user is forwarded to the
    login page if he/she is not logged in.

    Parameters:
        next: The next view to forward do. If it is not specified, it will
              default to the current page.
        url_args: Arguments to pass to url_for(). Used only when generating the
                  url to forward to.

    """

    def required_login_view_decorator(view):
        """Decorates a view so that the user is forwarded to the login page if
        he/she is not logged in.

        Parameters:
            view: The view to decorate.
        """

        def required_login_view(*args, **kwargs):
            if "user" not in session.keys():
                flash("You must be logged in to access this page.", "error")
                next = url_for(next_view or request.endpoint, **url_args)

                return redirect(url_for("login", next=next))

            return view(*args, **kwargs)

        # Included for debugging purposes
        required_login_view.__name__ = "required_login_view(%s)" % view.__name__
        required_login_view.__doc__ = view.__doc__

        return required_login_view

    return required_login_view_decorator
