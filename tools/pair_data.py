import re,os

def format_names(in_path):
    paths=get_paths(in_path)
    action={ path_j:get_id(path_j) 
            for path_i in paths 
                for path_j in get_paths( path_i)}
    print(action)

def get_paths(in_path):
    return [ "%s/%s" % (in_path,path_i)
                for path_i in os.listdir(in_path)]	

def get_id(in_path):
    raw=in_path.split("/")[-1]
    raw=re.sub('[a-z]|[A-Z]','',raw)
    raw=raw.split("_")[1:]
    raw=[atoi(raw_i) for raw_i in raw]
    return raw

def atoi(text):
    return int(text) if text.isdigit() else text

in_path="../../Depth/FullFrame"
format_names(in_path)