#!/usr/bin/env python

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

"""Set up blah and write the configuration file."""

import os
import sys

from contextlib import closing
from pymongo import Connection
from werkzeug.security import generate_password_hash

def read_option(prompt, parser=None, default=None):
    """Read an option from standard input.

    Parameters:
    parser: Run the returned value through this function (optional)
    default: The default option (optional)
    """
    if default is not None:
        print "%s (default: %s)" % (prompt, default)
    else:
        print prompt

    value = raw_input("> ")
    
    if not len(value) and default is not None:
        return default

    if parser:
        return parser(value)

    return value

def parse_yes_no(string):
    """Simple Y/N parser. Everything but "y" or "yes" returns False."""
    return string.lower() in ("y", "yes")

if __name__ == "__main__":
    config = {}

    admin_name = read_option("Admin display name")
    admin_mail = read_option("Admin e-mail address")
    admin_pass = read_option("Admin password", parser=generate_password_hash)

    config["DB"] = read_option("mongoDB database")
    config["DB_HOST"] = read_option("mongoDB host", default="localhost")
    config["DB_PORT"] = read_option("mongoDB port", parser=int, default=27017)

    if read_option("Use mongoDB authentication? y/N", parser=parse_yes_no):
        config["DB_AUTH"] = True
        config["DB_USER"] = read_option("mongoDB username")
        config["DB_PASS"] = read_option("mongoDB password")
    else:
        config["DB_AUTH"] = False

    config["RECAPTCHA_PUBLIC"] = read_option("reCAPTCHA public key")
    config["RECAPTCHA_PRIVATE"] = read_option("reCAPTCHA private key")

    config["SECRET_KEY"] = os.urandom(32)

    with open(os.path.join("blah","blah.cfg"), "w") as cfg:
        for option, value in config.iteritems():
            cfg.write("%s=%r\n" % (option, value))

    with closing(Connection(config["DB_HOST"], config["DB_PORT"])) as conn:
        db = conn[config["DB"]]
        
        if config["DB_AUTH"]:
            if not db.authenticate(config["DB_USER"], config["DB_PASS"]):
                print "Could not authenticate to the database. Exiting..."
                sys.exit(1)

        users = db["users"]
        user = {"name": admin_name,
                "email": admin_mail,
                "pass": admin_pass}

        users.insert(user)
