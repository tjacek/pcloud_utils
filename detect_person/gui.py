import cv2
import frames

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
        print(len(neg))
        break

classify_imgs("final","test")