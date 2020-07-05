#include "frames.h"
#include "pclouds.h"
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


void transform_seqs(std::string in_path,std::string out_path){
  make_dir(out_path);
  std::list<string> seq_paths=get_paths(in_path);
  for(auto it = seq_paths.begin(); it!=seq_paths.end(); ++it){
    std::string seq_path_i=(*it);
    std::list<cv::Mat> frames=read_frames(seq_path_i);
    std::string out_i=out_path +"/"+ get_name(seq_path_i);
//    frames=smooth_frames(frames);
    auto pcloud=img_to_pcl(frames.front());
    cv::Mat frame_i=pcl_to_img(pcloud);
    frames.push_back(frame_i);
    cout << out_i << endl;
    save_frames(frames,out_i);
  }  
}

/*Dataset transform_seqs(Dataset& dataset){
  Dataset new_dataset;
  for( auto const& pair : dataset ){
    std:string name=pair.first;
    std::list<cv::Mat> frames= smooth_frames(pair.second);
    cout << frames.size() << endl;
    new_dataset.insert ( std::pair<std::string,std::list<cv::Mat>>(name,frames) );
  }  
  return new_dataset;
}*/

int main(int argc,char ** argv){
  if(argc <3){
    cout << "too few args\n";
    return 1;
  }
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);

  auto t1 = std::chrono::steady_clock::now();
  transform_seqs(in_path,out_path);
/*  Dataset dataset=read_seqs(in_path);
  Dataset new_dataset= transform_seqs(dataset);
  cout <<"***************"<<endl;
  save_seqs(new_dataset,out_path);*/
  auto t2 = std::chrono::steady_clock::now();
  auto d_milli=std::chrono::duration_cast<std::chrono::milliseconds>(t2-t1).count();
  cout <<"time " << d_milli << endl;
}