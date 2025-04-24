import cv2


class Camera:
    def __init__(self):
        self.source = None
        self.refresh_source()
        pass

    def refresh_source(self):
        self.source = cv2.VideoCapture(0)

    def is_connected(self):
        return self.source.isOpened()

    def gen_frames(self):
        while True:
            success, frame = self.source.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()

                yield (
                    b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
                )
        pass
