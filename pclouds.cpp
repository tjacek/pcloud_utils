#include "pclouds.h"

std::list<PCloud> img_to_pcl(std::list<cv::Mat> frames){
  std::list<PCloud> new_frames;
  for(auto it = frames.begin(); it!=frames.end(); ++it){
    cv::Mat frame_i= (*it);
    new_frames.push_back(img_to_pcl(frame_i));
  }
//  std::transform(frames.begin(),frames.end(),new_frames,img_to_pcl);
  return new_frames;
}

PCloud img_to_pcl(cv::Mat img){
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
  std::cout << cloud->points.size() << std::endl;
  return cloud;
}

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr &pcloud){
  pcl::PointXYZ dim(240,320,255);
  return pcl_to_img(pcloud,dim);
}

cv::Mat pcl_to_img(pcl::PointCloud<pcl::PointXYZ>::Ptr & pcloud,pcl::PointXYZ dim){
  cv::Mat img=cv::Mat::zeros(dim.x,dim.y,CV_8UC1);
  for (size_t i = 0; i < pcloud->points.size(); ++i)
  {
    int x=(int) pcloud->points[i].x ;
    int y=(int) pcloud->points[i].y;
    float z=(float) pcloud->points[i].z;
    if(x<dim.x && y<dim.y){
      img.at<uchar>(x,y)=(uchar) z;
    }
  }
  return img;
}

std::list<cv::Mat> pcl_to_img(std::list<PCloud> pclouds){
  std::list<cv::Mat> frames;
  auto fun= [](PCloud pcloud) -> cv::Mat{ 
                  return pcl_to_img(pcloud); };
  std::transform(pclouds.begin(),pclouds.end(),std::back_inserter(frames),fun);
  return frames;
}

/*std::list<PCloud> transform(std::list<PCloud> pclouds){
  std::list<PCloud> new_pclouds;
  auto fun= [](PCloud pcloud) -> PCloud{ 
                  return pcloud; };
  std::transform(pclouds.begin(),pclouds.end(),new_pclouds,fun);
  return new_frames;
}*/