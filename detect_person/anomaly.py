import numpy as np
import frames

def find_anomaly(in_path,out_path):
    def helper(frames):
        ts=z_score(area(frames))
        outliners=np.array(frames)[( np.abs(ts)>2)]
        return outliners
    frames.transform_template(in_path,out_path,helper,False)

def z_score(frames):
    frames=np.array(frames)
    frames-=np.mean(frames)
    frames/=np.std(frames)	
    return frames

def area(frames):
    frames=np.array(frames)
    frames[frames!=0]=1.0
    return np.array([ np.mean(frame_i) for frame_i in frames])

in_path="../../clean/clf/result"
out_path="test"
find_anomaly(in_path,out_path)