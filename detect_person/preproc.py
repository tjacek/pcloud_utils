import cv2
import data

def preproc_exp(in_path,out_path):
    d=data.read_dataset(in_path)
    preproc_d=preproc_dir(d)
    data.save_seqs(preproc_d,out_path)

def preproc_dir(data):
    return {name_i: [standarize(frame_i) 
                        for frame_i in data_i] 
                for name_i,data_i in data.items()}

def standarize(img_i,dim=(96,96)):
    x,y,w,h=cv2.boundingRect(img_i)
    if(w<dim[0] or h<dim[1]):
        return None	
    img_i=img_i[x:x+w,y:y+h]
    print(img_i.shape)
    return cv2.resize(img_i,dim)

preproc_exp("dataset","test")