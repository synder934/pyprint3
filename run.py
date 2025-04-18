from app import create_app
from threading import Thread
import subprocess
import time


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
    # autoUpdate = Thread(target=gitCheckAndPull, daemon=True)
    # autoUpdate.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
