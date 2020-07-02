#include "frames.h"

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