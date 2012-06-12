from datetime import datetime
from flask import render_template

from .util import require_login

@require_login()
def admin():
    return render_template("admin.html")
