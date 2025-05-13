class PrintJob:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.__line_number = 0
        self.__paused = False
        self.__stopped = False
