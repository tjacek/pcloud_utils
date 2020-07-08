import numpy as np
import keras
import data,preproc,cnn

def train_model(in_path,out_path=None,n_epochs=100):
    raw_dict=data.read_dataset(in_path)
    preproc_dict=preproc.preproc_dict(raw_dict)
    X_pos,X_neg=preproc_dict['pos'],preproc_dict['neg']
    y_pos,y_neg=np.repeat(1,len(X_pos)),np.repeat(0,len(X_neg))
    X=np.array(X_pos+X_neg)
    y= keras.utils.to_categorical(np.concatenate([y_pos,y_neg]))
    X=np.expand_dims(X,axis=-1)
    model=cnn.make_model((96,96,1))
    model.fit(X,y,epochs=n_epochs,batch_size=y.shape[0])
    if(out_path):
        model.save(out_path)

train_model("dataset","nn")