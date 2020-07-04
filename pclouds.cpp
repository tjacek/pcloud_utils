#include "pclouds.h"

std::list<pcl::PointCloud<pcl::PointXYZ>::Ptr> img_to_pcl(std::list<cv::Mat> frames){
  std::list<pcl::PointCloud<pcl::PointXYZ>::Ptr> new_frames;
  for(auto it = frames.begin(); it!=frames.end(); ++it){
    cv::Mat frame_i= (*it);
    new_frames.push_back(img_to_pcl(frame_i));
  }
  return new_frames;
}

pcl::PointCloud<pcl::PointXYZ>::Ptr img_to_pcl(cv::Mat img){
  std::cout << img.rows <<" " << img.cols << "\n";
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
  for(int i=0;i<img.rows;i++){
    for(int j=0;j<img.cols;j++){
      float z= (float) img.at<uchar>(i,j);
//      if(z>10.0){
        pcl::PointXYZ point((float)i, (float) j,z);
        cloud->push_back (point);
//      }
    }
  }
  return cloud;
}