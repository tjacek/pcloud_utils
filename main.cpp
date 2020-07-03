#include "frames.h"
#include <chrono> 

std::list<cv::Mat> smooth_frames(const std::list<cv::Mat>& frames){
  std::list<cv::Mat> new_frames;
  for(auto it = frames.begin(); it!=frames.end(); ++it){
    cv::Mat frame_i= (*it);
    cv::Mat new_frame_i;
    cv::medianBlur(frame_i,new_frame_i,15);
    new_frames.push_back(new_frame_i);
  }
  return new_frames;//new_frames;
}

Dataset transform_seqs(Dataset& dataset){
  Dataset new_dataset;
  for( auto const& pair : dataset ){
    std:string name=pair.first;
    std::list<cv::Mat> frames= smooth_frames(pair.second);
    cout << frames.size() << endl;
    new_dataset.insert ( std::pair<std::string,std::list<cv::Mat>>(name,frames) );
  }  
  return new_dataset;
}

int main(int argc,char ** argv){
  if(argc <3){
    cout << "too few args\n";
    return 1;
  }
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);

  auto t1 = std::chrono::steady_clock::now();
  Dataset dataset=read_seqs(in_path);
  Dataset new_dataset= transform_seqs(dataset);
  cout <<"***************"<<endl;
  save_seqs(new_dataset,out_path);
  auto t2 = std::chrono::steady_clock::now();
  auto d_milli=std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count();
  cout <<"time " << d_milli << endl;
}