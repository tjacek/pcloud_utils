import cv2
import frames

def agum_dataset(in_path,seg_path,out_path):
    selected_paths=set([ path_i.split("/")[-1] 
                        for path_i in frames.get_dirs(seg_path)])
    seq_paths=[path_i for path_i in frames.get_dirs(in_path)
                if( get_id(path_i) in selected_paths)]
    classify_imgs(seq_paths,out_path)

def get_id(path_i):
    name_i= path_i.split("/")[-1]
    return "_".join(name_i.split("_")[-2:])

def classify_imgs(paths,out_path):
    if(type(paths)==str):
        paths=frames.get_dirs(paths)
    frames.make_dir(out_path)
    pos_path,neg_path=["%s/%s" % (out_path,name_i)
                         for name_i in ["pos","neg"]]
    for i,path_i in enumerate(paths):
        print("%d:%s" % (i,path_i))
        pos,neg=[],[]
        imgs_i=frames.read_frames(path_i)
        for img_ij in imgs_i:
            cv2.imshow('image',img_ij)
            key_ij=cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(key_ij)
            if(key_ij==115):# d key code
                pos.append(img_ij)
            else:
            	neg.append(img_ij)
        name_i=get_id(path_i)        
        frames.save_frames(pos,pos_path,name_i)
        frames.save_frames(neg,neg_path,name_i)

#classify_imgs("final","test")
in_path="../../clean/clf/result"
seq_path="test"
agum_dataset(in_path,seq_path,"agum")