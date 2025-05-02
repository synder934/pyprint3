import serial
import time
import datetime
import logging
import os
import re
import threading

import serial.tools
import serial.tools.list_ports
from .logger import LogBook


class Printer:
    def __init__(self, port: str = None, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.connection = None
        self._ready_to_recieve = True
        self._log: LogBook = LogBook()
        self.command_queue: list[dict] = []

        interface = threading.Thread(target=self._interface, daemon=True)
        interface.start()

    def _interface(self):
        while True:
            try:
                # send all queued commands
                if len(self.command_queue) and self._ready_to_recieve:
                    command: str = self.command_queue.pop(0)
                    self.add_log("USER", command)
                    if self.connection is not None:
                        self.connection.write("{}\n".format(command).encode())
                    else:
                        self.add_log("SERVER", "printer is offline")

                if self.connection is not None:

                    # read all data from port
                    newLines = self.connection.readlines()
                    for line in map(lambda x: x.decode().strip(), newLines):
                        kwargs = line.split(":")
                        if "busy" in kwargs:
                            self._ready_to_recieve = False
                        if "ok" in kwargs:
                            self._ready_to_recieve = True
                        self.add_log("PRINTER", line)
            except Exception as e:
                print(e)
                pass

    def get_log_text(self):
        return str(self._log).splitlines()

    def add_log(self, author: str, text: str):
        *kwargs, _ = text.split(":")
        level = 1

        if "busy" in kwargs:
            level = 0
        if "Unknown command" in kwargs:
            level = 2

        self._log.add_log(author, text, level)

    def listPorts(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def set_port(self, port: str):
        self.port = port

    def connect(self):
        if self.port is None:
            return False

        try:
            if not self.connection:
                self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
            return True
        except Exception as e:
            return False

    def disconnect(self):
        self.connection.close()
        self.connection = None
        self.port = None

    def queue_command(self, command):
        self.command_queue.append(command)


if __name__ == "__main__":
    printer = Printer()
    printer.connect()
    printer._interface()
    while True:
        command = input("ender3 > ")
        printer._sendCommand(command)
