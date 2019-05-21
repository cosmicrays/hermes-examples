cmake_minimum_required (VERSION 3.1)
project(hermes C CXX)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
set(CMAKE_BUILD_TYPE Debug)

set(HERMES_EXTRA_INCLUDES)
set(HERMES_EXTRA_LIBRARIES)

set (CMAKE_CXX_STANDARD 14)
cmake_policy(SET CMP0048 NEW)

# Set default build-type to release to enable performance improvements
if (NOT CMAKE_BUILD_TYPE)
        set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)
message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")

if(CMAKE_COMPILER_IS_GNUCXX AND NOT APPLE)
        set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--as-needed")
        set(CMAKE_MODULE_LINKER_FLAGS "${CMAKE_MODULE_LINKER_FLAGS} -Wl,--as-needed")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,--as-needed")
        message(STATUS "Use --as-needed linker flags!")
endif(CMAKE_COMPILER_IS_GNUCXX AND NOT APPLE)

# ----------------------------------------------------------------------------
# Fix Apple RPATH
# ----------------------------------------------------------------------------
set(CMAKE_MACOSX_RPATH 1)
option(USE_ABSOLUTE_RPATH "Add absolute rpath to all libraries and executables" ON)
if(APPLE OR USE_ABSOLUTE_RPATH)
	set(CMAKE_SKIP_BUILD_RPATH  FALSE)
	set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
	set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
	set(ABSOLUTE_RPATH "${CMAKE_INSTALL_PREFIX}/lib${LIB_SUFFIX}")
	if(NOT IS_ABSOLUTE ${ABSOLUTE_RPATH})
		set(ABSOLUTE_RPATH ${CMAKE_BINARY_DIR}/${ABSOLUTE_RPATH})
	endif()

	list(FIND CMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES "${ABSOLUTE_RPATH}" isSystemDir)
	if("${isSystemDir}" STREQUAL "-1")
		message(STATUS "Use absolute RPATH ${ABSOLUTE_RPATH}")
		set(CMAKE_INSTALL_RPATH "${ABSOLUTE_RPATH}")
	endif("${isSystemDir}" STREQUAL "-1")
endif()

# Fix for linker error on mac, Issue: #147
if(APPLE)
	add_definitions(-arch x86_64)
endif(APPLE)

# ----------------------------------------------------------------------------
# Dependencies
# ----------------------------------------------------------------------------

# GSL required dependency
find_package(GSL REQUIRED)
if(GSL_FOUND)
	list(APPEND HERMES_EXTRA_INCLUDES ${GSL_INCLUDE_DIRS})
	list(APPEND HERMES_EXTRA_LIBRARIES ${GSL_LIBRARIES})
endif(GSL_FOUND)

# OpenMP (optional for shared memory multiprocessing)
option(ENABLE_OPENMP "OpenMP for multithreading" ON)
if(ENABLE_OPENMP)
find_package(OpenMP)
        if(OPENMP_FOUND)
                set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
                set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
                set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
        endif(OPENMP_FOUND)
endif(ENABLE_OPENMP)

# FFTW3F (optional for turbulent magnetic fields)
find_package(FFTW3F)
if(FFTW3F_FOUND)
        list(APPEND HERMES_EXTRA_INCLUDES ${FFTW3F_INCLUDE_DIR})
        list(APPEND HERMES_EXTRA_LIBRARIES ${FFTW3F_LIBRARIES})
        add_definitions(-DHERMES_HAVE_FFTW3F)
        list(APPEND HERMES_SWIG_DEFINES -DHERMES_HAVE_FFTW3F)
endif(FFTW3F_FOUND)

option(ENABLE_SYS_CFITSIO "System CFITSIO for FITS output" ON)
if(ENABLE_SYS_CFITSIO)
	#set(CFITSIO_EXE_LINKER_FLAGS "-static")
	find_package(CFITSIO REQUIRED)
	if(CFITSIO_FOUND)
                list(APPEND HERMES_EXTRA_INCLUDES ${CFITSIO_INCLUDE_DIR})
                list(APPEND HERMES_EXTRA_LIBRARIES ${CFITSIO_LIBRARIES})
                set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${CFITSIO_C_FLAGS}")
                set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${CFITSIO_EXE_LINKER_FLAGS}")
		add_definitions(-DHERMES_HAVE_CFITSIO)
	endif(CFITSIO_FOUND)
endif(ENABLE_SYS_CFITSIO)

find_package(HERMES)
if(HERMES_FOUND)
        list(APPEND HERMES_EXTRA_INCLUDES ${HERMES_INCLUDE_DIR})
        list(APPEND HERMES_EXTRA_LIBRARIES ${HERMES_LIBRARIES})
endif(HERMES_FOUND)

# ----------------------------------------------------------------------------
# Playground
# ----------------------------------------------------------------------------
include_directories(include ${HERMES_EXTRA_INCLUDES})

add_executable(freefree src/freefree.cpp)
target_link_libraries(freefree ${HERMES_EXTRA_LIBRARIES})

add_executable(rotationmeasure src/rotationmeasure.cpp)
target_link_libraries(rotationmeasure ${HERMES_EXTRA_LIBRARIES})

add_executable(synchrotron src/synchrotron.cpp)
target_link_libraries(synchrotron ${HERMES_EXTRA_LIBRARIES})

add_executable(synchrotronwithabsorption src/synchrotronwithabsorption.cpp)
target_link_libraries(synchrotronwithabsorption ${HERMES_EXTRA_LIBRARIES})

add_executable(piondecay src/piondecay.cpp)
target_link_libraries(piondecay ${HERMES_EXTRA_LIBRARIES})

add_executable(generic src/generic.cpp)
target_link_libraries(generic ${HERMES_EXTRA_LIBRARIES})

add_executable(exportmodel src/exportmodel.cpp)
target_link_libraries(exportmodel ${HERMES_EXTRA_LIBRARIES})
