import random,data
from itertools import chain

def make_dataset(in_path,out_path,k=100):
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

if __name__=="__main__":
    in_path="../../segm"
    out_path="../../clf"
    data.make_dir(out_path)
    make_dataset(in_path,out_path)