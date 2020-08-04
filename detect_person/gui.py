import cv2
import frames

class KeyInput(object):
    def __init__(self, code=115):# d key code
        self.code = code

    def __call__(self):
        cv2.imshow('image',img_ij)
        key_ij=cv2.waitKey(0)
        cv2.destroyAllWindows()        
        return  (key_ij==self.code)

class BoundInput(object):
    def __init__(self):
        self.name = 'image'
        self.window=cv2.namedWindow(self.name)
        self.x="X"
        self.y="Y"

    def __call__(self,img_i,x=0,y=0):
        self.show(img_i,x,y)  
        while(True):
            key_j=cv2.waitKey(0)
            x,y=self.get_input()
            if(key_j==115):
                break
            self.cut(img_i,x,y)
        cv2.destroyAllWindows()
        return x,y

    def show(self,img_i,x,y):
        cv2.imshow(self.name,img_i)
        cv2.createTrackbar(self.x,self.name,x,img_i.shape[1],on_action)
        cv2.createTrackbar(self.y,self.name,y,img_i.shape[1],on_action)

    def get_input(self):
        x = cv2.getTrackbarPos(self.x, self.name)
        y = cv2.getTrackbarPos(self.y, self.name)
        return x,y

    def cut(self,img_i,x,y):
        new_img=img_i.copy()
        new_img[:,:x]=0
        new_img[:,y:]=0
        cv2.imshow(self.name,new_img)

def on_action(x):
    pass

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
    key_gui=KeyInput()
    for i,path_i in enumerate(paths):
        print("%d:%s" % (i,path_i))
        pos,neg=[],[]
        imgs_i=frames.read_frames(path_i)
        for img_ij in imgs_i:
            data_i= pos if(key_gui()) else neg
            data_i.append(img_ij)
        name_i=get_id(path_i)        
        frames.save_frames(pos,pos_path,name_i)
        frames.save_frames(neg,neg_path,name_i)

#def reg_gui(paths):
#    if(type(paths)==str):
#        paths=frames.get_dirs(paths)
#    bound_input=BoundInput()
#    for i,path_i in enumerate(paths):
#        print("%d:%s" % (i,path_i))
#        imgs_i=frames.read_frames(path_i)
#        for img_ij in imgs_i:
#            bound_input(img_ij)
#            raise Exception("OK")

if __name__=="__main__":
#   classify_imgs("final","test")
    in_path="../../clean/clf/result"
    seq_path="test"
#   agum_dataset(in_path,seq_path,"agum")
    reg_gui(seq_path)