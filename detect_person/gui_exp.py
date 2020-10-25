from PyQt5 import QtGui, QtCore, QtWidgets
import cv2,sys
import os.path
from ast import literal_eval 
import dataset,foreground,bound,frames

class State(object):
    def __init__(self,data_dict,path,cut):
        self.data_dict=data_dict
        self.path=path
        self.cut=cut

    def __getitem__(self,frame_i):
        return str(self.data_dict[frame_i])
    
    def keys(self):
        return list(self.data_dict.keys())

    def show(self,frame_i,text_i):
        self.data_dict[frame_i]=text_i
        position=literal_eval(text_i)
        img_i=cv2.imread(frame_i, cv2.IMREAD_GRAYSCALE)
        img_i=self.cut(img_i,position)
        cv2.imshow(frame_i,img_i)

    def save(self,path_i):
        dataset.save_dict(self.data_dict,path_i)

class ComboBoxDemo(QtWidgets.QWidget):

    def __init__(self, state):
        super().__init__()
        self.state=state

        self.delta=50
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(self.delta, 50, 400, 35)
        self.comboBox.addItems(self.state.keys() )
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
        self.pathbox.setText(self.state.path)
        self.getComboValue()

    def getComboValue(self):
        frame_i=self.comboBox.currentText()
        value_i=self.state[frame_i] 
        self.textbox.setText(value_i)

    def show_frame(self):
        frame_i=self.comboBox.currentText()
        text_i=self.textbox.text()
        self.state.show(frame_i,text_i)

    def save(self):
        path_i=self.pathbox.text()
        print("Saves %s" % path_i)
        self.state.save(path_i)

    def closeEvent(self, event):
        in_path,fun=self.state.path,self.state.cut
        out_path="%s/%s" % (os.path.dirname(in_path),"cut")
        dataset.cut_template(in_path,out_path,self.state.cut)

def read_dataset(in_path,default=None):
    if(os.path.isdir(in_path)):
        paths=frames.get_files(in_path)
        data_i={ path_i:default for path_i in paths}
        in_path="%s.csv" % in_path
        dataset.save_dict(data_i,in_path)
    else:
        data_i=dataset.read_dict(in_path)
    return data_i,in_path

def get_rect_gui(in_path):
    default=[30,30,30,30]
    data_i,in_path=read_dataset(in_path,default)
    state=State(data_i,in_path,bound.rect_cut)
    app = QtWidgets.QApplication(sys.argv)
    return ComboBoxDemo(state),app

def get_fore_gui(in_path):
    default=[90]
    data_i,in_path=read_dataset(in_path,default)
    state=State(data_i,in_path,foreground.back_cut)
    app = QtWidgets.QApplication(sys.argv)
    return ComboBoxDemo(state),app

in_path="../../forth/dataset"
#out_path="../../forth/cut"
demo,app=get_fore_gui(in_path)
demo.show()
sys.exit(app.exec_())