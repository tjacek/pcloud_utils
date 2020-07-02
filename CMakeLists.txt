cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(pcloud_utils)

find_package(OpenCV REQUIRED)
add_executable(pcloud_utils main.cpp files.cpp frames.cpp)
target_link_libraries(pcloud_utils ${OpenCV_LIBS})