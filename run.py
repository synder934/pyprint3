from app import create_app
from threading import Thread


def gitCheckAndPull():
    pass


app = create_app()

if __name__ == "__main__":
    autoUpdate = Thread(target=gitCheckAndPull, daemon=True)
    autoUpdate.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
