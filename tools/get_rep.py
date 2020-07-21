import os,shutil

def person_rep(in_path,out_path):
    paths=os.listdir(in_path)
    person_paths={}
    for path_i in paths:
        person_i=get_person(path_i)
        if(not person_i in person_paths):
            full_path_i="%s/%s" % (in_path,path_i)
            person_paths[person_i]=full_path_i
#    unique_person(paths)
    make_dir(out_path)
    for name_i,path_i in person_paths.items():	
        print(path_i)
        out_i="%s/%s"%(out_path,path_i.split('/')[-1])
        print(out_i)
        shutil.copytree(path_i, out_i)
#def unique_person(paths):
#    ids=set()
#    for path_i in paths:
#        ids.update([get_person(path_i)]) 
#    return ids	

def get_person(path_i):
    return path_i.split("_")[-2]	

def make_dir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)

in_path="../../clf/result"
person_rep(in_path,"test")
