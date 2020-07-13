import cv2,numpy as np
import data

def segm(in_path,out_path,fun=None):
    if(not fun):
        fun=clust_segm
    seq_dict=data.read_seqs(in_path)
    cls_dict={ name_i:[fun(frame_j) 
                for frame_j in seq_i]
                    for name_i,seq_i in seq_dict.items()}
    data.save_clusters(cls_dict,out_path)

def clust_segm(img_i,k=4):
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
    edges = cv2.Canny(img_i,10,200)
    return [edges]

if __name__=="__main__":
    in_path="../normal/result"
    segm(in_path,"../normal/cls",flood_segm)