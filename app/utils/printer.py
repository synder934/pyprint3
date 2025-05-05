import serial
import time
import datetime
import logging
import os
import re
import threading
from io import TextIOWrapper

import serial.tools
import serial.tools.list_ports
from .logger import LogBook


class Printer:
    IDLE = 0
    PAUSED = 1
    PRINTING = 2

    def __init__(self, port: str = None, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.__connection = None
        self.__ready_to_recieve = True
        self.__log: LogBook = LogBook()
        self.__command_queue: list[dict] = []

        self.__gcode_filepath = None
        self.__gcode_file: TextIOWrapper = None
        self.__linecount = 0
        self.__print_state = Printer.IDLE

        interface = threading.Thread(target=self.__interface, daemon=True)
        interface.start()

    def __interface(self):
        while True:
            try:  # add next print command to queue
                if (
                    self.__print_state == Printer.PRINTING
                    and self.__gcode_file is not None
                ):
                    line = self.__gcode_file.readline().strip().split(";")[0]
                    print(line)
                    self.queue_command(line, author="PRINTFILE")

            except Exception as e:
                print(e)

            try:  # send next command in queue if ready
                if len(self.__command_queue) and self.__ready_to_recieve:
                    command: str = self.__command_queue.pop(0)
                    self.add_log("SERVER", command)
                    if self.__connection is not None:
                        self.__connection.write("{}\n".format(command).encode())
                    else:
                        self.add_log("SERVER", "printer is offline")
            except Exception as e:
                print(e)

            try:  # read lines from serial connection
                if self.__connection is not None:
                    newLines = self.__connection.readlines()
                    for line in map(lambda x: x.decode().strip(), newLines):
                        kwargs = line.split(":")
                        if "busy" in kwargs:
                            self.__ready_to_recieve = False
                        if "ok" in kwargs:
                            self.__ready_to_recieve = True
                        self.add_log("PRINTER", line)
            except Exception as e:
                print(e)

    def connect(self):
        if self.port is None:
            return False

        try:
            if not self.__connection:
                self.__connection = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except Exception as e:
            return False

    def disconnect(self):
        self.__connection.close()
        self.__connection = None
        self.port = None

    def get_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def set_port(self, port: str):
        self.port = port

    def get_log_text(self):
        return str(self.__log).splitlines()

    def add_log(self, author: str, text: str):
        *kwargs, _ = text.split(":")
        level = 1

        if "busy" in kwargs:
            level = 0
        if "Unknown command" in kwargs:
            level = 2

        self.__log.add_log(author, text, level)

    def queue_command(self, command, author: str = "USER"):
        self.add_log(author, f"command queued: {command}")
        self.__command_queue.append(command)

    def set_filename(self, filename: str):
        if self.__gcode_file is not None:
            self.__gcode_file.close()
        self.__gcode_filepath = os.path.join(os.curdir, "uploads", filename)
        self.__gcode_file = open(self.__gcode_filepath, "r")

    def get_filename(self):
        if self.__gcode_filepath:
            return self.__gcode_filepath.rsplit(os.sep, 1)[1]
        else:
            return "None selected"

    def list_files(self):
        return os.listdir(os.path.join(os.curdir, "uploads"))

    def get_print_state(self):
        return self.__print_state

    def get_print_state_name(self):
        return self.__print_state.__qualname__

    def set_print_state(self, state: int):
        print(state)
        self.__print_state = state

    def get_print_states(self):
        return [
            {"name": "IDLE", "value": Printer.IDLE},
            {"name": "PAUSED", "value": Printer.PAUSED},
            {"name": "PRINTING", "value": Printer.PRINTING},
        ]


if __name__ == "__main__":
    # printer = Printer()
    # printer.connect()
    # while True:
    #     command = input("ender3 > ")
    #     printer.queue_command(command)

    pass
