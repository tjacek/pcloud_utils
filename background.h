#include "pclouds.h"
#include <pcl/octree/octree_pointcloud_changedetector.h>
#include <list>
#include <iterator>

std::list<PCloud> remove_background(std::list<PCloud> & pclouds);
std::vector<int> detect_uchanged(PCloud & prev,PCloud& next);