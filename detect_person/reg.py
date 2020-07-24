import cv2,os.path
import numpy as np
from keras.models import load_model
from scipy.ndimage import gaussian_filter1d
import data,cnn,clf

def apply_reg(in_path,nn_path,out_path):
    model=load_model(nn_path)
    def helper(frame_i):
        r_i=model.predict(np.array([np.expand_dims(frame_i,axis=-1)]) )
        print(r_i)
        frame_i[int(r_i):,:]=0
        return frame_i
    data.transform_template(in_path,out_path,helper)

def train_reg(in_path,out_path,n_epochs=1000):
    model=cnn.make_regression(img_shape=(96,96,1))
    reg_dict=read_dict(in_path)
    X,y=data.train_dataset(reg_dict)
    model.fit(X,y,epochs=n_epochs,batch_size=64)
    if(out_path):
        model.save(out_path)    

def random_dataset(in_path,out_path,k=100):
    data.random_dataset(in_path,out_path,detect_floor,k)

def reg_dataset(in_path,out_path):
    dataset={}
    seq_dict=data.read_seqs(in_path)
    for cat_i,frames in seq_dict.items():
        for j,frame_j in enumerate(frames):
            y=detect_floor(frame_j)
            img_id="%s/%s/frame_%d.png"%(in_path,cat_i,j)
            dataset[img_id]=y
    save_dict(dataset,out_path)

def detect_floor(img_i):
    ret,binary = cv2.threshold(img_i,1,255,cv2.THRESH_BINARY)
    binary=cv2.medianBlur(binary,15)
    ts=np.mean(binary,axis=0)
    ts=gaussian_filter1d(ts, 6)
    ts= np.sign(np.diff(ts))
    extr=np.where(np.diff(ts)==-2)
    if(extr[0].shape[0]==0):
        return 96
    k=extr[-1][0]
    return k

#def cut_floor(in_path,out_path):

if __name__=="__main__":
    in_path="../../clf/result"
    out_path="../../reg"
    data.make_dir(out_path)
    dirs=["reg.txt","cut"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}    
    if(not os.path.exists(paths["reg.txt"])):
        random_dataset(in_path,paths["reg.txt"],k=100)    
#    cut_floor(paths["reg.txt"],paths["cut"])