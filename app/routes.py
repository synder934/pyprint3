from flask import Blueprint, render_template, request, redirect, url_for, current_app

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        command = request.form.get("command")
        if command:
            current_app.printer._sendCommand(command)

    return render_template(
        "index.html",
    )
