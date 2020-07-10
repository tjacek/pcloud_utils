#include "pclouds.h"
#include "frames.h"
#include <pcl/segmentation/region_growing.h>
#include <pcl/search/kdtree.h>
#include <pcl/filters/passthrough.h>
#include <pcl/features/normal_3d.h>
#include <pcl/segmentation/min_cut_segmentation.h>

std::list<PCloud> simple_segm(std::list<PCloud> & pclouds);
void pcloud_segmentation(PCloud & pcloud,std::string seq_path);
std::vector <pcl::PointIndices> growth_segmentation(PCloud & cloud);
std::vector <pcl::PointIndices> min_cut(PCloud & cloud);