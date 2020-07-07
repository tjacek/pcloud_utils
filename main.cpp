#include "frames.h"
#include "pclouds.h"
#include "segm.h"
//#include "background.h"
#include <chrono> 

void transform_seqs(std::string in_path,std::string out_path);
std::list<cv::Mat> smooth_frames(const std::list<cv::Mat>& frames);
void preproc_seq(std::string seg_path_i,std::string out_i);
void frames_segmentation(std::string seq_path_i,std::string out_i);

void transform_seqs(std::string in_path,std::string out_path){
  make_dir(out_path);
  std::list<string> seq_paths=get_paths(in_path);
  for(auto it = seq_paths.begin(); it!=seq_paths.end(); ++it){
    std::string seq_path_i=(*it);
    std::string out_i=out_path +"/"+ get_name(seq_path_i);
//    preproc_seq(seq_path_i,out_i);
    frames_segmentation(seq_path_i,out_i);
  }  
}

std::list<cv::Mat> smooth_frames(const std::list<cv::Mat>& frames){
  auto fun= [](cv::Mat frame) -> cv::Mat{ 
                  cv::medianBlur(frame,frame,15);
                  return frame; };
  std::for_each(frames.begin(),frames.end(),fun);
  return frames;
}

void frames_segmentation(std::string seq_path_i,std::string out_i){
  std::list<cv::Mat> frames=read_frames(seq_path_i);
  make_dir(out_i);
  int j=0;
  for(auto it = frames.begin(); it!=frames.end(); ++it){
    cv::Mat frame_j= (*it);
    std::string frame_path_j=out_i+"/frame_"+std::to_string(j);
    cout << frame_path_j << endl;
    PCloud  pcloud_j=img_to_pcl(frame_j); 
    pcloud_segmentation(pcloud_j,frame_path_j);
    j++;
  }
}

void preproc_seq(std::string seq_path_i,std::string out_i){
  std::list<cv::Mat> frames=read_frames(seq_path_i);
  std::list<cv::Mat>  new_frames=smooth_frames(frames);
  list<PCloud> pclouds=img_to_pcl(new_frames);
  list<PCloud> trans_pclouds=simple_segm(pclouds);
//  list<PCloud> trans_pclouds=remove_background(pclouds);
//  list<PCloud> trans_pclouds=transform(pclouds);
  std::list<cv::Mat> final_frames=pcl_to_img(trans_pclouds);
  cout << out_i << endl;
  save_frames(final_frames,out_i);
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