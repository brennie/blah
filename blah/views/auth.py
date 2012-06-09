from flask import flash, redirect, request, session, url_for

def require_login(next_view=None):
    """Returns a decorator to wrap a view so that the user is forwarded to the
    login page if he/she is not logged in.

    Parameters:
        next: The next view to forward do. If it is not specified, it will
              default to the current page.

    """

    def required_login_view_decorator(view):
        """Decorates a view so that the user is forwarded to the login page if
        he/she is not logged in.

        Parameters:
            view: The view to decorate.
        """

        def required_login_view(*args, **kwargs):
            # request.path must be evaluated in a request context
            if next_view is None:
                next = request.path
            else:
                next = url_for(next_view)

            if "user" not in session.keys():
                flash("You must be logged in to access this page.", "error")

                return redirect(url_for("login.get", next=next))

            return view(*args, **kwargs)

        # Included for debugging purposes
        required_login_view.__name__ = "required_login_view(%s)" % view.__name__
        required_login_view.__doc__ = view.__doc__

        return required_login_view

    return required_login_view_decorator
