cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(pcloud_utils)

set(Boost_DEBUG ON)
set(PCL_DIR "/usr/lib/x86_64-linux-gnu/cmake/pcl")

find_package(PCL 1.8 REQUIRED COMPONENTS common)
find_package(OpenCV REQUIRED)

include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

add_executable(pcloud_utils main.cpp files.cpp frames.cpp pclouds.cpp)
target_link_libraries(pcloud_utils ${OpenCV_LIBS})
target_link_libraries(pcloud_utils ${PCL_LIBRARIES})
