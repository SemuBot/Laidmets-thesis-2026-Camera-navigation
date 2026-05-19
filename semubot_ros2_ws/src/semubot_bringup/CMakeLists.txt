cmake_minimum_required(VERSION 3.8)
project(semubot_bringup)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/odom_broadcaster.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
