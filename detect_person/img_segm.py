import cv2,numpy as np
import data

def segm(in_path,out_path,fun=None):
    if(not fun):
        fun=clust_segm
#    data.cluster_template(in_path,out_path,fun)#,single=True)
    data.transform_template(in_path,out_path,fun,single=True)

def clust_segm(img_i,k=4):
#    if(type(img_i)==list):
#        return [clust_segm(img_j,k) for img_j in img_i]
    img_i = cv2.cvtColor(img_i, cv2.COLOR_GRAY2RGB)
    pixel_values = img_i.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    labels = labels.flatten()
    def helper(i):
        masked_img=np.copy(img_i)
        masked_img=masked_img.reshape((-1,3))
        masked_img[labels!=i]=[0,0,0]
        masked_img=masked_img.reshape(img_i.shape)
        return masked_img    
    return [ helper(i) for i in range(k)]

def flood_segm(img_i):
    img_i=cv2.medianBlur(img_i,15)
    edges = cv2.Canny(img_i,20,200)
    return edges

if __name__=="__main__":
    in_path="../smooth"
    out_path="clust"
#    data.make_dir(out_path)
    segm(in_path,out_path)#,flood_segm)