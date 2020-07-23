import numpy as np
from scipy.ndimage import gaussian_filter1d
import dataset,frames

#def aprox_bound(in_path,out_path):
#	frames.transform_template(in_path,out_path,fun)

def random_dataset(in_path,out_path,k=100):
    dataset.random_dataset(in_path,out_path,detect_person,k)

def cut_person(in_path,out_path):
    def helper(reg_i,img_i):
#        raise Exception( type(reg_i ))
        x0,x1= reg_i#int(reg_i[0]),int(reg_i[1])
        img_i[:,:x0]=0
        img_i[:,x1:]=0
        return img_i
    dataset.cut_template(in_path,out_path,helper)

def detect_person(img_i):
    img_i[img_i!=0]=1
    ts_i=np.mean(img_i,axis=0)
    ts_i=gaussian_filter1d(ts_i, 6)    
    x0,x1=get_inflected(ts_i)
#    plot_i=bar_plot(ts_i)
#    plot_i[:,:x0]=0
#    plot_i[:,x1:]=0
    return x0,x1

def get_inflected(ts_i):
    max_ts=np.argmax(ts_i)
    diff_i=np.diff(ts_i)
    extr_i= np.abs( np.diff(np.sign(diff_i)))
    extr_i=np.where(extr_i==2)
    if(extr_i[0].shape[0]==0):
        return 0,ts_i.shape[0]
    extr_i=extr_i[0]
    left=np.argmax( extr_i>max_ts)
    x0,x1= extr_i[left-2],extr_i[left] 
    return x0,x1

def bar_plot(ts_i):
    plot_i=np.zeros((100,ts_i.shape[0]))
    for j,value_j in enumerate(ts_i):
        k=int( (1.0-value_j) *100)
        plot_i[k:,j]=100
    return plot_i

#aprox_bound("raw","test")
#random_dataset("raw","dataset.txt",k=100)
cut_person("dataset.txt","person")