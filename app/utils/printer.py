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
        self._log: LogBook = LogBook()
        self.command_queue: list[dict] = []

        interface = threading.Thread(target=self._interface, daemon=True)
        interface.start()

    def _interface(self):
        while True:
            try:
                # send all queued commands
                while len(self.command_queue):
                    command = self.command_queue.pop(0)
                    self.addLog("USER", command)
                    if self.connection is not None:
                        self.connection.write(command)
                    else:
                        self.addLog("SERVER", "printer is offline")

                if self.connection is not None:

                    # read all data from port
                    newLines = self.connection.readlines()
                    for line in newLines:
                        self.addLog("PRINTER", line.decode().strip())
            except:
                pass

    def getLogText(self):
        return str(self._log).splitlines()

    def addLog(self, author, text):
        self._log.add_log(author, text, 1)

    def _listPorts(self):
        return [port.location for port in serial.tools.list_ports.comports()]

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

    def queue_command(self, command):
        self.command_queue.append(command)

    def _send_command(self, command):
        try:
            self.connection.write(f"{command}\n".encode())
            return True
        except Exception as e:
            return False


if __name__ == "__main__":
    printer = Printer()
    printer.connect()
    printer._interface()
    while True:
        command = input("ender3 > ")
        printer._sendCommand(command)
