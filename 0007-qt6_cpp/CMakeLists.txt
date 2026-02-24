cmake_minimum_required(VERSION 3.22.1)
project(QT6HW)

set(CMAKE_CXX_STANDARD 20)

find_package(Qt6 COMPONENTS Core Widgets)

qt_add_executable(${PROJECT_NAME} src/main.cpp)
set_target_properties(${PROJECT_NAME} PROPERTIES AUTOMOC ON)
target_include_directories(${PROJECT_NAME} PUBLIC include)

target_link_libraries(${PROJECT_NAME} PUBLIC Qt6::Core Qt6::Widgets)
