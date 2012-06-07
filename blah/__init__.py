from flask import Flask, g
import pymongo

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
