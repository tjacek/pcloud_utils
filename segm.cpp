#include "segm.h"

void pcloud_segmentation(PCloud & pcloud,std::string seq_path){
//  std::vector<pcl::PointIndices> clust=growth_segmentation(pcloud);
  std::vector<pcl::PointIndices> clust=min_cut(pcloud);
  std::list<cv::Mat> new_frames;
  for(auto it = clust.begin(); it!=clust.end(); ++it){
    pcl::PointIndices ind_i=(*it);
    PCloud subcloud_i=extract_cloud(ind_i,pcloud);
    cv::Mat frame_i=pcl_to_img(subcloud_i);
    new_frames.push_back(frame_i);
  }
  save_frames(new_frames,seq_path);
//  auto fun= [](pcl::PointIndices in_i) -> cv::Mat{ 
//                  PCloud subcloud_i=extract_cloud(in_i,pcloud);
//                  return pcl_to_img(subcloud_i); };
//  std::transform(clust.begin(),clust.end(),std::back_inserter(new_frames),fun);
}

std::list<PCloud> simple_segm(std::list<PCloud> & pclouds){
  std::list<PCloud> new_pclouds;
  for(auto it = pclouds.begin(); it!=pclouds.end(); ++it){
    PCloud pcloud_i=(*it);
    std::vector <pcl::PointIndices> clust_i=growth_segmentation(pcloud_i);
    pcl::PointIndices first=clust_i.front();
    new_pclouds.push_back( extract_cloud(first ,pcloud_i));
  }
  return new_pclouds;
}

std::vector <pcl::PointIndices> growth_segmentation(PCloud & cloud){
  std::cout << cloud->points.size() <<"\n";
  pcl::search::Search<pcl::PointXYZ>::Ptr tree = boost::shared_ptr<pcl::search::Search<pcl::PointXYZ> > (new pcl::search::KdTree<pcl::PointXYZ>);
  pcl::PointCloud <pcl::Normal>::Ptr normals (new pcl::PointCloud <pcl::Normal>);
  pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> normal_estimator;
  normal_estimator.setSearchMethod (tree);
  normal_estimator.setInputCloud (cloud);
  normal_estimator.setKSearch(20); //(50);
  normal_estimator.compute(*normals);

  pcl::IndicesPtr indices (new std::vector <int>);
  pcl::PassThrough<pcl::PointXYZ> pass;
  pass.setInputCloud(cloud);
  pass.setFilterFieldName("z");
  pass.setFilterLimits(0.0,1.0);
  pass.filter (*indices);

  pcl::RegionGrowing<pcl::PointXYZ, pcl::Normal> reg;
  reg.setMinClusterSize (30);
  reg.setMaxClusterSize (1000000);
  reg.setSearchMethod (tree);
  reg.setNumberOfNeighbours (10);
  reg.setInputCloud (cloud);
  //reg.setIndices (indices);
  reg.setInputNormals (normals);
  reg.setSmoothnessThreshold (30.0 / 180.0 * M_PI);
  reg.setCurvatureThreshold (20.0);

  std::vector <pcl::PointIndices> clusters;
  reg.extract (clusters);
  return clusters;
}

std::vector <pcl::PointIndices> min_cut(PCloud & cloud){
  pcl::IndicesPtr indices (new std::vector <int>);
  pcl::PassThrough<pcl::PointXYZ> pass;
  pass.setInputCloud(cloud);
  //pass.setFilterFieldName("z");
  //pass.setFilterLimits(0.0,1.0);
  pass.filter (*indices);
  

  pcl::MinCutSegmentation<pcl::PointXYZ> seg;
  seg.setInputCloud (cloud);
  seg.setIndices (indices);
  
  Eigen::Vector4f centroid;
  pcl::compute3DCentroid(*cloud, centroid);

  pcl::PointCloud<pcl::PointXYZ>::Ptr foreground_points(new pcl::PointCloud<pcl::PointXYZ> ());
  pcl::PointXYZ point;
  point.x = centroid[0];//120;
  point.y = centroid[1];//160;
  point.z = centroid[2];//0.5;
  foreground_points->points.push_back(point);
  seg.setForegroundPoints (foreground_points);

  seg.setSigma (1.0);
  seg.setRadius (200.0);
  seg.setNumberOfNeighbours( 14); //(14);
  seg.setSourceWeight (0.2);

  std::vector <pcl::PointIndices> clusters;
  seg.extract(clusters);
  cout << clusters[0].indices.size() << endl;
  cout << clusters[1].indices.size() << endl;

  return clusters;
}