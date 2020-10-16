#import numpy as np
#import random,keras
#from itertools import chain
#from keras.models import load_model
#import preproc,cnn
import frames

def make_dataset(in_path,out_path):
    paths=frames.get_dict(in_path)    
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

def no_action_split(seq_i):
    neg=[seq_i[0],seq_i[-1]]
    center=int(len(seq_i)/2)
    pos=[seq_i[center]]
    return neg,pos

def get_persons(in_path,nn_path,out_path,imgs_shape=None):
    model=load_model(nn_path)
    def helper(frames):
        if(imgs_shape):
            frames= preproc.standarize(frames,imgs_shape) 
        X_i=np.array(frames)
        X_i=np.expand_dims(X_i,axis=-1)
        y_true=model.predict(X_i)
        k=np.argmax(y_true[:,1])
        person=np.squeeze(X_i[k] )
        return person
    data.cluster_template(in_path,out_path,helper)

def train_model(in_path,out_path=None,n_epochs=100,imgs_shape=None):
    raw_dict=data.read_dataset(in_path)
    preproc_dict=preproc.preproc_dict(raw_dict) if(imgs_shape) else raw_dict
    X_pos,X_neg=preproc_dict['pos'],preproc_dict['neg']
    y_pos,y_neg=np.repeat(0,len(X_pos)),np.repeat(1,len(X_neg))
    X=np.array(X_pos+X_neg)
    y= keras.utils.to_categorical(np.concatenate([y_pos,y_neg]))
    X=np.expand_dims(X,axis=-1)
    imgs_shape=(imgs_shape[0],imgs_shape[1],1) if(imgs_shape) else (X.shape[1],X.shape[2],1) 
    model=cnn.make_model(imgs_shape)
    model.fit(X,y,epochs=n_epochs,batch_size=8)#64)
    if(out_path):
        model.save(out_path)

if __name__=="__main__":
    in_path="../../box"
    out_path="dataset"
#    data.make_dir(out_path)
    make_dataset(in_path,out_path)