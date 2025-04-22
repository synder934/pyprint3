from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    jsonify,
)
from . import customFlask
import os
import sys
import socket


main = Blueprint("main", __name__)
current_app: customFlask


@main.route("/", methods=["GET", "POST"])
def index():
    print(current_app.printer._listPorts())

    return render_template(
        "index.html",
        printer=current_app.printer,
        os=os,
        sys=sys,
        socket=socket,
    )


@main.route("/send_command", methods=["POST"])
def send_command():

    command = request.form.get("command")
    if command:
        current_app.printer.queue_command(command)

    return redirect(request.referrer)


@main.route("/connect", methods=["POST"])
def connect_to_printer():

    port = request.form.get("port")
    current_app.printer.set_port(port)
    current_app.printer.connect()

    return redirect(request.referrer)


@main.route("/disconnect", methods=["POST"])
def disconnect_from_printer():
    current_app.printer.connection.close()
    current_app.printer.connection = None
    return redirect(request.referrer)


@main.route("/serial-log")
def serial_log():
    return jsonify(current_app.printer.getLogText())
