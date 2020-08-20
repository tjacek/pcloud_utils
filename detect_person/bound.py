import numpy as np,os.path
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
    model=cnn.make_regression(img_shape,4)
    model.fit(X,y,epochs=n_epochs,batch_size=16)
    if(out_path):
        model.save(out_path)

#def cut_person(in_path,out_path):
#    def cut(reg_i,img_i):
#        x0,x1= reg_i
#        img_i[:,:x0]=0
#        img_i[:,x1:]=0
#        return img_i
#    dataset.cut_template(in_path,out_path,cut)

def exp(in_path,out_path,use_gui=True,k=100):
    frames.make_dir(out_path)
    dirs=["dataset","cut"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}    
    if(not os.path.exists(paths["dataset"])):
        if(use_gui):
            gui_gen(in_path,paths["dataset"],k=k)
        else:
            dataset.random_dataset(in_path,paths["dataset"],detect_person,k)
#    cut_person(paths["dataset"],paths["cut"])    

def gui_gen(in_path,out_path,k=20):
    bound=gui.get_bound4D() 
    def helper(img_i):
        #position=detect_person(img_i.copy())
        position=[0,0,200,200]
        position=[int(pos_i) for pos_i in position]
        return bound(img_i,position)
    dataset.random_dataset(in_path,out_path,helper,k)

if __name__=="__main__":
    in_path="final"#"../depth"
    out_path="test2"
    exp(in_path,out_path,k=None,use_gui=True)