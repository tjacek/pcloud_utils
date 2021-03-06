import numpy as np
import cv2,random,csv,os.path
from itertools import chain
from ast import literal_eval 
import frames

def make_dataset_template(in_path,out_path,fun,cut_fun,k=100):
    frames.make_dir(out_path)
    dirs=["dataset","cut"]
    paths={ dir_i:"%s/%s"%(out_path,dir_i) for dir_i in dirs}    
    if(not os.path.exists(paths["dataset"])):
        fun(in_path,paths["dataset"],k)
    if(cut_fun):
        cut_template(paths["dataset"],paths["cut"],cut_fun)    

def cut_template(in_path,out_path,fun):
    reg_dict=read_dict(in_path)
    frames.make_dir(out_path)
    for path_i,reg_i in reg_dict.items():
        print(path_i)
        img_i=cv2.imread(path_i, cv2.IMREAD_GRAYSCALE)
        frame_id="_".join(path_i.split('/')[-2:])
        frame_id= frame_id.replace("..","")
        print(frame_id)
        out_i="%s/%s.png" % (out_path,frame_id)
        print(out_i)
        img_i=fun(img_i,reg_i)
        cv2.imwrite(out_i,img_i)

def train_dataset(reg_dict):
    X,y=[],[]
    for path_i,reg_i in reg_dict.items():
        X.append(cv2.imread(path_i, cv2.IMREAD_GRAYSCALE))
        y.append(list(reg_i))
    X,y=np.array(X),np.array(y)
    X=np.expand_dims(X,axis=-1)
    return X,y

def random_dataset(in_path,out_path,fun,k=100):        
    if(type(k)==int):
        frame_paths=random_paths(in_path,k)
    else:
        frame_paths=all_seqs(in_path)
    dataset={}
    size=len(frame_paths)
    for i,path_i in enumerate(frame_paths):
        print("%d/%d" % (i,size))
        img_i=cv2.imread(path_i, cv2.IMREAD_GRAYSCALE)
        r_i=fun(img_i)
        dataset[path_i]=r_i
    save_dict(dataset,out_path)

def all_seqs(in_path):
    paths=[]
    for path_i in frames.get_dirs(in_path):
        paths_ij=frames.get_dirs(path_i)
        paths.append(random.choice(paths_ij))
    return paths

def random_paths(in_path,k=100):
    paths=[ frames.get_dirs(cat_i)
            for cat_i in frames.get_dirs(in_path)]
    paths=list(chain.from_iterable(paths))
    return [random.choice(paths) for i in range(k)]

def read_dict(in_path):
    with open(in_path, mode='r') as infile:
        reader=csv.reader(infile)
        dataset={rows[0]:literal_eval(rows[1]) 
                    for rows in reader
                        if( len(rows)>1)}
    return dataset

def save_dict(reg_dict,out_path):
    paths=list(reg_dict.keys())
    paths.sort(key=frames.natural_keys) 
    with open(out_path, 'w') as f:  
        w = csv.writer(f)
        for path_i in paths:
            w.writerow((path_i,reg_dict[path_i]))