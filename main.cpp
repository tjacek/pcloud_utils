#include <iostream>
#include <list>
#include <dirent.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"
using namespace std;

std::list<string> get_paths(string in_path);
void show(std::list<string> paths);

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

void show(std::list<string> paths){
  for (auto it = paths.begin(); it!=paths.end(); ++it){
    std::cout << (*it) << endl;
  }
}

void read_frames(std::string seq_path){
  std::list<cv::Mat> frames;
  std::cout << seq_path << endl;
  std::list<string> frame_paths=get_paths(seq_path);
//  show(frame_paths);
  for (auto it = frame_paths.begin(); it!=frame_paths.end(); ++it){
//    std::cout << (*it) << endl;
    std::string frame_path_j=(*it);
    cv::Mat image = cv::imread((*it),CV_LOAD_IMAGE_GRAYSCALE);
    frames.push_back(image);
  }
  cout << frames.size() << endl;
}

int main(int argc,char ** argv){
//  if(argc <3){
//    cout << "too few args\n";
//    return 1;
//  }
  std::string in_path(argv[1]);
  std::list<string> paths=get_paths(in_path);
// show(paths);
  read_frames(paths.front());

//  std::string out_path(argv[2]);
//  std::cout << in_path << " " << out_path << std::endl;
}