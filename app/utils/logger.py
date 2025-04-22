import time as t
from datetime import datetime as dt
import logging


class Log:
    FATAL = 3
    WARNING = 2
    INFO = 1
    DEBUG = 0

    def __init__(self, author: str, text: str, level: int = 0):
        self.author = author
        self.text = text
        self.level = level
        self.time = dt.now()

    def __repr__(self):
        return (
            f"{self.time.strftime("[%d/%m/%Y %H:%M:%S]")} [{self.author}] {self.text}"
        )


class LogBook:
    def __init__(self):
        self._logs = []

    def add_log(self, author: str, text: str, level: int = Log.INFO):
        self._logs.append(
            Log(
                author=author,
                text=text,
                level=level,
            )
        )

    def get_logs(self):
        return self._logs

    def __repr__(self):
        return "\n".join([str(log) for log in self._logs])


if __name__ == "__main__":
    logbook = LogBook()
    logbook.add_log("test log")

    print(logbook)
