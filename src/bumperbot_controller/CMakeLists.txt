cmake_minimum_required(VERSION 3.8)
project(bumperbot_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

#using these packages to create a python package as Cmake is not able to create a python package on its own
# also add these dependencies to the package.xml file
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(
  DIRECTORY config launch bumperbot_controller
  DESTINATION share/${PROJECT_NAME}
)

# Install the Python controller script
install(PROGRAMS
  ${PROJECT_NAME}/simple_controller.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME simple_controller
)

install(PROGRAMS
  ${PROJECT_NAME}/noisy_controller.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME noisy_controller
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
