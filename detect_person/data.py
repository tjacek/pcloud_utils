import os,re
import cv2

def transform_template(in_path,out_path,fun,single=True):
    cats=get_dirs(in_path)
    files.make_dir(out_path)
    for cat_path_i in cats:
        frames=read_frames(cat_path_j) 
        if(single):
            frames=[fun(frame_i) for frame_i in frames]
        else:
            frames=fun(frames)
        out_i="%s/%s" % (out_path,cat_path_i.split('/')[-1])
        save_frames(frames,out_i)
       
def read_clusters(in_path):
    cats=get_dirs(in_path)
    clusters={}
    for cat_i in cats:
        cat_id=cat_i.split("/")[-1]
        clusters[cat_id]={frame_j.split("/")[-1]:read_frames(frame_j) 
                            for frame_j in get_dirs(cat_i)}
    return clusters

def save_clusters(cluster_dict,out_path):
    make_dir(out_path)
    for name_i,seq_i in cluster_dict.items():
        out_i="%s/%s" % (out_path,name_i)
        make_dir(out_i)
        for j,frame_j in enumerate(seq_i):
            out_j="%s/%d" %(out_i,j)
            save_frames(frame_j,out_j)

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
        if(not frame_i is None):
             out_i="%s/frame_%d.png" % (out_path,i)
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