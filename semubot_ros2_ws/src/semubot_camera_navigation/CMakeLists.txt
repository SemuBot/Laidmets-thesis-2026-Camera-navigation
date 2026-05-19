cmake_minimum_required(VERSION 3.8)
project(semubot_camera_navigation)

find_package(ament_cmake REQUIRED)

install(DIRECTORY
  config
  launch
  DESTINATION share/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.yaml" PATTERN "*.py" PATTERN "*.xml"
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
