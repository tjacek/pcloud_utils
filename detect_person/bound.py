#import numpy as np,os.path
#from scipy.ndimage import gaussian_filter1d
#from keras.models import load_model
#import dataset,frames,cnn,gui
#import cv2
import gui,dataset

def exp(in_path,out_path,k=100):
    fun=gui_gen
    dataset.make_dataset_template(in_path,out_path,fun,rect_cut,k)

def gui_gen(in_path,out_path,k=20):
    rect_gui=get_bound4D() 
    def helper(img_i):
        size=int(img_i.shape[0]/2)
        position=[0,0,size,size]
        return rect_gui(img_i,position)
    dataset.random_dataset(in_path,out_path,helper,k)

def get_bound4D():
    bar_names=["X","Y","width","height"]
    return gui.TrackbarInput(bar_names, rect_cut)

def rect_cut(img_i,position):
    x,y,width,height=position
    img_i[:,:x]=0
    img_i[:,x+width:]=0
    img_i[:y,:]=0
    img_i[y+height:,:]=0
    return img_i

#def apply_reg(in_path,nn_path,out_path):
#    model=load_model(nn_path)
#    def helper(frame_i):
#        frame_i=frame_i.reshape((1,frame_i.shape[0],frame_i.shape[1],1))
#        r_i=model.predict(frame_i)
#        r_i=model.predict(np.array([np.expand_dims(frame_i,axis=-1)]) )       
#        x0,x1=int(r_i[0][0]),int(r_i[0][1])
#        raise Exception(frame_i.shape)
#        frame_i[:,:x0]=0
#        frame_i[:,x1:]=0
#        return frame_i
#    frames.transform_template(in_path,out_path,helper)

#def train_reg(in_path,out_path,n_epochs=1000):
#    reg_dict=dataset.read_dict(in_path)
#    X,y=dataset.train_dataset(reg_dict)
#    img_shape=(X.shape[1],X.shape[2],1)
#    model=cnn.make_regression(img_shape,4)
#    model.fit(X,y,epochs=n_epochs,batch_size=16)
#    if(out_path):
#        model.save(out_path)

if __name__=="__main__":
    in_path="final"#"../depth"
    out_path="test2"
    exp(in_path,out_path,k=None)