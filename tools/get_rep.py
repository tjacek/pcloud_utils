import re,os,shutil

def format_names(in_path,out_path):
    paths=os.listdir(in_path)
    persons=list(unique_person(paths))
    persons.sort()
    size=len(persons)/2
    def helper(i):
        return 2*(i-size) if(i>size) else (2*i+1)
    persons={ person_i: int(helper(i)) 
                for i,person_i in enumerate(persons)}
    make_dir(out_path)
    for path_i in paths:
        raw=path_i.split("_")
        person_i= persons[raw[-2].lower()]
        cat_i=re.sub('[^0-9]','',raw[-1])
        name_i="%s_%s_1"%(cat_i, person_i)
        in_i="%s/%s"%(in_path,path_i)
        out_i="%s/%s"%(out_path,name_i)
        shutil.copytree(in_i, out_i)

def person_rep(in_path,out_path):
    paths=os.listdir(in_path)
    person_paths={}
    for path_i in paths:
        person_i=get_person(path_i)
        if(not person_i in person_paths):
            full_path_i="%s/%s" % (in_path,path_i)
            person_paths[person_i]=full_path_i
    make_dir(out_path)
    for name_i,path_i in person_paths.items():	
        print(path_i)
        out_i="%s/%s"%(out_path,path_i.split('/')[-1])
        print(out_i)
        shutil.copytree(path_i, out_i)

def unique_person(paths):
    ids=set()
    for path_i in paths:
        ids.update([get_person(path_i).lower()]) 
    return ids	

def get_person(path_i):
    return path_i.split("_")[-2]	

def make_dir(path):
    if(not os.path.isdir(path)):
        os.mkdir(path)

in_path="../detect_person/final"
format_names(in_path,"test")
