import os
import cv2

def read_seqs(in_path):
    seq_dict={}
    seq_paths=get_dirs(in_path)
    for seq_i in seq_paths:
        clust=[cv2.imread(path_j, cv2.IMREAD_GRAYSCALE)
                    for path_j in get_files(seq_i)]
        seq_dict[seq_i.split('/')[-1]]=clust
    return seq_dict

def get_dirs(in_path):
    return ["%s/%s" %(in_path,dir_i) 
                for dir_i in os.listdir(in_path)]

def get_files(in_path):
    all_paths=[]
    for root, directories, filenames in os.walk(in_path):	
        all_paths+=["%s/%s" %(root,file_i) for file_i in filenames]
    return all_paths

read_seqs("../out")