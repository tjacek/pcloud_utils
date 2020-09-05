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

        self.btn = QtWidgets.QPushButton('Show', self)
        self.btn.setGeometry(50, 150, 120, 35)
        self.btn.clicked.connect(self.getComboValue)

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(50, 90)
        self.textbox.resize(280,40)

    def getComboValue(self):
        frame_i=self.comboBox.currentText()
        value_i=self.data_dict[frame_i]
        self.textbox.setText(str(value_i))
        print( dir(self.textbox))
#        print((frame_i,self.data_dict[frame_i]))

in_path="test2/dataset"
data_i=dataset.read_dict(in_path)

app = QtWidgets.QApplication(sys.argv)
demo = ComboBoxDemo(data_i)
demo.show()
sys.exit(app.exec_())