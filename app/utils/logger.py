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
    def __init__(self, level: int = Log.INFO):
        self.__level = level
        self.__logs: list[Log] = []

    def add_log(self, author: str, text: str, level: int = Log.INFO):
        self.__logs.append(
            Log(
                author=author,
                text=text,
                level=level,
            )
        )

    def get_logs(self):
        return self.__logs

    def set_level(self, level: int):
        self.__level = level

    def __repr__(self):
        return "\n".join([str(log) for log in self.__logs if log.level >= self.__level])


if __name__ == "__main__":
    logbook = LogBook()
    logbook.add_log("test log")

    print(logbook)
