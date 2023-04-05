################################################################################
# Author: Jesus Ramos Membrive
# E-Mail: ramos.membrive@gmail.com
################################################################################
import traceback

import cv2
from pyzbar import pyzbar
from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtGui import QImage


class Video(QObject):
    changePixmap = pyqtSignal(QImage)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._img = None
        self._kill_video = False
        self._frame = None
        self._camera_index = 0
        self.cap = None
        self.counter = 0
        self._current_camera_name = ""

    @property
    def current_camera_name(self):
        return self._current_camera_name

    @current_camera_name.setter
    def current_camera_name(self, value):
        self._current_camera_name = value

    @property
    def kill_video(self):
        return self._kill_video

    @kill_video.setter
    def kill_video(self, value):
        self._kill_video = value

    @property
    def camera_index(self):
        return self._camera_index

    @camera_index.setter
    def camera_index(self, value):
        self._camera_index = value

    @staticmethod
    def detect_qr_codes(frame):
        # Find QR codes in the frame
        qr_codes = pyzbar.decode(frame)

        # Draw a green rectangle around each detected QR code
        for qr_code in qr_codes:
            x, y, w, h = qr_code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return frame

    @staticmethod
    def decode_qr_code(image):
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            print("Tipo:", obj.type)
            print("Datos:", obj.data.decode("utf-8"))
            print("Datos-tipo:", type(obj.data.decode("utf-8")))
            print("\n")

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            self.error.emit("No camera detected")
            self.cap.release()
            self.finished.emit()

        # Get the camera's resolution
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while True:
            try:
                if self.kill_video is True:
                    self.cap.release()
                    self.finished.emit()
                    break
                # global frame
                ret, frame = self.cap.read()
                self.decode_qr_code(frame)
                frame = self.detect_qr_codes(frame)  # Add this line to process the frame for QR codes
                if ret:
                    # https://stackoverflow.com/a/55468544/6622587
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
                    p = convertToQtFormat.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
                    self.changePixmap.emit(p)
            except Exception as e:
                self.error.emit("Connection lost")
                self.kill_video = True
                print(e)
