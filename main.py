from flask import Flask, render_template, request

from users import get_users, update_user_data
from timetables import get_timetable

import datetime
import time
import json
import os


app = Flask(__name__)

LOG_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "app.log")


TABS = [
    {
        "id": "timetables",
        "name": "Public transit timetables",
        "icons": ["fas", "fa-bus", "fa-5x"],
        "icon_type": "i",
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


@app.route("/log/", methods=["POST"])
def log():
    """
    Log given information into a log file
    """
    log_data = json.loads(request.values.get("log", {}))
    log_data["timestamp"] = datetime.datetime.now().timestamp()

    with open(LOG_PATH, "a") as f:
        f.write("%s\n" % json.dumps(log_data))

    return json.dumps({"status": "success"})
