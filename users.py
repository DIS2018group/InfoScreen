"""
A simple database to keep track of users who logged in at the moment
"""
import dataset
import codename

from randomavatar.randomavatar import Avatar

import os
import base64
import random
import json
import datetime


DATABASE_LOCATION = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "users.db")

SECRET_KEY = "6c3raSJc95hcx6h8EFaWCxJ8"


def open_database():
    db = dataset.connect("sqlite:///%s" % DATABASE_LOCATION)

    return db


def generate_name(user_id):
    """
    Generate a deterministic name from the given user ID
    """
    return codename.codename(
        capitalize=True, id="%s%s" % (SECRET_KEY, user_id))


def generate_avatar(user_id):
    """
    Generate a deterministic avatar and return the avatar as a base64-encoded
    image
    """
    user_seed = "%s%s" % (SECRET_KEY, user_id)
    # randomavatar generates random colors. Workaround this by initializing
    # the random number generator with the same user-specific seed every time
    random.seed(hash(user_seed))

    avatar = Avatar(rows=8, columns=8)
    image = avatar.get_image(user_seed, 64, 64)
    image = "data:image/png;base64,%s" % str(base64.b64encode(image), "utf-8")

    return image


def get_user_data(user_id):
    """
    Get persistent information for an user
    """
    db = open_database()

    user_data_table = db["user_data"]
    user_data = user_data_table.find_one(user_id=user_id)

    current_time = datetime.datetime.now(datetime.timezone.utc).timestamp()

    if not user_data:
        user_data_table.insert({
            "user_id": user_id,
            "data": json.dumps({"timestamp": current_time})
        })
        return {"timestamp": current_time}
    else:
        return json.loads(user_data["data"])


def update_user_data(user_id, data):
    """
    Update the data for a single user
    """
    db = open_database()

    user_data_table = db["user_data"]
    user_data_table.upsert(
        {
            "user_id": user_id,
            "data": json.dumps(data)
        },
        ["user_id"]
    )


def login_user(auth_id, user_id):
    """
    Login user 'user_id' using the authentication 'auth_id'
    """
    db = open_database()

    user_table = db["logged_in_users"]
    user_table.delete(auth_id=auth_id)

    # Generate deterministic username and avatar
    name = generate_name(user_id)
    image = generate_avatar(user_id)

    user_table.insert({
        "auth_id": auth_id,
        "user_id": user_id,
        "name": name,
        "image": image
    })

    return True


def logout_user(auth_id):
    """
    Logout any user previously authenticated using method 'auth_id'
    """
    db = open_database()

    user_table = db["logged_in_users"]
    user_table.delete(auth_id=auth_id)

    return True


def get_users():
    """
    Get users that are currently logged in
    """
    db = open_database()

    user_table = db["logged_in_users"]

    users = user_table.find()

    user_entries = {}
    for user in users:
        entry = user
        entry["data"] = get_user_data(user["user_id"])
        user_entries[user["auth_id"]] = entry

    return user_entries
