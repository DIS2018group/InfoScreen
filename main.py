from flask import Flask, render_template

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
    # TODO: Authentication not implemented yet
    # For now, fake a login/logout every 5 seconds
    unix_timestamp = time.time()
    logged_in = unix_timestamp % 10 >= 5

    data = {
        "user": {
            "is_authenticated": True if logged_in else False,
            "name": "Terry Test" if logged_in else None
        }
    }

    return json.dumps(data)
