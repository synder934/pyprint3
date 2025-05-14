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


IDLE = 0
PAUSED = 1
PRINTING = 2


class Printer:
    def __init__(self, port: str = None, baudrate: int = 115200):
        """Creates a new Printer object allowing the user to interface with the printer

        Args:
            port (str, optional): _description_. Defaults to None.
            baudrate (int, optional): _description_. Defaults to 115200.
        """
        self.port = port
        self.baudrate = baudrate
        self.__connection = None
        self.__printer_is_busy = False
        self.__log: LogBook = LogBook()
        self.__command_queue: list[dict] = []

        self.__gcode_filepath = None
        self.__gcode_file: TextIOWrapper = None
        self.__print_state: int = IDLE

        interface = threading.Thread(target=self.__interface, daemon=True)
        interface.start()

    def __interface(self) -> None:
        """interface loop to send and recieve commands with the printer"""
        while True:

            if (
                self.__print_state == int(PRINTING)
                and self.__gcode_file is not None
                and self.__printer_is_busy == False
            ):
                self.__queue_next_gcode_command()
            self.__send_next_queued_command()
            self.__log_data_from_serial()

    def __log_data_from_serial(self) -> None:
        """reads data from serial port if open and logs all commands"""
        try:
            if self.__connection is not None:
                newLines = self.__connection.readlines()

                for line in map(lambda x: x.decode().strip(), newLines):
                    kwargs = line.split(":")
                    if "busy" in kwargs:
                        self.__printer_is_busy = True
                    if "ok" in kwargs:
                        self.__printer_is_busy = False
                    self.add_log("PRINTER", line)
        except Exception as e:
            self.disconnect()
            print(e)

    def __send_next_queued_command(self) -> None:
        """sends next command in queue to printer"""
        try:
            if len(self.__command_queue) and not self.__printer_is_busy:
                command: str = self.__command_queue.pop(0)
                self.add_log("SERVER", command)
                if self.__connection is not None:
                    self.__connection.write("{}\n".format(command).encode())
                else:
                    self.add_log("SERVER", "printer is offline")
        except Exception as e:
            print(e)

    def __queue_next_gcode_command(self) -> None:
        """queue next gcode line from printing file"""
        try:
            line = ""
            while line.startswith(";") or line == "":
                line = self.__gcode_file.readline().strip()
            self.queue_command(line, author="PRINTFILE")
        except Exception as e:
            print(e)

    def connect(self) -> bool:

        if self.port is None:
            return False
        try:
            if not self.__connection:
                self.__connection = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except Exception as e:
            return False

    def disconnect(self):
        if self.__connection is not None:
            self.__connection.close()
        self.__connection = None
        self.port = None

    def get_ports(self) -> list[str]:
        return [port.device for port in serial.tools.list_ports.comports()]

    def get_port(self) -> str:
        return self.port

    def set_port(self, port: str) -> None:
        self.port = port

    def get_log_text(self) -> str:
        return str(self.__log).splitlines()

    def add_log(self, author: str, text: str) -> None:
        *kwargs, _ = text.split(":")
        level = 1

        if "busy" in kwargs:
            level = 0
        if "Unknown command" in kwargs:
            level = 2

        self.__log.add_log(author, text, level)

    def set_log_level(self, level):
        self.__log.set_level(level)

    def queue_command(self, command: str, author: str = "USER") -> None:
        """appends command to command queue

        Args:
            command (str): command to be appended
            author (str, optional): sender of command. Defaults to "USER".
        """
        self.add_log(author, f"command queued: {command}")
        self.__command_queue.append(command)

    def set_filename(self, filename: str) -> None:
        if self.__gcode_file is not None:
            self.__gcode_file.close()
        self.__gcode_filepath = os.path.join(os.curdir, "uploads", filename)
        self.__gcode_file = open(self.__gcode_filepath, "r", encoding="utf-8")

    def get_filename(self) -> str:
        if self.__gcode_filepath:
            return self.__gcode_filepath.rsplit(os.sep, 1)[1]
        else:
            return "None selected"

    def list_files(self) -> list[str]:
        return os.listdir(os.path.join(os.curdir, "uploads"))

    def get_print_state(self) -> int:
        return self.__print_state

    def set_print_state(self, state: int) -> None:
        self.__print_state = state

    def get_print_states(self) -> list[dict]:
        return [
            {"name": "IDLE", "value": IDLE},
            {"name": "PAUSED", "value": PAUSED},
            {"name": "PRINTING", "value": PRINTING},
        ]

    def is_connected(self):
        if self.__connection != None:
            return True

        return False


if __name__ == "__main__":
    # printer = Printer()
    # printer.connect()
    # while True:
    #     command = input("ender3 > ")
    #     printer.queue_command(command)

    pass
