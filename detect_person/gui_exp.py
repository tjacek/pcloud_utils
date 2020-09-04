from PyQt5 import QtGui, QtCore, QtWidgets
import cv2
import sys
import dataset

class ComboBoxDemo(QtWidgets.QWidget):

    def __init__(self,data_dict):
        super().__init__()
        self.data_dict=data_dict

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(50, 50, 400, 35)
        self.comboBox.addItems(list(data_dict.keys()))

        self.btn = QtWidgets.QPushButton('Click', self)
        self.btn.setGeometry(170, 120, 120, 35)
        self.btn.clicked.connect(self.getComboValue)

    def getComboValue(self):
        frame_i=self.comboBox.currentText()
        print((frame_i,self.data_dict[frame_i]))#self.comboBox.currentIndex()))

in_path="test2/dataset"
data_i=dataset.read_dict(in_path)

app = QtWidgets.QApplication(sys.argv)
demo = ComboBoxDemo(data_i)
demo.show()
sys.exit(app.exec_())