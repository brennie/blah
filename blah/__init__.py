from flask import Flask, g
import pymongo

import views

__all__ = ("BlahApp",)

class BlahApp(Flask):
    """The blah Flask application."""
    def __init__(self, development=False):
        """Create the application.

        Parameters:
            development: Enables development server mode.
        """
        if development:
            super(BlahApp, self).__init__(__name__, static_folder="static")
            self.config["DEBUG"] = True
        else:
            super(BlahApp, self).__init__(__name__, static_folder=None)

        self.config.from_pyfile("blah.cfg")

        self.add_url_rule("/", "index", views.index.get)
        self.add_url_rule("/post/<id>", "post", views.post.get)

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
