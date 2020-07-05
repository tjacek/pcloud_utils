//#ifndef PC_TOOLS
//#define PC_TOOLS
#include <list>
#include <algorithm>
#include <pcl/common/common.h>
#include <opencv2/core/core.hpp>
//#include <opencv2/highgui/highgui.hpp>
//#include "opencv2/imgproc/imgproc.hpp"
#include <pcl/ModelCoefficients.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/extract_indices.h>

typedef pcl::PointCloud<pcl::PointXYZ>::Ptr PCloud;
PCloud img_to_pcl(cv::Mat depth_img);
std::list<PCloud> img_to_pcl(std::list<cv::Mat> depth_img);
cv::Mat pcl_to_img(PCloud & pcloud);
cv::Mat pcl_to_img(PCloud & pcloud,pcl::PointXYZ dim);
std::list<cv::Mat> pcl_to_img(std::list<PCloud> pclouds);

std::list<PCloud> transform(std::list<PCloud> pclouds);

pcl::PointCloud<pcl::PointXYZ>::Ptr simple_ransac(pcl::PointCloud<pcl::PointXYZ>::Ptr pcloud);
PCloud extract_cloud(pcl::PointIndices::Ptr cls,PCloud cloud);