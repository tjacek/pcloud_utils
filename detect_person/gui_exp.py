from PyQt5 import QtGui, QtCore, QtWidgets
import cv2,sys
from ast import literal_eval 
import dataset,foreground

class ComboBoxDemo(QtWidgets.QWidget):

    def __init__(self,data_dict,path):
        super().__init__()
        self.data_dict=data_dict
        self.path=path 
        
        self.delta=50
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(self.delta, 50, 400, 35)
        self.comboBox.addItems(list(data_dict.keys()))
        self.comboBox.currentTextChanged.connect(self.getComboValue)

        self.btn = QtWidgets.QPushButton('Show', self)
        self.btn.setGeometry(self.delta, 4*self.delta, 100, 35)
        self.btn.clicked.connect(self.show_frame)

        self.btn = QtWidgets.QPushButton('Save', self)
        self.btn.setGeometry(3*self.delta, 4*self.delta, 100, 35)
        self.btn.clicked.connect(self.save)

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(50, 90)
        self.textbox.resize(280,40)

        self.pathbox = QtWidgets.QLineEdit(self)
        self.pathbox.move(50, 150)
        self.pathbox.resize(280,40)
        self.pathbox.setText(self.path)

    def getComboValue(self):
        frame_i=self.comboBox.currentText()
        value_i=self.data_dict[frame_i]
        self.textbox.setText(str(value_i))

    def show_frame(self):
        frame_i=self.comboBox.currentText()
        text_i=self.textbox.text()
        self.data_dict[frame_i]=text_i
        position=literal_eval(text_i)
        img_i=cv2.imread(frame_i, cv2.IMREAD_GRAYSCALE)
        img_i=foreground.back_cut(img_i,position)
        cv2.imshow(frame_i,img_i)

    def save(self):
        path_i=self.pathbox.text()
        print("Saves %s" % path_i)
        dataset.save_dict(self.data_dict,path_i)

in_path="test2/dataset"
data_i=dataset.read_dict(in_path)

app = QtWidgets.QApplication(sys.argv)
demo = ComboBoxDemo(data_i,in_path)
demo.show()
sys.exit(app.exec_())