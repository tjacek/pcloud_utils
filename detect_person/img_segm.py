import cv2,numpy as np
import data

def segm(in_path,out_path):
    seq_dict=data.read_seqs(in_path)
    print( type(seq_dict['A'][0]))
    cls_dict={ name_i:[proc_img(frame_j) 
                for frame_j in seq_i]
                    for name_i,seq_i in seq_dict.items()}
    print(cls_dict.keys())
    data.save_clusters(cls_dict,out_path)

def proc_img(img_i,k=4):
    img_i = cv2.cvtColor(img_i, cv2.COLOR_GRAY2RGB)
    pixel_values = img_i.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)    
    centers = np.uint8(centers)
    labels = labels.flatten()
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(img_i.shape)
#    cls_i=[cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)]
    
    masked_img=np.copy(img_i)
    masked_img=masked_img.reshape((-1,3))
    masked_img[labels==1]=[0,0,0]
    masked_img=masked_img.reshape(img_i.shape)    
    return [masked_img]

in_path="../normal/result"
segm(in_path,"../normal/cls")