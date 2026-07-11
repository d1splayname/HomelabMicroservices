cmake_minimum_required(VERSION 3.15)

project(cppmethods LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(cppmethods
    cpp/bindings.cpp

    cpp/test.cpp
    cpp/sha256sum.cpp
    cpp/bcrypt.cpp
)

target_include_directories(cppmethods PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

install(TARGETS cppmethods
    LIBRARY DESTINATION .
)