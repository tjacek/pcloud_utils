import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
print("physical_devices-------------", len(physical_devices))
tf.config.experimental.set_memory_growth(physical_devices[0], True)
import numpy as np
import keras,cv2
#import data,preproc,cnn,img_segm
import clf
#from keras.models import load_model

def simple_exp(in_path,out_path):
    dirs=["dataset","nn","result"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}
    clf.train_model(paths["dataset"],paths["nn"],n_epochs=1000)
    clf.get_persons(in_path,paths["nn"],paths["result"])



out_path="../../clf"
#train_model(out_path+"/dataset",out_path+"/nn",n_epochs=1000)
#get_persons("test",out_path+"/nn","result")

simple_exp("../grow","../clf")
