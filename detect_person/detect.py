import numpy as np
import keras,cv2
import data,preproc,cnn
from keras.models import load_model

def get_persons(in_path,nn_path,out_path):
    clust_dict=data.read_clusters(in_path)
    preproc_dict=preproc.preproc_clusters(clust_dict)
    model=load_model(nn_path)
    data.make_dir(out_path)
    for cat_i,cat_dict_i in preproc_dict.items():
        cat_path="%s/%s" % (out_path,cat_i)
        data.make_dir(cat_path)
        for frame_j,segm_j in cat_dict_i.items():
            X_i=np.array(segm_j)
            X_i=np.expand_dims(X_i,axis=-1)
            y_true=model.predict(X_i)
            y_true=np.nonzero(np.argmax(y_true,axis=1))[0]
            if(y_true.shape[0]==1):
                person_segm_j=np.squeeze(X_i[y_true[0]])
                out_ij="%s/%s.png"%(cat_path,frame_j)
                cv2.imwrite(out_ij,person_segm_j) 

def train_model(in_path,out_path=None,n_epochs=100):
    raw_dict=data.read_dataset(in_path)
    preproc_dict=preproc.preproc_dict(raw_dict)
    X_pos,X_neg=preproc_dict['pos'],preproc_dict['neg']
    y_pos,y_neg=np.repeat(0,len(X_pos)),np.repeat(1,len(X_neg))
    X=np.array(X_pos+X_neg)
    y= keras.utils.to_categorical(np.concatenate([y_pos,y_neg]))
    X=np.expand_dims(X,axis=-1)
    model=cnn.make_model((96,96,1))
    model.fit(X,y,epochs=n_epochs,batch_size=y.shape[0])
    if(out_path):
        model.save(out_path)

#train_model("dataset","nn",n_epochs=1000)
get_persons("../segm","nn","result")