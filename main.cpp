#include <iostream>
#include <list>
#include <dirent.h>
using namespace std;

std::list<string> get_paths(string in_path);
void show(std::list<string> paths);

std::list<string> get_paths(string in_path){
  std::list<string> paths;
  if (auto dir =opendir(in_path.c_str())) {
    while (auto f = readdir(dir)){
        if (!f->d_name || f->d_name[0] == '.')
            continue; // Skip everything that starts with a dot
        std::string path_i(f->d_name);
        paths.push_back(path_i);
    }
    closedir(dir);
  }
  return paths;
}

void show(std::list<string> paths){
  for (auto it = paths.begin(); it!=paths.end(); ++it){
    std::cout << (*it) << endl;
  }
}

int main(int argc,char ** argv){
//  if(argc <3){
//    cout << "too few args\n";
//    return 1;
//  }
  std::string in_path(argv[1]);
  std::list<string> paths=get_paths(in_path);
  show(paths);
//  std::string out_path(argv[2]);
//  std::cout << in_path << " " << out_path << std::endl;
}