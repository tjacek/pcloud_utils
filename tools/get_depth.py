import os,shutil

def depth_only(in_path,out_path):
    make_dir(out_path)
    for path_i in get_files(in_path):
        id_i="_".join(path_i.split("/")[:-1])
        out_i="%s/%s" % (out_path,id_i)
        print(out_i)	
    #    make_dir(out_i)
        shutil.copytree(path_i, out_i)

def get_files(in_path,dir_name="depth"):
    all_paths=[]
    for root, directories, filenames in os.walk(in_path):	
        if(root.split('/')[-1]==dir_name):
            all_paths.append(root)
    return all_paths

def make_dir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)

depth_only("test","depth")