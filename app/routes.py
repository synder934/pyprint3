from flask import (
    Blueprint,
    Response,
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
    current_app.camera.refresh_source()
    return render_template(
        "index.html",
        printer=current_app.printer,
        camera=current_app.camera,
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
    worked = current_app.printer.connect()
    if worked:
        current_app.printer.add_log(
            "SERVER", "connection succesfull to {}".format(port)
        )
    else:
        current_app.printer.add_log(
            "SERVER", "connection unsuccesfull to {}".format(port)
        )
    return redirect(request.referrer)


@main.route("/disconnect", methods=["POST"])
def disconnect_from_printer():
    current_app.printer.disconnect()
    return redirect(request.referrer)


@main.route("/serial-log")
def serial_log():
    return jsonify(current_app.printer.get_log_text())


@main.route("/set_level", methods=["POST"])
def set_level():
    level = request.form.get("level")
    current_app.printer._log.set_level(int(level))
    return redirect(request.referrer)


# @main.route("/video_feed")
# def video_feed():
#     return Response(
#         current_app.camera.gen_frames(),
#         mimetype="multipart/x-mixed-replace; boundary=frame",
#     )
