from app import create_app
from threading import Thread
import subprocess
import time

import logging
from flask import Flask, request


class NoLoggingFilter(logging.Filter):
    def filter(self, record):
        ignore_paths = ["/serial-log"]  # Add any route paths you want to suppress
        return not any(path in record.getMessage() for path in ignore_paths)


def gitCheckAndPull():
    while True:
        subprocess.run(["git", "fetch"])
        res = subprocess.run(
            ["git", "status", "-uno"],
            stdout=subprocess.PIPE,
        )
        if "Your branch is behind" in res.stdout.decode():
            subprocess.run(["git", "config", "pull.ff", "only"])
            subprocess.run(["git", "pull"])
        time.sleep(5)


app = create_app()

if __name__ == "__main__":
    log = logging.getLogger("werkzeug")
    log.addFilter(NoLoggingFilter())
    autoUpdate = Thread(target=gitCheckAndPull, daemon=True)
    autoUpdate.start()

    app.run(host="0.0.0.0", port=5000, debug=True)
