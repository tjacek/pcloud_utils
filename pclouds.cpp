#include "pclouds.h"

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