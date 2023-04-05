# Form implementation generated from reading ui file 'QR_READER.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 500)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_QRCode = QtWidgets.QGroupBox(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_QRCode.sizePolicy().hasHeightForWidth())
        self.groupBox_QRCode.setSizePolicy(sizePolicy)
        self.groupBox_QRCode.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_QRCode.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_QRCode.setObjectName("groupBox_QRCode")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_QRCode)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_live_stream = QtWidgets.QLabel(parent=self.groupBox_QRCode)
        self.label_live_stream.setObjectName("label_live_stream")
        self.gridLayout_3.addWidget(self.label_live_stream, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_QRCode, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 80))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_init = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton_init.setObjectName("pushButton_init")
        self.gridLayout.addWidget(self.pushButton_init, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox_list_cameras = QtWidgets.QComboBox(parent=self.groupBox)
        self.comboBox_list_cameras.setObjectName("comboBox_list_cameras")
        self.horizontalLayout.addWidget(self.comboBox_list_cameras)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionWebSockt = QtGui.QAction(parent=MainWindow)
        self.actionWebSockt.setObjectName("actionWebSockt")
        self.actionSocket = QtGui.QAction(parent=MainWindow)
        self.actionSocket.setObjectName("actionSocket")
        self.actionAPIs = QtGui.QAction(parent=MainWindow)
        self.actionAPIs.setObjectName("actionAPIs")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QR Code Generator"))
        self.groupBox_QRCode.setTitle(_translate("MainWindow", "QR Code Reader"))
        self.label_live_stream.setText(_translate("MainWindow", "No camera connected."))
        self.groupBox.setTitle(_translate("MainWindow", "Controls"))
        self.pushButton_init.setText(_translate("MainWindow", "Init"))
        self.label_2.setText(_translate("MainWindow", "Camera availables"))
        self.actionWebSockt.setText(_translate("MainWindow", "WebSocket"))
        self.actionSocket.setText(_translate("MainWindow", "Socket"))
        self.actionAPIs.setText(_translate("MainWindow", "APIs"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
