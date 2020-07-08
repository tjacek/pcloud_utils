import os
import cv2

def read_dataset(in_path):
    seq_paths=get_dirs(in_path)
    return{ path_i.split('/')[-1]:read_frames(path_i) 
                for path_i in seq_paths}

def read_seqs(in_path):
    seq_dict={}
    seq_paths=get_dirs(in_path)
    for seq_i in seq_paths:
        clust=read_frames(seq_i)
        seq_dict[seq_i.split('/')[-1]]=clust
    return seq_dict

def save_seqs(seq_dict,out_path):
    make_dir(out_path)
    for name_i,seq_i in seq_dict.items():
        out_i="%s/%s" % (out_path,name_i)
        save_frames(seq_i,out_i)

def read_frames(seq_i):
    return [cv2.imread(path_j, cv2.IMREAD_GRAYSCALE)
                for path_j in get_files(seq_i)]

def save_frames(frames,out_path):
    make_dir(out_path)
    for i,frame_i in enumerate(frames):
        print(type(frame_i))
        if(not frame_i is None):
             out_i="%s/frame_%d.png" % (out_path,i)
             cv2.imwrite(out_i,frame_i) 

def get_dirs(in_path):
    return ["%s/%s" %(in_path,dir_i) 
                for dir_i in os.listdir(in_path)]

def get_files(in_path):
    all_paths=[]
    for root, directories, filenames in os.walk(in_path):	
        all_paths+=["%s/%s" %(root,file_i) for file_i in filenames]
    return all_paths

def make_dir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)

#d=read_dataset("dataset")
#print(d.keys())