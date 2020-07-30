import cv2
import frames

def agum_dataset(in_path,seg_path):
    selected_paths=set([ path_i.split("/")[-1] 
                        for path_i in frames.get_dirs(seg_path)])
    seq_paths=[path_i for path_i in frames.get_dirs(in_path)
                if( get_id(path_i) in selected_paths)]
    print(seq_paths)
#    print(selected_paths)

def get_id(path_i):
    name_i= path_i.split("/")[-1]
    return "_".join(name_i.split("_")[-2:])

def classify_imgs(in_path,out_path):
    paths=frames.get_dirs(in_path)
    pos,neg=[],[]
    frames.make_dir(out_path)
    for path_i in paths:
        imgs_i=frames.read_frames(path_i)
        for img_ij in imgs_i:
            cv2.imshow('image',img_ij)
            key_ij=cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(key_ij)
            if(key_ij==100):
                pos.append(img_ij)
            else:
            	neg.append(img_ij)
    frames.save_frames(pos,"%s/%s" % (out_path,"pos"))
    frames.save_frames(neg,"%s/%s" % (out_path,"neg"))

#classify_imgs("final","test")
in_path="../../clean/clf/result"
seq_path="test"
agum_dataset(in_path,seq_path)