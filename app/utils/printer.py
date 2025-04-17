import serial
import time
import logging
import os
import re
import threading


class Printer:
    def __init__(self, port: str = None, baudrate: int = 115200):
        self.port = None
        self.baudrate = baudrate
        self.connection = None
        self.log = []

        threading.Thread(target=self.listener, daemon=True)

    def listener(self):
        while True:
            if self.connection is not None:
                newLines = self.connection.readlines()
                for line in newLines:
                    self.addLog(line)

    def addLog(self, text):
        self.log.append(
            {
                "text": text,
                "time": time.time(),
            }
        )

    def _listPorts(self):
        if os.name == "posix":
            ports = os.listdir("/dev")
            return [port for port in ports if re.search("USB", port)]
        else:
            return ["proxy1", "proxy2"]

    def setPort(self, port: str):
        self.port = "/dev/" + port

    def _connect(self):
        try:
            if not self.connection:
                self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
                time.sleep(1)
            return True
        except Exception as e:
            print(e)
            return False

    def _sendCommand(self, command):
        print(f"sending command: {command}")
        try:
            self.connection.write(f"{command}\n".encode())
            time.sleep(1)
            res = self.connection.readlines()
            print([line.decode().strip() for line in res])
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    printer = Printer()
    printer._connect()
    while True:
        command = input("ender3 > ")
        printer._sendCommand(command)
