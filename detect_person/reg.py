#import cv2
#import numpy as np
#from keras.models import load_model
#from scipy.ndimage import gaussian_filter1d
#import frames,cnn,clf
import gui,dataset

def exp(in_path,out_path,k=100):
    fun=gui_gen
    dataset.make_dataset_template(in_path,out_path,fun,k)

def gui_gen(in_path,out_path,k=20):
    reg_gui=get_bound2D() 
    def helper(img_i):
        position=[0,0]
        return reg_gui(img_i,position)
    dataset.random_dataset(in_path,out_path,helper,k)

def get_bound2D():
    return gui.TrackbarInput(["X","Y"], simple_cut)

def simple_cut(img_i,position):
    x,y=position
    img_i[:,:x]=0
    img_i[:,y:]=0
    return img_i

if __name__=="__main__":
    in_path="final"#"../depth"
    out_path="test2"
    exp(in_path,out_path,k=None)