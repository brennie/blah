from flask import Flask, g
import markdown
import pymongo

import views
from .extensions import markdown

__all__ = ("BlahApp",)

class BlahApp(Flask):
    """The blah Flask application."""
    def __init__(self, development=False):
        """Create the application.

        Parameters:
            development: Enables development server mode.
        """
        super(BlahApp, self).__init__(__name__)
        
        if development:
            self.config["DEBUG"] = True

        self.config.from_pyfile("blah.cfg")

        self.jinja_env.filters["markdown"] = markdown

        self.add_url_rule("/", "index", views.index)
        self.add_url_rule("/admin", "admin", views.admin)
        self.add_url_rule("/admin/post/<action>", "admin_post", views.admin_post, methods=["GET", "POST"])
        self.add_url_rule("/login", "login", views.login, methods=["GET", "POST"])
        self.add_url_rule("/logout", "logout", views.logout)
        self.add_url_rule("/post/<id>", "post", views.post, methods=["GET", "POST"])
        self.add_url_rule("/tag/<tag>", "tag", views.tag)

        @self.before_request
        def before_request():
            g.conn = None
            g.conn = pymongo.Connection(self.config["DB_HOST"], self.config["DB_PORT"])
            g.db = g.conn[self.config["DB"]]

            if self.config["DB_AUTH"]:
                g.db.authenticate(self.config["DB_USER"], self.config["DB_PASS"])

        @self.teardown_request
        def teardown_request(exception):
            if g.conn is not None:
                g.conn.disconnect()
                g.db = None
                g.conn = None
