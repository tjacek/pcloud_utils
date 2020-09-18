import cv2
from collections import defaultdict

def preproc_exp(in_path,out_path):
    d=data.read_dataset(in_path)
    preproc_d=preproc_dict(d)
    data.save_seqs(preproc_d,out_path)

def preproc_clusters(cluster_dict):
    preproc_dict=defaultdict(lambda :{})
    for cat_i,frame_dict_i in cluster_dict.items():
        for frame_j,segm_k in frame_dict_i.items():
            preproc_dict[cat_i][frame_j]=standarize(segm_k)	
    return preproc_dict

def preproc_dict(data):
    return {name_i: standarize(data_i) 
                for name_i,data_i in data.items()}

def standarize(img_i,dim=(96,96)):
    if(type(img_i)==list):
        return [ standarize(img_ij) for img_ij in img_i]
    x,y,w,h=cv2.boundingRect(img_i)
    w=dim[1] if( w<dim[1]) else w
    h=dim[0] if( h<dim[0]) else h
    x=img_i.shape[1]-w if(img_i.shape[1]<(x+w)) else x
    y=img_i.shape[0]-h if(img_i.shape[0]<(y+h)) else y
    img_i=img_i[x:x+w,y:y+h]
    return cv2.resize(img_i,dim)

if __name__ == "__main__":
    preproc_exp("dataset","test")