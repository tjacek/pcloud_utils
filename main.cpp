#include <iostream>
#include <list>
#include <map>
#include <dirent.h>
#include <sys/stat.h>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"
using namespace std;

typedef std::map<std::string,std::list<cv::Mat>> Dataset;

Dataset read_seqs(std::string in_path);
void save_seqs(Dataset dataset,std::string out_path);
std::list<cv::Mat> read_frames(std::string seq_path);
void save_frames(std::list<cv::Mat> frames,std::string seq_path);
std::list<string> get_paths(string in_path);
std::string get_name(string in_path);
void make_dir(std::string dir_path);
void show(std::list<string> paths);

Dataset read_seqs(std::string in_path){
  Dataset dataset;
  std::list<string> seq_paths=get_paths(in_path);
  for(auto it = seq_paths.begin(); it!=seq_paths.end(); ++it){
    std::string seq_path_i=(*it);
    std::string name=get_name(seq_path_i);
    std::list<cv::Mat> frames=read_frames(seq_path_i);
    cout << name <<" " << frames.size() << endl;

    dataset.insert ( std::pair<std::string,std::list<cv::Mat>>(name,frames) );
  }
  return dataset;
}

void save_seqs(Dataset dataset,std::string out_path){
  make_dir(out_path);
  for( auto const& pair : dataset ){
    std::string out_i=out_path +"/"+ pair.first;
    std::list<cv::Mat> seq_i=pair.second;  //dataset[out_i];
    cout << out_i << " " << seq_i.size()<< endl;
    save_frames(seq_i,out_i);
  }
}

std::list<cv::Mat> read_frames(std::string seq_path){
  std::list<cv::Mat> frames;
  std::cout << seq_path << endl;
  std::list<string> frame_paths=get_paths(seq_path);
  for (auto it = frame_paths.begin(); it!=frame_paths.end(); ++it){
    std::string frame_path_j=(*it);
    cv::Mat image = cv::imread((*it),CV_LOAD_IMAGE_GRAYSCALE);
    frames.push_back(image);
  }
  return frames;
}

void save_frames(std::list<cv::Mat> frames,std::string out_i){
  make_dir(out_i);
  int j=0;
  for (auto it = frames.begin(); it!=frames.end(); ++it){
    cv::Mat frame_j=(*it);
    std::string path_j=out_i+"/frame"+std::to_string(j)+".png";
    cv::imwrite(path_j, frame_j);
    j++;
  }  
}

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

int main(int argc,char ** argv){
  if(argc <3){
    cout << "too few args\n";
    return 1;
  }
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);  
  Dataset dataset=read_seqs(in_path);
  cout <<"***************"<<endl;
  save_seqs(dataset,out_path);


//  std::list<string> paths=get_paths(in_path);
// show(paths);
//  read_frames(paths.front());

//  std::cout << in_path << " " << out_path << std::endl;
}