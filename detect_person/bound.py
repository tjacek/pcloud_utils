import numpy as np
import gui,dataset,cnn,frames

def train_reg(in_path,out_path,n_epochs=1000):
    reg_dict=dataset.read_dict(in_path)
    X,y=dataset.train_dataset(reg_dict)
    img_shape=(X.shape[1],X.shape[2],1)
    model=cnn.make_regression(img_shape,4)
    model.fit(X,y,epochs=n_epochs,batch_size=16)
    if(out_path):
        model.save(out_path)

def apply_reg(in_path,nn_path,out_path):
    model=cnn.read_model(nn_path)
    def helper(frame_i):     
        r_i=model.predict(frame_i)
        position=[int(r_i[0][i]) for i in range(4)]
        return rect_cut(frame_i,position) #frame_i
    frames.transform_template(in_path,out_path,helper)    

def apply_box(in_path,nn_path,out_path):
    model=cnn.read_model(nn_path)
    def helper(frames):     
        reg_result=[model.predict(frame_i) for frame_i in frames ]
        position=common_box(reg_result)
#        position=[int(r_i[0][i]) for i in range(4)]
        return [rect_cut(frame_i,position) 
                    for frame_i in frames]
    frames.transform_template(in_path,out_path,helper,False)    

def exp(in_path,out_path,k=100):
    fun=gui_gen
    dataset.make_dataset_template(in_path,out_path,fun,rect_cut,k)

def gui_gen(in_path,out_path,k=20):
    rect_gui=get_bound4D() 
    def helper(img_i):
        size=int(img_i.shape[0]/2)
        position=[0,0,size,size]
        return rect_gui(img_i,position)
    dataset.random_dataset(in_path,out_path,helper,k)

def get_bound4D():
    bar_names=["X","Y","width","height"]
    return gui.TrackbarInput(bar_names, rect_cut)

def rect_cut(img_i,position):
    x,y,width,height=position
    img_i[:,:x]=0
    img_i[:,x+width:]=0
    img_i[:y,:]=0
    img_i[y+height:,:]=0
    return img_i

def common_box(reg_result):
    reg_result=np.squeeze(np.array(reg_result))
    x0,y0=reg_result[:,0],reg_result[:,1]
    x1=x0+reg_result[:,2]
    y1=y0+reg_result[:,3]
    x0,y0=np.amin(x0),np.amin(y0)
    x1,y1=np.amax(x1),np.amax(y1)
    return int(x0),int(y0),int(x1-x0),int(y1-y0)

if __name__=="__main__":
    in_path="final"#"../depth"
    out_path="test2"
    exp(in_path,out_path,k=None)