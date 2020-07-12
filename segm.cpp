#include "segm.h"

void pcloud_segmentation(PCloud & pcloud,std::string seq_path){
//  std::vector<pcl::PointIndices> clust=min_cut(pcloud);
  std::vector<pcl::PointIndices> clust=diff_of_normal(pcloud);

  std::list<cv::Mat> new_frames;
  auto fun=[&pcloud](pcl::PointIndices in_i) -> cv::Mat{ 
                  PCloud subcloud_i=extract_cloud(in_i,pcloud);
                  return pcl_to_img(subcloud_i); };
  std::transform(clust.begin(),clust.end(),std::back_inserter(new_frames),fun);
  save_frames(new_frames,seq_path);
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

  PCloud foreground_points(new pcl::PointCloud<pcl::PointXYZ> ());  pcl::PointXYZ point;
  point.x = centroid[0];//120;
  point.y = centroid[1];//160;
  point.z = centroid[2];//0.5;
  foreground_points->points.push_back(point);
  seg.setForegroundPoints (foreground_points);

  seg.setSigma (4.0);
  seg.setRadius (400.0);
  seg.setNumberOfNeighbours(50); 
  seg.setSourceWeight (0.2);

  std::vector <pcl::PointIndices> clusters;
  seg.extract(clusters);
  cout << clusters[0].indices.size() << endl;
  cout << clusters[1].indices.size() << endl;

  return clusters;
}

/*std::vector <pcl::PointIndices> diff_of_normal(PCloud & cloud){
  double scale1,scale2,segradius;
//  std::vector <pcl::PointIndices> cluster_indices;
  pcl::search::Search<pcl::PointXYZ>::Ptr tree;
  if (cloud->isOrganized ())
  {
    tree.reset (new pcl::search::OrganizedNeighbor<pcl::PointXYZ>());
  }
  else
  {
    tree.reset (new pcl::search::KdTree<pcl::PointXYZ>(false));
  }
    tree->setInputCloud (cloud);

  pcl::NormalEstimationOMP<pcl::PointXYZ,pcl::PointNormal> ne;
  ne.setInputCloud (cloud);
  ne.setSearchMethod (tree);
  ne.setViewPoint(std::numeric_limits<float>::max(), std::numeric_limits<float>::max(),std::numeric_limits<float>::max());
  pcl::PointCloud<pcl::PointNormal>::Ptr normals_small_scale (new pcl::PointCloud<pcl::PointNormal>);
  ne.setRadiusSearch (scale1);
  ne.compute (*normals_small_scale);
  std::cout << "Calculating normals for scale..." << scale2 << std::endl;
  pcl::PointCloud<pcl::PointNormal>::Ptr normals_large_scale (new pcl::PointCloud<pcl::PointNormal>);
  pcl::PointCloud<pcl::PointNormal>::Ptr doncloud (new pcl::PointCloud<pcl::PointNormal>);
  copyPointCloud (*cloud, *doncloud);
  std::cout << "Calculating DoN... " << std::endl;
  // Create DoN operator
  pcl::DifferenceOfNormalsEstimation<pcl::PointXYZ,pcl::PointNormal,pcl::PointNormal> don;
  don.setInputCloud (cloud);
  don.setNormalScaleLarge (normals_large_scale);
  don.setNormalScaleSmall (normals_small_scale);

  if (!don.initCompute ())
  {
    std::cerr << "Error: Could not initialize DoN feature operator" << std::endl;
    exit (EXIT_FAILURE);
  }

  // Compute DoN
  don.computeFeature (*doncloud);

  pcl::search::KdTree<pcl::PointNormal>::Ptr segtree (new pcl::search::KdTree<pcl::PointNormal>);
  segtree->setInputCloud(doncloud);

  std::vector<pcl::PointIndices> cluster_indices;
  pcl::EuclideanClusterExtraction<pcl::PointNormal> ec;

  ec.setClusterTolerance (segradius);
  ec.setMinClusterSize (50);
  ec.setMaxClusterSize (100000);
  ec.setSearchMethod (segtree);
  ec.setInputCloud (doncloud);
  ec.extract (cluster_indices);

  return cluster_indices;
}*/


