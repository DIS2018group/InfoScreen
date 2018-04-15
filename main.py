from flask import Flask, render_template, request

from users import get_users, update_user_data
from timetables import get_timetable

import time
import json


app = Flask(__name__)


TABS = [
    {
        "id": "unicafe",
        "name": "Unicafe Menu",
        "icons": ["glyphicon", "glyphicon-cutlery"],
        "icon_type": "span",
    },
    {
        "id": "timetables",
        "name": "Public transit timetables",
        "icons": ["fas", "fa-bus", "fa-5x"],
        "icon_type": "i",
    },
    {
        "id": "library",
        "name": "Library",
        "icons": ["glyphicon", "glyphicon-book"],
        "icon_type": "span",
    },
    {
        "id": "users",
        "name": "Users",
        "icons": ["glyphicon", "glyphicon-users"],
        "icon_type": "span",
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


@app.route("/timetables/")
def timetables():
    """
    Retrieve public transit timetables
    """
    timetable = get_timetable()

    return json.dumps(timetable)
