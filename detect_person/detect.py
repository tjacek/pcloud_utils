import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
print("physical_devices-------------", len(physical_devices))
tf.config.experimental.set_memory_growth(physical_devices[0], True)
import numpy as np
import keras,cv2
import clf,reg,bound

def clf_exp(in_path,out_path,n_epochs=100):
    dirs=["dataset","nn","result"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}
    clf.train_model(paths["dataset"],paths["nn"],n_epochs=n_epochs)
    clf.get_persons(in_path,paths["nn"],paths["result"])

def reg_exp(in_path,out_path):
    dirs=["reg.txt","nn","result"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}
    reg.train_reg(paths["reg.txt"],paths["nn"],n_epochs=1000)
    reg.apply_reg(in_path,paths["nn"],paths["result"])

def bound_exp(in_path,out_path):
    dirs=["dataset","nn","result"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}
    bound.train_reg(paths["dataset"],paths["nn"],n_epochs=1000)
#    bound.apply_reg(in_path,paths["nn"],paths["result"])

in_path="../../clean/clf/result"
out_path="test2"
bound_exp(in_path,out_path)
