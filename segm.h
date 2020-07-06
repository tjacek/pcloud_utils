#include "pclouds.h"
#include <pcl/segmentation/region_growing.h>
#include <pcl/search/kdtree.h>
#include <pcl/filters/passthrough.h>
#include <pcl/features/normal_3d.h>

std::list<PCloud> simple_segm(std::list<PCloud> & pclouds);
std::vector <pcl::PointIndices> growth_segmentation(PCloud & cloud);