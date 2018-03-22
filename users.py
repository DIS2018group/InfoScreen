"""
A simple database to keep track of users who logged in at the moment
"""
import dataset

import os


DATABASE_LOCATION = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "users.db")


def open_database():
    db = dataset.connect("sqlite:///%s" % DATABASE_LOCATION)

    return db


def login_user(auth_id, user_id):
    """
    Login user 'user_id' using the authentication 'auth_id'
    """
    db = open_database()

    user_table = db["logged_in_users"]
    user_table.delete(auth_id=auth_id)
    user_table.insert({"auth_id": auth_id, "user_id": user_id})

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
        result["auth_id"]: result["user_id"]
        for result in user_table.find()
    }
