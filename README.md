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
1. Clone the git repository if you haven't already  
`git clone git://github.com/brennie/blah.git -O blog`  
This will clone it into blog/
2. Install and set up `mongoDB` and `Flask`
3. Run `setup.py` and follow the instructions

Updating
---------
To update blah to the latest version, just enter the top directory and run:  
`git pull`


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
