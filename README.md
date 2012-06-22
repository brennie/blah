blah: A Simple Flask Blog
=========================

Requirements
------------

- Flask (`easy_install flask`)
- markdown (`easy_install markdown`)
- mongoDB (`easy_install pymongo`)
- requests (`easy_install requests`)
- Python 2
- A reCAPTCHA account

Features
--------

- Create posts in markdown
- gist support in posts (see `blah/extensions.py`)

Setup
-----

1. Install and set up `mongoDB` and `Flask`
2. Run `setup.py` and follow the instructions

Development Server
------------------

To run the development server, run `app.py` in the main directory. It creates a
server on localhost:5000 to test the app. The development server will serve
static files and has debug mode enabled.

Production Server
-----------------

Run `uwsgi blah.ini` to start the development server (you may want to configure
this to suit your needs first). Check out the nginx.conf in contrib/ for a
sample nginx configuration.
