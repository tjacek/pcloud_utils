import cv2,csv,os.path
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
    X,y=[],[]
    for path_i,reg_i in reg_dict.items():
        X.append(cv2.imread(path_i, cv2.IMREAD_GRAYSCALE))
        y.append(float(reg_i))
    X,y=np.array(X),np.array(y)
    X=np.expand_dims(X,axis=-1)
    model.fit(X,y,epochs=n_epochs,batch_size=64)
    if(out_path):
        model.save(out_path)    

def random_dataset(in_path,out_path,k=100):
    frame_paths=clf.random_paths(in_path,k)
    dataset={}
    for path_i in frame_paths:
        img_i=cv2.imread(path_i, cv2.IMREAD_GRAYSCALE)
        r_i=detect_floor(img_i)
        dataset[path_i]=r_i
    save_dict(dataset,out_path)

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
#    def helper(img_i):
#        k=detect_floor(img_i)
#        img_i[k:,:]=0
#        return img_i
#    data.transform_template(in_path,out_path,helper)

def cut_floor(in_path,out_path):
    reg_dict=read_dict(in_path)
    data.make_dir(out_path)
    for path_i,reg_i in reg_dict.items():
        print(path_i)
        img_i=cv2.imread(path_i, cv2.IMREAD_GRAYSCALE)
        frame_id="_".join(path_i.split('/')[-2:])
        frame_id= frame_id.replace("..","")
        print(frame_id)
        out_i="%s/%s.png" % (out_path,frame_id)
        print(out_i)
        img_i[int(reg_i):,:]=0
        cv2.imwrite(out_i,img_i)

def read_dict(in_path):
    with open(in_path, mode='r') as infile:
        reader=csv.reader(infile)
        dataset={rows[0]:rows[1] for rows in reader
                    if( len(rows)>1)}
    return dataset

def save_dict(reg_dict,out_path):
    paths=list(reg_dict.keys())
    paths.sort(key=data.natural_keys) 
    with open(out_path, 'w') as f:  
        w = csv.writer(f)
        for path_i in paths:
            w.writerow((path_i,reg_dict[path_i]))
#        w.writerows(reg_dict.items())

if __name__=="__main__":
    in_path="../../clf/result"
    out_path="../../reg"
    data.make_dir(out_path)
    dirs=["reg.txt","cut"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}    
    if(not os.path.exists(paths["reg.txt"])):
        random_dataset(in_path,paths["reg.txt"],k=100)    
    cut_floor(paths["reg.txt"],paths["cut"])