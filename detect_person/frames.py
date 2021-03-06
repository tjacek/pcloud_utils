import os,re
import cv2

def transform_template(in_path,out_path,fun,single=True):
    cats=get_dirs(in_path)
    print(cats)
    make_dir(out_path)
    for cat_path_i in cats:
        frames=read_frames(cat_path_i) 
        if(single):
            frames=[fun(frame_i) for frame_i in frames]
        else:
            frames=fun(frames)
        out_i="%s/%s" % (out_path,cat_path_i.split('/')[-1])
        if(frames):
            print(out_i)
            save_frames(frames,out_i)

def cluster_template(in_path,out_path,fun):
    cats=get_dirs(in_path)
    make_dir(out_path)
    for cat_path_i in cats:
        print(cat_path_i)
        frames_path=get_dirs(cat_path_i)
        out_i="%s/%s"  % (out_path, cat_path_i.split("/")[-1])   
        trans_frames=[]
        for frame_path_j in frames_path:
            frames=read_frames(frame_path_j) 
            trans_frames.append(fun(frames))
        save_frames(trans_frames,out_i)

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
    paths=seq_i if(type(seq_i)==list) else get_files(seq_i)
    return [cv2.imread(path_j, cv2.IMREAD_GRAYSCALE)
                for path_j in paths]

def save_frames(frames,out_path,name="frame"):
    make_dir(out_path)
    for i,frame_i in enumerate(frames):
        if(frame_i is None):
            break
        if(type(frame_i)==list):
            out_i="%s/%s_%d" % (out_path,name,i)
            save_frames(frame_i,out_i)
        else:
            out_i="%s/%s_%d.png" % (out_path,name,i)
            cv2.imwrite(out_i,frame_i) 

def get_dirs(in_path):
    return ["%s/%s" %(in_path,dir_i) 
                for dir_i in os.listdir(in_path)]

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def atoi(text):
    return int(text) if text.isdigit() else text

def get_files(in_path):
    all_paths=[]
    for root, directories, filenames in os.walk(in_path):	
        all_paths+=["%s/%s" %(root,file_i) for file_i in filenames]
    all_paths.sort(key=natural_keys)        
    return all_paths

def make_dir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)