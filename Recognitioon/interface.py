from PIL import ImageQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

__author__ = 'Bio'

import Recognitioon.int as int
import Recognitioon.text as rec

class Interface():
    text = ''
    file_name = ''
    flag = False
    path = ''

    def __init__(self, window):
        self.interface = int.Ui_MainWindow()
        self.interface.setupUi(window)
        self.interface.retranslateUi(window)
        self.scene = QGraphicsScene()
        self.view = self.interface.graphicsView.setScene(self.scene)
        self.interface.b_open.clicked.connect(self.open_img)
        self.interface.b_save.clicked.connect(self.save_text)
        self.interface.b_recognize.clicked.connect(self.recognize)
        self.interface.checkBox.clicked.connect(self.activate)
        self.interface.pushButton.setDisabled(True)
        self.interface.pushButton.clicked.connect(self.choose_directory)

    def choose_directory(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        if dlg.exec_():
            self.path = dlg.selectedFiles()[0]

    def activate(self):
        if self.interface.checkBox.isChecked():
            self.interface.pushButton.setEnabled(True)
            self.flag = True
        else:
            self.flag = False
            self.interface.pushButton.setDisabled(True)

    def save_text(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        if dlg.exec_():
            fileName = dlg.selectedFiles()
            if fileName:
                file = open(fileName[0], 'w')
                file.write(self.text)

    def recognize(self):
        if self.file_name != '':
            self.text = rec.recognize(self.file_name, self.flag, self.path)
            self.interface.textBrowser.setText(self.text)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Bідкрийте зображення!")
            return

    def open_img(self):
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.AnyFile)
        fileName = QFileDialog.getOpenFileName(dlg)
        print(fileName)
        if fileName:
            image = QImage(fileName)
            if image.isNull():
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Неможливо відкрити %s" % fileName)
                return
            else:
                self.display_image(fileName)
                self.file_name = fileName

    def display_image(self, img):
        self.scene.clear()
        pixmap = QPixmap(img)
        pixItem = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(pixItem)
        # self.interface.graphicsView.fitInView(pixItem)
        self.scene.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Interface(window)
    window.show()
    sys.exit(app.exec_())