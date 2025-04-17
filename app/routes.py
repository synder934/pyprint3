from flask import Blueprint, render_template, request, redirect, url_for, current_app
from . import customFlask

main = Blueprint("main", __name__)
current_app: customFlask


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        command = request.form.get("command")
        if command:
            current_app.printer._sendCommand(command)

    return render_template(
        "index.html",
        ports=current_app.printer._listPorts(),
    )
