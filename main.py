from flask import Flask, render_template

from users import get_users

import time
import json


app = Flask(__name__)


TABS = [
    {
        "id": "unicafe",
        "name": "Unicafe Menu",
        "icon": "glyphicon-cutlery"
    },
    {
        "id": "library",
        "name": "Library",
        "icon": "glyphicon-book"
    },
    {
        "id": "users",
        "name": "Users",
        "icon": "glyphicon-users",
        "user_tab": True
    }
]


@app.route("/")
def main_view():
    return render_template(
        "main.html",
        tabs=TABS,
    )


@app.route("/heartbeat/")
def heartbeat():
    """
    Probe the environment and figure out which user is logged in at the moment,
    if any
    """
    data = {
        "users": get_users()
    }

    return json.dumps(data)
