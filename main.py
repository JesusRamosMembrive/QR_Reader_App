################################################################################
# Author: Jesus Ramos Membrive
# E-Mail: ramos.membrive@gmail.com
################################################################################
import re
import sys
import traceback

import cv2
from pygrabber.dshow_graph import FilterGraph
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from pyzbar import pyzbar
from modules.Video_Thread.VideoThread import Video
from modules.Utils.Get_camera_names import get_camera_connected
from modules.Video_Thread.Supervise_devices_connected import WorkerSupervisorConnection
from QR_READER_Raw_GUI import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    The QMainWindow class provides a main application window.
    Before displaying the screen a basic configuration takes place
    and the module that connects the button signals to the corresponding slots is loaded.
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.video_init_flag = False
        self.current_camera_index: int = 0
        self.worker = None
        self.available_cameras: dict = {}
        self.thread = None
        # CLOSE -> Initial condition
        self.isDirectlyClose = False
        self.__init_daemon_camera_connected()
        # SIGNALS AND SLOTS
        self.ui.pushButton_init.clicked.connect(self.handler_init_stop_video)
        # MAIN WINDOW SHOW
        self.show()

    @pyqtSlot()
    def get_webcam_titles(self) -> None:
        """
        Returns a dictionary of available webcams and their corresponding titles.

        :return: None.
        """
        self.available_cameras = get_camera_connected()
        self.add_cameras_to_list(self.available_cameras)

    def add_cameras_to_list(self, cameras_dict: dict) -> None:
        """
        Adds available cameras to the camera list combo box.

        The function removes disconnected cameras from the combo box, and then adds any new connected cameras to the combo box.
        If the `cameras_dict` parameter is an empty dictionary, the function clears the combo box.

        :param cameras_dict: A dictionary of available webcams and their corresponding titles.
        :return: None
        """

        if not cameras_dict:
            self.ui.comboBox_list_cameras.clear()
            return

        combo_box = self.ui.comboBox_list_cameras
        # Remove disconnected cameras from the QComboBox
        i = 0
        while i < combo_box.count():
            item_text = combo_box.itemText(i)
            if item_text not in cameras_dict.values():

                combo_box.removeItem(i)
            else:
                i += 1

        # Add connected cameras to the QComboBox
        for value in cameras_dict.values():
            if value not in [combo_box.itemText(i) for i in range(combo_box.count())]:
                combo_box.addItem(value)

    def get_current_camera_index(self) -> None:
        """
        Sets the current camera index based on the selected camera in the cameras list combo box.

        :return: None
        """
        for key, value in self.available_cameras.items():
            if self.ui.comboBox_list_cameras.currentText() == value:
                self.current_camera_index = key

    def check_camera_available(self) -> bool:
        """
        Checks if a camera is available for use.

        The function checks if the camera list combo box is empty or if the available cameras dictionary is empty. If either
        condition is true, a warning message is displayed and the function returns False. Otherwise, the function returns True.

        :return: True if a camera is available for use, False otherwise.
        """
        if self.ui.comboBox_list_cameras.size() == 0 or not self.available_cameras:
            QMessageBox.warning(self, "Warning", "There is not any webcam connected", QMessageBox.StandardButton.Ok)
            return False
        return True

    def handler_init_stop_video(self, text_to_show) -> None:
        """
        Initializes or stops the video stream from the selected webcam.
        :param text_to_show: It is the string to be shown in the label of the stream.
        :return: None
        """
        if text_to_show is False:
            text_to_show = "Camera stopped"

        if self.check_camera_available() is False:
            return

        if self.video_init_flag is False:
            self.get_current_camera_index()
            self.__init_video_stream()
            self._handler_video_button_and_flag(
                True, "Stop", "background-color:red"
            )
        elif self.video_init_flag is True:
            self.worker.kill_video = True
            self._handler_video_button_and_flag(
                False, "Start", "background-color:green"
            )
            self.ui.label_live_stream.setText(text_to_show)

    def _handler_video_button_and_flag(self, arg0, arg1, arg2) -> None:
        """
        Updates the video initialization flag and the text and style of the init video button.

        :param arg0: The new value of the video initialization flag.
        :param arg1: The new text for the init video button.
        :param arg2: The new style for the init video button.
        :return: None
        """
        self.video_init_flag = arg0
        self.ui.pushButton_init.setText(arg1)
        self.ui.pushButton_init.setStyleSheet(arg2)

    def __init_video_stream(self) -> None:
        """
        Initializes the video stream from the selected webcam.

        :return: None
        """
        self.thread = QThread()
        self.worker = Video()
        self.worker.camera_index = self.current_camera_index
        self.worker.current_camera_name = self.ui.comboBox_list_cameras.currentText()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.changePixmap.connect(self.setImage)
        self.worker.error.connect(self.handler_no_video)
        self.worker.connection_lost.connect(self.connection_lost)
        self.thread.start()

    def __init_daemon_camera_connected(self):
        """
        Initializes the worker supervisor thread to monitor the availability of connected cameras.

        The function initializes a `WorkerSupervisorConnection` object and moves it to a new `QThread`. The worker supervisor
        monitors the availability of connected cameras and emits a signal when the available cameras change. This signal is
        connected to the `get_webcam_titles` method, which updates the list of available cameras in the UI.

        :return: None
        """
        self.thread_connections = QThread()
        self.worker_supervisor = WorkerSupervisorConnection()
        self.worker_supervisor.moveToThread(self.thread_connections)
        self.thread_connections.started.connect(self.worker_supervisor.run)
        self.worker_supervisor.finished.connect(self.thread_connections.quit)
        self.worker_supervisor.finished.connect(self.worker_supervisor.deleteLater)
        self.thread_connections.finished.connect(self.thread_connections.deleteLater)
        self.worker_supervisor.devices.connect(self.get_webcam_titles)
        self.thread_connections.start()

    @pyqtSlot(QImage)
    def setImage(self, image) -> None:
        """
        Sets the live stream label pixmap with the given image.

        :param image: The image to set as the live stream label pixmap.
        :return: None
        """
        self.ui.label_live_stream.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(str)
    def handler_no_video(self, text: str) -> None:
        """
        Handles the error raised when the selected camera is not valid.

        :return: None
        """
        QMessageBox.critical(self, "Error", text, QMessageBox.StandardButton.Ok)
        self.handler_init_stop_video(text_to_show="")

    def connection_lost(self) -> None:
        """
        Handles the error raised when the connection with the camera is lost.

        :return: None
        """
        QMessageBox.warning(self, "Error", "The connection with camera has benn lost.", QMessageBox.StandardButton.Ok)
        self.handler_init_stop_video(text_to_show="Connection lost")

    # --------------------------------------------------------
    # EVENT-> TO CLOSE THE WINDOW
    # --------------------------------------------------------

    def close(self) -> None:
        """
        Closes the current widget and deletes all its child widgets and global variables.

        :return: None
        """
        for childQWidget in self.findChildren(QWidget):
            QWidget(childQWidget).close()
        self.isDirectlyClose = True
        for name in dir():
            if not name.startswith('_'):
                del globals()[name]
        return super().close()

    def closeEvent(self, eventQCloseEvent) -> None:
        """
        Close the windows and terminate all the connections before close.

        :return:
        """
        if self.isDirectlyClose:
            eventQCloseEvent.accept()
        else:
            answer = QMessageBox.question(
                self,
                'Close the program?',
                'Are you sure?',
                QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.No)
            if (answer == QMessageBox.StandardButton.Yes) or (self.isDirectlyClose is True):
                if self.worker is not None:
                    self.worker.kill_video = True
                eventQCloseEvent.accept()
                sys.exit(0)
            else:
                eventQCloseEvent.ignore()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        MainWindow = MainWindow()
        ui = Ui_MainWindow()
        MainWindow.show()
        sys.exit(app.exec())
    except OSError:
        print(f"Error produced in the init: {traceback.format_exc()}")
