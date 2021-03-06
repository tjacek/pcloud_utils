import numpy as np
import frames,gui,dataset,cnn

def apply_reg(in_path,nn_path,out_path):
    model=cnn.get_model(nn_path)
    def helper(frame_i):       
        r_i=model.predict(frame_i)
        position=int(r_i[0][0]),int(r_i[0][1])
        return simple_cut(frame_i,position) #frame_i
    frames.transform_template(in_path,out_path,helper)

def exp(in_path,out_path,k=100):
    fun=gui_gen
    dataset.make_dataset_template(in_path,out_path,fun,simple_cut,k)

def gui_gen(in_path,out_path,k=20):
    reg_gui=get_bound2D() 
    def helper(img_i):
        position=[0,int(img_i.shape[0]/2)]
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