#include "files.h"
#include <map>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"

typedef std::map<std::string,std::list<cv::Mat>> Dataset;
Dataset read_seqs(std::string in_path);
void save_seqs(Dataset & dataset,std::string out_path);
std::list<cv::Mat> read_frames(std::string seq_path);
void save_frames(std::list<cv::Mat> & frames,std::string seq_path);