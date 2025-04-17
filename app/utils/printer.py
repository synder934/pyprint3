import serial
import time
import logging


class Printer:
    def __init__(self, port: str = None, baudrate: int = 115200):
        self.port = port if port else "/dev/ttyUSB0"
        self.baudrate = baudrate
        self.connection = None

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
