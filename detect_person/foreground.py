import numpy as np
import gui,dataset,cnn,frames

def apply_cut(in_path,nn_path,out_path):
    model=cnn.read_model(nn_path)
    def helper(frame_i):     
        r_i=model.predict(frame_i)
        position=[int(r_i[0][0])]
        return back_cut(frame_i,position) #frame_i
    frames.transform_template(in_path,out_path,helper)    

def exp(in_path,out_path,k=100):
    dataset.make_dataset_template(in_path,out_path,gui_gen,back_cut,k)

def gui_gen(in_path,out_path,k=20):
    rect_gui=get_fore1D() 
    def helper(img_i):
        max_z=int(np.amax(img_i))
        print(max_z)
        position=[max_z]
        return rect_gui(img_i,position)
    dataset.random_dataset(in_path,out_path,helper,k)

def get_fore1D():
    bar_names=["Z"]
    return gui.TrackbarInput(bar_names,back_cut,get_max_z)

def back_cut(img_i,position):
    z=position[0]
    img_i[img_i<z]=0
    return img_i

def get_max_z(img_i):
    return np.amax(img_i)	

if __name__=="__main__":
    in_path="../../forth/frames"#"../depth"
    out_path="../../forth/"
    exp(in_path,out_path,k=None)