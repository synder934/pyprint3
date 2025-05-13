from flask import (
    Blueprint,
    Response,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    jsonify,
    flash,
)
from . import customFlask
import os
import sys
import socket
from .utils.utils import *


main = Blueprint("main", __name__)
current_app: customFlask


@main.route("/", methods=["GET", "POST"])
def index():
    # current_app.camera.refresh_source()
    return render_template(
        "index.html",
        printer=current_app.printer,
        # camera=current_app.camera,
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
    level = int(request.form.get("level"))
    current_app.printer.set_log_level(level)
    return redirect(request.referrer)


# @main.route("/video_feed")
# def video_feed():
#     return Response(
#         current_app.camera.gen_frames(),
#         mimetype="multipart/x-mixed-replace; boundary=frame",
#     )


@main.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if "file" not in request.files:
            pass
        elif file.filename == "":
            pass
        elif file and allowed_file(file.filename):
            filepath = os.path.join(f"{os.curdir}{os.sep}uploads", file.filename)
            file.save(filepath)

    return redirect(request.referrer)  # or your main page


@main.route("/select_file", methods=["POST"])
def select_file():
    current_app.printer.set_filename(request.form.get("file"))
    return redirect(request.referrer)


@main.route("/set_print_state", methods=["POST"])
def set_print_state():
    current_app.printer.set_print_state(int(request.form.get("state")))
    return redirect(request.referrer)
