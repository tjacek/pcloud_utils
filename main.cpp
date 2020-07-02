#include <iostream>
using namespace std;

int main(int argc,char ** argv){
  if(argc <3){
    cout << "too few args\n";
    return 1;
  }
  std::string in_path(argv[1]);
  std::string out_path(argv[2]);
  std::cout << in_path << " " << out_path << std::endl;
}