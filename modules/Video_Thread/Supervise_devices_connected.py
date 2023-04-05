################################################################################
# Author: Jesus Ramos Membrive
# E-Mail: ramos.membrive@gmail.com
################################################################################
from time import sleep
from PyQt6.QtCore import pyqtSignal, QObject
from modules.Utils.Get_camera_names import get_camera_connected


class WorkerSupervisorConnection(QObject):
    error = pyqtSignal()
    finished = pyqtSignal()
    state = pyqtSignal(bool)
    devices = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stop = False

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, value):
        self._stop = value

    def run(self):
        while True:

            if self._stop is False:
                self.finished.emit()

            self.devices.emit()
            sleep(0.1)

