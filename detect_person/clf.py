import numpy as np
import keras#random
#from itertools import chain
from keras.models import load_model
import cnn#preproc
import frames,dataset

def make_dataset(in_path,out_path):
    paths=frames.get_dirs(in_path)    
    seqs=[frames.get_files(path_i) for path_i in paths]
    pos,neg=[],[]
    for seq_i in seqs:
        pos_i,neg_i=no_action_split(seq_i)
        pos+=pos_i
        neg+=neg_i
    frames.make_dir(out_path)
    for i,cat in enumerate([pos,neg]):
        cat_path="%s/%d" % (out_path,i)
        frames_i=frames.read_frames(cat)
        frames.save_frames(frames_i,cat_path)
        print(cat_path)

def read_clf_dataset(in_path):
    dataset=frames.read_dataset(in_path)
    X,y=[],[]
    for i,cat_i in enumerate(dataset.keys()):
        for frame_j in dataset[cat_i]:
            X.append(frame_j)
            y.append(i)
    y=keras.utils.to_categorical(y)
    return np.array(X),y

def no_action_split(seq_i):
    neg=[seq_i[0],seq_i[-1]]
    center=int(len(seq_i)/2)
    pos=[seq_i[center]]
    return neg,pos

def train_model(in_path,out_path=None,n_epochs=100,imgs_shape=None):
    X,y=read_clf_dataset(in_path)
    X=np.expand_dims(X,axis=-1)
    n_cats=y.shape[-1]
    img_shape=(128,128,1)
    model=cnn.make_model(img_shape=img_shape,n_cats=n_cats)
    model.fit(X,y,epochs=n_epochs,batch_size=8)
    if(out_path):
        model.save(out_path)

def filtr_seg(in_path,nn_path,out_path):
    model=load_model(nn_path)
    dataset=frames.read_dataset(in_path)
    frames.make_dir(out_path)
    for name_i,seq_i in dataset.items():
        print(name_i)
        seq_i=np.array(seq_i)
        seq_i=np.expand_dims(seq_i,axis=-1)
        result_i=model.predict(seq_i)
        no_action=np.argmax(result_i,axis=1)
        new_seq=[np.squeeze(seq_i[k])  
                    for k,no_action in enumerate(no_action)
                       if(no_action==0)]
        out_i="%s/%s" % (out_path,name_i)
        frames.save_frames(new_seq,out_i)

if __name__=="__main__":
    in_path="../../box"
    out_path="dataset"
#    make_dataset(in_path,out_path)
#    train_model("dataset",out_path="nn")
    filtr_seg(in_path,"nn","out")