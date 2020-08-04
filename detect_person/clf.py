import numpy as np
import random,keras
from itertools import chain
from keras.models import load_model
import preproc,cnn

def make_dataset(in_path,out_path,k=100):
    selected=random_paths(in_path,k)
    path_dict={ dir_i:("%s/%s" % (out_path,dir_i))  for dir_i in ["neg","pos"]}
    data.make_dir(out_path)
    for dir_i in path_dict.values():
        data.make_dir(dir_i)
    frames=[]
    for path_i in selected:
        frames+=data.read_frames(path_i)
    data.save_frames(frames,path_dict['pos'])

def random_paths(in_path,k=100):
    paths=[ data.get_dirs(cat_i)
            for cat_i in data.get_dirs(in_path)]
    paths=list(chain.from_iterable(paths))
    return [random.choice(paths) for i in range(k)]

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
#    raise Exception(imgs_shape)
    model=cnn.make_model(imgs_shape)
    model.fit(X,y,epochs=n_epochs,batch_size=8)#64)
    if(out_path):
        model.save(out_path)

if __name__=="__main__":
    in_path="../../segm"
    out_path="../../clf"
    data.make_dir(out_path)
    make_dataset(in_path,out_path)