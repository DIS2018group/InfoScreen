"""
A simple database to keep track of users who logged in at the moment
"""
import dataset
import codename

from randomavatar.randomavatar import Avatar

import os
import base64
import random


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
    return {
        result["auth_id"]: result
        for result in user_table.find()
    }
