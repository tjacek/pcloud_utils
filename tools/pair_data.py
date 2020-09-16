import re,os,shutil

def format_names(in_path,out_path):
    paths=get_paths(in_path)
    action={ path_j:get_id(path_j) 
            for path_i in paths 
                for path_j in get_paths( path_i)}
    for path_i,name_i in action.items():
        out_i="%s/%s" % (out_path,name_i)
        print(out_i)
        shutil.copytree(path_i, out_i)

def get_paths(in_path):
    return [ "%s/%s" % (in_path,path_i)
                for path_i in os.listdir(in_path)]	

def get_id(in_path):
    raw=in_path.split("/")[-1]
    raw=re.sub('[a-z]|[A-Z]','',raw)
    raw=raw.split("_")[1:]
    raw=[atoi(raw_i) for raw_i in raw]
    train= int(raw[1]>5)
    action_id= "%d_%d_%d_%d" % (raw[0],train,raw[1],raw[2])
    return action_id

def atoi(text):
    return int(text) if text.isdigit() else text

in_path="../../Depth/FullFrame"
out_path="../../depth"
format_names(in_path,out_path)