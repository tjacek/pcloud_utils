import numpy as np
import keras
import data,preproc,cnn
from keras.models import load_model

def get_persons(in_path,nn_path,out_path):
    model=load_model(nn_path)
    seq_dict=data.read_seqs(in_path)
    seq_dict=preproc.preproc_dict(seq_dict)
    data.make_dir(out_path)
    for name_i,seq_i in seq_dict.items():
        X_i=np.array(seq_i)
        X_i=np.expand_dims(X_i,axis=-1)
        y_true=model.predict(X_i)
        y_true=np.argmax(y_true,axis=1)
        indcs=np.nonzero(y_true)[0]
        filtered_X=np.array([X_i[i] for i in indcs])
        filtered_X=np.squeeze(filtered_X)
        out_i="%s/%s" % (out_path,name_i)
        data.save_frames(filtered_X,out_i)

    #print(len(seq_dict['A']))

#def filtr_positives(y_true):
#    y_true[]

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

#train_model("dataset","nn",n_epochs=1000)
get_persons("../out","nn","result")