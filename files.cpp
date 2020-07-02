#include "files.h"

std::list<string> get_paths(string in_path){
  std::list<string> paths;
  if (auto dir =opendir(in_path.c_str())) {
    while (auto f = readdir(dir)){
        if (!f->d_name || f->d_name[0] == '.')
            continue;
        std::string path_i(f->d_name);
        paths.push_back(in_path+"/"+path_i);
    }
    closedir(dir);
  }
  return paths;
}

std::string get_name(string seq_path_i){
  int found = seq_path_i.find_last_of("/\\");
  return seq_path_i.substr(found+1);
}

void make_dir(std::string dir_path){
  const int dir_err = mkdir(dir_path.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
  if(-1==dir_err){
    printf("Error creating directory!\n");
//    exit(1);
  }
}

void show(std::list<string> paths){
  for (auto it = paths.begin(); it!=paths.end(); ++it){
    std::cout << (*it) << endl;
  }
}
