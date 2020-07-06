#include "background.h"

std::list<PCloud> remove_background(std::list<PCloud> & pclouds){
  PCloud prev=pclouds.front();
  std::list<PCloud> new_pclouds;

  for(auto it = std::next(pclouds.begin()); it!=pclouds.end(); ++it){
    PCloud next=(*it);
    std::vector<int> indices=detect_uchanged(prev,next);
    prev=next;
    pcl::PointIndices::Ptr inIndices(new pcl::PointIndices); 
    inIndices->indices = indices;
    new_pclouds.push_back( extract_cloud(inIndices,next) );
  }
  return new_pclouds;
}

std::vector<int> detect_uchanged(PCloud & prev,PCloud & next){
  float resolution = 32.0f;

  pcl::octree::OctreePointCloudChangeDetector<pcl::PointXYZ> octree (resolution);
  octree.setInputCloud(prev);
  octree.addPointsFromInputCloud();
  octree.switchBuffers();

  octree.setInputCloud (next);
  octree.addPointsFromInputCloud ();
  std::vector<int> newPointIdxVector;
  octree.getPointIndicesFromNewVoxels (newPointIdxVector);
  return newPointIdxVector;
}