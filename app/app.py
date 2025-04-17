from flask import Flask, render_template, request, redirect, url_for
from utils.printer import Printer
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

app = Flask(__name__)

# Create the printer object once
printer = Printer(port="/dev/ttyUSB0", baudrate=115200)
printer._connect()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        command = request.form.get("command")
        if command:
            printer._sendCommand(command)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
