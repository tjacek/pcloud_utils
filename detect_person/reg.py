import data#,img_segm
import cv2,csv
import numpy as np

def reg_dataset(in_path,out_path):
    dataset={}
    seq_dict=data.read_seqs(in_path)
    for cat_i,frames in seq_dict.items():
        for j,frame_j in enumerate(frames):
            y=aprox_floor(frame_j)
            if(y):
               img_id="%s/%s/%d.png"%(in_path,cat_i,j)
               dataset[img_id]=y
    save_dict(dataset,out_path)

def aprox_floor(img_i):
    edges = cv2.Canny(img_i,10,200)
    lines=cv2.HoughLinesP(edges,1,np.pi/180,40,minLineLength=30,maxLineGap=30)
    lines=np.squeeze(lines)
    if(lines.ndim==0):
        return None
    if(lines.ndim==1):
        return lines[0]
    return lines[1][np.argmax(lines[0])]

def cut_floor(in_path,out_path):
    reg_dict=read_dict(in_path)
    data.make_dir(out_path)
    for path_i,reg_i in reg_dict.items():
        img_i=cv2.imread(path_i, cv2.IMREAD_GRAYSCALE)
        out_i="%s/%s.png" % (out_path,path_i.split('/')[-1])
        img_i[int(reg_i):,:]=0
        cv2.imwrite(out_i,img_i)

def read_dict(in_path):
    with open(in_path, mode='r') as infile:
        reader=csv.reader(infile)
        dataset={rows[0]:rows[1] for rows in reader}
    return dataset

def save_dict(reg_dict,out_path):
    with open(out_path, 'w') as f:  
        w = csv.writer(f)
        w.writerows(reg_dict.items())

in_path="../growth/imgs/result"
out_path="test"

reg_dataset(in_path,out_path)
cut_floor("test","out")