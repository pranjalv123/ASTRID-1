cmake_minimum_required (VERSION 2.6)
project (ASTRID)
set (ASTRID_VERSION_MAJOR 1)
set (ASTRID_VERSION_MINOR 3)
include(ExternalProject)


ExternalProject_Add(FastME2
  PREFIX distmethods/fastme2/
  URL "http://www.atgc-montpellier.fr/download/sources/fastme/fastme-2.1.4.tar.gz"

  UPDATE_COMMAND ""
  PATCH_COMMAND ""

  BUILD_IN_SOURCE 1
  
  CONFIGURE_COMMAND ./configure --prefix=${CMAKE_BINARY_DIR}
)

option(UsePhyDStar "Download PhyDStar. PhyDStar is copyright 2007 by
Alexis Criscuolo and Olivier Gascuel.  The software is provided \"as
is\" without warranty of any kind. In no event shall the author be held
responsible for any damage resulting from the use of this software,
including but not limited to the frustration that you may experience
in using the package. The program package, including source codes,
example data sets, executables, and the user's guide, is distributed
free of charge for academic use only." OFF)

if (UsePhyDStar)
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
endif()


add_subdirectory(py)
add_subdirectory(cpp)
