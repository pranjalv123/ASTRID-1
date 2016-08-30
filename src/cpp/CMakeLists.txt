link_directories(/usr/local/lib )
file(GLOB SOURCES *.cpp)
add_definitions(-std=c++14 -g -O3)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

OPTION(STATIC "build static executable"
        0)

FIND_PACKAGE( Boost 1.58 COMPONENTS program_options REQUIRED )
INCLUDE_DIRECTORIES( ${Boost_INCLUDE_DIR} )
LINK_DIRECTORIES( ${Boost_LINK_DIR} )


if (APPLE)
  
elseif(UNIX)
	if (STATIC)
	  SET(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
	  SET(BUILD_SHARED_LIBRARIES OFF)
	  SET(CMAKE_EXE_LINKER_FLAGS "-static")
	endif()
endif()
add_executable(makemat ${SOURCES} )
target_link_libraries(makemat pthread  boost_program_options)

