#include <iostream>
#include <string>
#include <list>
#include <dirent.h>
#include <sys/stat.h>
using namespace std;

std::list<string> get_paths(string in_path);
std::string get_name(string in_path);
void make_dir(std::string dir_path);
void show(std::list<string> paths);