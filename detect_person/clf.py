import numpy as np
import random,data,keras
from itertools import chain
from keras.models import load_model
import preproc,cnn

def make_dataset(in_path,out_path,k=10):
    paths=[ data.get_dirs(cat_i)
            for cat_i in data.get_dirs(in_path)]
    paths=list(chain.from_iterable(paths))
    selected=[random.choice(paths) for i in range(k)]
    path_dict={ dir_i:("%s/%s" % (out_path,dir_i))  for dir_i in ["neg","pos"]}
    data.make_dir(out_path)
    for dir_i in path_dict.values():
        data.make_dir(dir_i)
    frames=[]
    for path_i in selected:
        frames+=data.read_frames(path_i)
    data.save_frames(frames,path_dict['pos'])

def get_persons(in_path,nn_path,out_path):
    model=load_model(nn_path)
    def helper(frames):
        X_i=np.array(preproc.standarize(frames,(96,96)))
        X_i=np.expand_dims(X_i,axis=-1)
        y_true=model.predict(X_i)
        k=np.argmax(y_true[:,1])
        person=np.squeeze(X_i[k] )
        return person
    data.cluster_template(in_path,out_path,helper)

def train_model(in_path,out_path=None,n_epochs=100):
    raw_dict=data.read_dataset(in_path)
    preproc_dict=preproc.preproc_dict(raw_dict)
    X_pos,X_neg=preproc_dict['pos'],preproc_dict['neg']
    y_pos,y_neg=np.repeat(0,len(X_pos)),np.repeat(1,len(X_neg))
    X=np.array(X_pos+X_neg)
    y= keras.utils.to_categorical(np.concatenate([y_pos,y_neg]))
    X=np.expand_dims(X,axis=-1)
    model=cnn.make_model((96,96,1))
    model.fit(X,y,epochs=n_epochs,batch_size=64)
    if(out_path):
        model.save(out_path)

if __name__=="__main__":
    in_path="../grow"
    out_path="../clf"
    data.make_dir(out_path)
    make_dataset(in_path,out_path)