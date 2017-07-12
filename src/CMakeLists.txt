cmake_minimum_required (VERSION 2.6)
project (ASTRID)
set (ASTRID_VERSION_MAJOR 1)
set (ASTRID_VERSION_MINOR 4)
include(ExternalProject)


ExternalProject_Add(FastME2
  PREFIX distmethods/fastme2/
  URL "http://www.atgc-montpellier.fr/download/sources/fastme/fastme-2.1.4.tar.gz"

  UPDATE_COMMAND ""
  PATCH_COMMAND ""

  BUILD_IN_SOURCE 1
  
  CONFIGURE_COMMAND ./configure --prefix=${CMAKE_BINARY_DIR} LDFLAGS=-static 
)


ExternalProject_Add(PhyDStar
  PREFIX distmethods/PhyDStar/
  URL "http://www.atgc-montpellier.fr/download/binaries/phyd/PhyDstar.tar.gz"

  UPDATE_COMMAND ""
  PATCH_COMMAND ""

  BUILD_IN_SOURCE 1
  
  CONFIGURE_COMMAND ""
  BUILD_COMMAND cp PhyDstar.jar ${CMAKE_BINARY_DIR}/bin
  INSTALL_COMMAND ""
)


add_subdirectory(py)
add_subdirectory(cpp)
