link_directories(/usr/local/lib )
file(GLOB SOURCES *.cpp)
add_definitions(-std=c++14 -g -O3)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

FIND_PACKAGE( Boost 1.58 COMPONENTS program_options REQUIRED )
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} )

if (APPLE)
  
elseif(UNIX)
  SET(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
  SET(BUILD_SHARED_LIBRARIES OFF)
  SET(CMAKE_EXE_LINKER_FLAGS "-static -static-libgcc")
endif()
add_executable(makemat ${SOURCES} )
target_link_libraries(makemat pthread ${Boost_LIBRARIES} )

