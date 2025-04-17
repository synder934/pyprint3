from flask import Blueprint, render_template, request, redirect, url_for, current_app
from . import customFlask

main = Blueprint("main", __name__)
current_app: customFlask


@main.route("/", methods=["GET", "POST"])
def index():

    return render_template(
        "index.html",
        ports=current_app.printer._listPorts(),
        printer=current_app.printer,
    )


@main.route("/send_command", methods=["POST"])
def send_command():

    command = request.form.get("command")
    if command:
        current_app.printer._sendCommand(command)

    return redirect(request.referrer)


@main.route("/connect", methods=["POST"])
def connect_to_printer():

    port = request.form.get("port")
    current_app.printer.setPort(port)
    current_app.printer._connect()

    return redirect(request.referrer)
