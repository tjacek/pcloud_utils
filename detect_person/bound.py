import numpy as np
import data

def aprox_bound(in_path,out_path):
	data.transform_template(in_path,out_path,fun)

def fun(img_i):
    img_i[img_i!=0]=1
    ts_i=np.mean(img_i,axis=0)
    return bar_plot(ts_i)

def bar_plot(ts_i):
    plot_i=np.zeros((100,ts_i.shape[0]))
    for j,value_j in enumerate(ts_i):
        k=int( (1.0-value_j) *100)
        plot_i[k:,j]=100
    return plot_i


aprox_bound("raw","test")