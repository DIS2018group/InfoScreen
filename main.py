from flask import Flask, render_template


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
