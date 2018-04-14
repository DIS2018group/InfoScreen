from flask import Flask, render_template, request

from users import get_users, update_user_data

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


@app.route("/heartbeat/", methods=["POST"])
def heartbeat():
    """
    Probe the environment and figure out which user is logged in at the moment,
    if any
    """
    # Get any user data we need to update
    update = request.values.get("update", None)

    if update:
        update = json.loads(update)

        for user_id, data in update.items():
            update_user_data(user_id, data)

    data = {
        "users": get_users()
    }

    return json.dumps(data)
