# Copyright (c) 2012 Barret Rennie

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        self.add_url_rule("/tag/<t>", "tag", views.tag)

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
