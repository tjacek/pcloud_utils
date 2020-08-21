import cv2
import frames,dataset

class KeyInput(object):
    def __init__(self, code=115):# d key code
        self.code = code

    def __call__(self,img_ij):
        cv2.imshow('image',img_ij)
        key_ij=cv2.waitKey(0)
        cv2.destroyAllWindows()        
        return  (key_ij==self.code)

class TrackbarInput(object):
    def __init__(self,bar_names,cut_fun):
        self.name = 'image'
        self.window=cv2.namedWindow(self.name)
        self.bar_names=bar_names#["X","Y"]
        self.cut_fun=cut_fun#simple_cut

    def __call__(self,img_i,position):
        self.show(img_i,position)  
        while(True):
            key_j=cv2.waitKey(0)
            position=self.get_input()
            if(key_j==115):
                break
            self.cut(img_i,position)
        cv2.destroyAllWindows()
        return position

    def show(self,img_i,start):
        cv2.imshow(self.name,img_i)
        size=img_i.shape[1]
        for j,bar_j in enumerate(self.bar_names):
            cv2.createTrackbar(bar_j,self.name,start[j],size,on_action)

    def get_input(self):
        return [cv2.getTrackbarPos(bar_j, self.name) 
                    for bar_j in self.bar_names]

    def cut(self,img_i,position):
        new_img=img_i.copy()
        new_img=self.cut_fun(new_img,position)
        cv2.imshow(self.name,new_img)

def on_action(x):
    pass

def get_bound4D():
    bar_names=["X","Y","width","height"]
    return TrackbarInput(bar_names, rect_cut)

def rect_cut(img_i,position):
    x,y,width,height=position
    img_i[:,:x]=0
    img_i[:,x+width:]=0
    img_i[:y,:]=0
    img_i[y+height:,:]=0
    return img_i

def agum_dataset(in_path,seg_path,out_path):
    selected_paths=set([ path_i.split("/")[-1] 
                        for path_i in frames.get_dirs(seg_path)])
    seq_paths=[path_i for path_i in frames.get_dirs(in_path)
                if( get_id(path_i) in selected_paths)]
    classify_imgs(seq_paths,out_path)

def get_id(path_i):
    name_i= path_i.split("/")[-1]
    return "_".join(name_i.split("_")[-2:])

def show_imgs(in_path):
    paths=dataset.all_seqs(in_path)
    key_gui=KeyInput()
    for i,img_i in enumerate(frames.read_frames(paths)):
        print("%d" % i)
        key_gui(img_i)

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
            data_i= pos if(key_gui(img_ij)) else neg
            data_i.append(img_ij)
        name_i=get_id(path_i)        
        frames.save_frames(pos,pos_path,name_i)
        frames.save_frames(neg,neg_path,name_i)

if __name__=="__main__":
#   classify_imgs("final","test")
    in_path="final"#"../../clean/reg/result"
    show_imgs(in_path)