std::vector <pcl::PointIndices> diff_of_normal(PCloud & cloud){
  double scale1=5;
  double scale2=25;
  double threshold=5;
  double segradius=5;

  // Create a search tree, use KDTreee for non-organized data.
  pcl::search::Search<pcl::PointXYZ>::Ptr tree;
  if (cloud->isOrganized ())
  {
    tree.reset (new pcl::search::OrganizedNeighbor<pcl::PointXYZ> ());
  }
  else
  {
    tree.reset (new pcl::search::KdTree<pcl::PointXYZ>(false));
  }

  // Set the input pointcloud for the search tree
  tree->setInputCloud (cloud);

  if (scale1 >= scale2)
  {
    std::cerr << "Error: Large scale must be > small scale!" << std::endl;
    exit (EXIT_FAILURE);
  }

  pcl::NormalEstimationOMP<pcl::PointXYZ, pcl::PointNormal> ne;
  ne.setInputCloud (cloud);
  ne.setSearchMethod (tree);

  ne.setViewPoint (std::numeric_limits<float>::max (), std::numeric_limits<float>::max (), std::numeric_limits<float>::max ());

  std::cout << "Calculating normals for scale..." << scale1 << std::endl;
  pcl::PointCloud<pcl::PointNormal>::Ptr normals_small_scale (new pcl::PointCloud<pcl::PointNormal>);

  ne.setRadiusSearch (scale1);
  ne.compute (*normals_small_scale);

  // calculate normals with the large scale
  std::cout << "Calculating normals for scale..." << scale2 << std::endl;
  pcl::PointCloud<pcl::PointNormal>::Ptr normals_large_scale (new pcl::PointCloud<pcl::PointNormal>);

  ne.setRadiusSearch (scale2);
  ne.compute (*normals_large_scale);

  // Create output cloud for DoN results
  pcl::PointCloud<pcl::PointNormal>::Ptr doncloud (new pcl::PointCloud<pcl::PointNormal>);
  copyPointCloud (*cloud, *doncloud);

  std::cout << "Calculating DoN... " << std::endl;
  // Create DoN operator
  pcl::DifferenceOfNormalsEstimation<pcl::PointXYZ,pcl::PointNormal,pcl::PointNormal> don;
  don.setInputCloud (cloud);
  don.setNormalScaleLarge (normals_large_scale);
  don.setNormalScaleSmall (normals_small_scale);

  if (!don.initCompute ())
  {
    std::cerr << "Error: Could not initialize DoN feature operator" << std::endl;
    exit (EXIT_FAILURE);
  }

  // Compute DoN
  don.computeFeature (*doncloud);


/*  // Build the condition for filtering
  pcl::ConditionOr<PointNormal>::Ptr range_cond (
    new pcl::ConditionOr<PointNormal> ()
    );
  range_cond->addComparison (pcl::FieldComparison<PointNormal>::ConstPtr (
                               new pcl::FieldComparison<PointNormal> ("curvature", pcl::ComparisonOps::GT, threshold))
                             );
  // Build the filter
  pcl::ConditionalRemoval<PointNormal> condrem;
  condrem.setCondition (range_cond);
  condrem.setInputCloud (doncloud);

  pcl::PointCloud<PointNormal>::Ptr doncloud_filtered (new pcl::PointCloud<PointNormal>);

  // Apply filter
  condrem.filter (*doncloud_filtered);

  doncloud = doncloud_filtered;

  // Filter by magnitude
  std::cout << "Clustering using EuclideanClusterExtraction with tolerance <= " << segradius << "..." << std::endl;
*/
  pcl::search::KdTree<pcl::PointNormal>::Ptr segtree (new pcl::search::KdTree<pcl::PointNormal>);
  segtree->setInputCloud (doncloud);

  std::vector<pcl::PointIndices> cluster_indices;
  pcl::EuclideanClusterExtraction<pcl::PointNormal> ec;

  ec.setClusterTolerance (segradius);
  ec.setMinClusterSize (50);
  ec.setMaxClusterSize (100000);
  ec.setSearchMethod (segtree);
  ec.setInputCloud (doncloud);
  ec.extract (cluster_indices);

  return cluster_indices;

}