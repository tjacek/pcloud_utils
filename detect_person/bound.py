import numpy as np,os.path
from scipy.ndimage import gaussian_filter1d
from keras.models import load_model
import dataset,frames,cnn,gui
import cv2

def apply_reg(in_path,nn_path,out_path):
    model=load_model(nn_path)
    def helper(frame_i):
        r_i=model.predict(np.array([np.expand_dims(frame_i,axis=-1)]) )
        x0,x1=int(r_i[0][0]),int(r_i[0][1])
        print(r_i)
        frame_i[:,:x0]=0
        frame_i[:,x1:]=0
        return frame_i
    frames.transform_template(in_path,out_path,helper)

def train_reg(in_path,out_path,n_epochs=1000):
    reg_dict=dataset.read_dict(in_path)
    X,y=dataset.train_dataset(reg_dict)
    img_shape=(X.shape[1],X.shape[2],1)
    model=cnn.make_regression(img_shape,2)
    model.fit(X,y,epochs=n_epochs,batch_size=16)
    if(out_path):
        model.save(out_path)

def cut_person(in_path,out_path):
    def cut(reg_i,img_i):
        x0,x1= reg_i
        img_i[:,:x0]=0
        img_i[:,x1:]=0
        return img_i
    dataset.cut_template(in_path,out_path,cut)

def detect_person(img_i):
    img_i[img_i!=0]=1
    ts_i=np.mean(img_i,axis=0)
    ts_i=gaussian_filter1d(ts_i, 6)    
    x0,x1=get_inflected(ts_i)
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
    if(left<2):
        return 0,ts_i.shape[0]
    x0,x1= extr_i[left-2],extr_i[left] 
    return x0,x1

def bar_plot(ts_i):
    plot_i=np.zeros((100,ts_i.shape[0]))
    for j,value_j in enumerate(ts_i):
        k=int( (1.0-value_j) *100)
        plot_i[k:,j]=100
    return plot_i

def exp(in_path,out_path,use_gui=True,k=100):
    frames.make_dir(out_path)
    dirs=["dataset","cut"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}    
    if(not os.path.exists(paths["dataset"])):
        if(use_gui):
            gui_gen(in_path,paths["dataset"],k=k)
        else:
            dataset.random_dataset(in_path,paths["dataset"],detect_person,k)
    cut_person(paths["dataset"],paths["cut"])    

def gui_gen(in_path,out_path,k=20):
    bound=gui.BoundInput() 
    def helper(img_i):
        position=detect_person(img_i.copy())
        position=[int(pos_i) for pos_i in position]
        return bound(img_i,position)
    dataset.random_dataset(in_path,out_path,helper,k)

if __name__=="__main__":
    in_path="../depth"
    out_path="test2"
    exp(in_path,out_path,k=None,use_gui=True)