# Specifies the minimum required CMake version
cmake_minimum_required(VERSION 3.20)

# Defines the name of your project
project(flightControlSystem C) # Specify C project since the sources are C files

if(WIN32)
# --- SCADE Dependencies and Path Configuration ---

# 1. Attempt to read the Windows environment variable
set(SCADE_DISPLAY_HOME_ENV $ENV{SCADE_DISPLAY_HOME})

# If the environment variable exists, normalize the path (replaces \ with /)
file(TO_CMAKE_PATH "${SCADE_DISPLAY_HOME_ENV}" SCADE_DISPLAY_ROOT)
message(STATUS "Using SCADE root from environment variable: ${SCADE_DISPLAY_ROOT}")

# The rest of the variables now depend on SCADE_DISPLAY_ROOT, which is normalized.
set(OGLX_UTILITIES_DIR "${SCADE_DISPLAY_ROOT}/OGLX/SDYOGLX67/extras/utils")
set(OGLX_FREEGLUT_DIR "${SCADE_DISPLAY_ROOT}/OGLX/SDYOGLX67/extras/freeglut32")
set(OGLX_LIB_DIR "${SCADE_DISPLAY_ROOT}/lib-oglx")
set(APP_SOURCE_DIR "${CMAKE_SOURCE_DIR}")



# Adding include directories
include_directories(../kcgdisplay)
include_directories(../swan_cg)
include_directories(src)
include_directories(${OGLX_LIB_DIR}/include)
include_directories(${OGLX_UTILITIES_DIR}/include)
include_directories(${OGLX_FREEGLUT_DIR})

# --- Source Files Definition ---

# .c files in code and src
file(GLOB APP_SOURCES 
    "${APP_SOURCE_DIR}/src/*.c"
    "${APP_SOURCE_DIR}/../kcgdisplay/*.c"
    "${APP_SOURCE_DIR}/../swan_cg/*.c"
    # External .c files (Windows path escaping is required for compatibility)
    ${OGLX_UTILITIES_DIR}/src/oglxReadErrors.c
)

# --- Configuration for OpenGL and GLUT ---

# We search for OpenGL. On Windows, this usually finds opengl32.lib
find_package(OpenGL REQUIRED) 

# --- Conditional OGLX and GLUT Library Paths ---

# Determine the correct library directory and library name based on the build system
if (MSVC)
    # Visual Studio 17 2022 links with the 'lib' folder and dynamic GLUT
    set(OGLX_FINAL_LIB_DIR "${OGLX_LIB_DIR}/lib")
    set(GLUT_LIB_NAME "freeglut") # Assumes 'freeglut.lib' (dynamic link)
    set(COMPILER_TYPE "MSVC (Visual Studio)")
elseif (CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    # Ninja (GCC/Clang) links with the 'lib64' folder and static GLUT
    set(OGLX_FINAL_LIB_DIR "${OGLX_LIB_DIR}/lib64")
    set(GLUT_LIB_NAME "freeglut_static64") # Link with the static library
    set(COMPILER_TYPE "GNU/Clang (Ninja)")
else()
    # Default fallback
    set(OGLX_FINAL_LIB_DIR "${OGLX_LIB_DIR}/lib")
    set(GLUT_LIB_NAME "freeglut")
    set(COMPILER_TYPE "Unknown")
    message(WARNING "Unknown compiler/generator. Defaulting OGLX library path to: ${OGLX_FINAL_LIB_DIR}")
endif()

message(STATUS "${COMPILER_TYPE} detected: Using OGLX/GLUT path: ${OGLX_FINAL_LIB_DIR}")

# Search for the OGLX library using the determined path
find_library(OGLX_LIBRARY
    NAMES OGLX
    PATHS ${OGLX_FINAL_LIB_DIR}
    NO_DEFAULT_PATH
)

if (NOT OGLX_LIBRARY)
    message(FATAL_ERROR "OGLX library not found in ${OGLX_FINAL_LIB_DIR}. Check the name (e.g.: oglx).")
endif()

# Searching for the GLUT library using the determined path and name
find_library(GLUT_LIBRARY
    NAMES ${GLUT_LIB_NAME}
    PATHS ${OGLX_FREEGLUT_DIR}
    NO_DEFAULT_PATH
)

if (NOT GLUT_LIBRARY)
    message(FATAL_ERROR "GLUT library (${GLUT_LIB_NAME}) not found in ${OGLX_FINAL_LIB_DIR}. Please check the path and name.")
endif()

# --- Executable Creation ---

# Creates the executable from the sources
add_executable(flightControlSystem ${APP_SOURCES})


# Link libraries in the specific required order: OGLX, FREEGLUT, opengl32, gdi32, winmm
# The PRIVATE keyword ensures this order is only applied to this target.
target_link_libraries(flightControlSystem PRIVATE
    # 1. SCADE OGLX Library
    ${OGLX_LIBRARY}
    
    # 2. GLUT Library (Static for Ninja/GCC, Dynamic for MSVC)
    ${GLUT_LIBRARY} 
    
    # 3. Standard Windows/OpenGL libraries (Crucial for MinGW/GCC)
    opengl32
    gdi32
    winmm
)

# --- Compiler Specific Options ---

if (CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
    # Configuration for GCC and Clang (used by Ninja on Linux/MinGW)
    
    # Add -DFREEGLUT_STATIC definition for static linking
    target_compile_definitions(flightControlSystem PRIVATE FREEGLUT_STATIC COEXECUTION)
    
    # Compilation options: C99 standard and all warnings
    target_compile_options(flightControlSystem PRIVATE -std=c99 -Wall)

    # Linker options for MinGW/Windows: creates a console window and uses Win32 API
    target_link_options(flightControlSystem PRIVATE -mconsole -mwin32)
    
elseif (MSVC)
    # Configuration for Visual Studio (MSVC)
    set_target_properties(flightControlSystem PROPERTIES
        # Disables the C4996 warning for unsafe C functions like sprintf
        COMPILE_FLAGS "/W3 /D_CRT_SECURE_NO_WARNINGS /DCOEXECUTION" 
    )
endif()

# --- Conditional DLL Copy for Visual Studio (MSVC) ---

# Copy the DLL ONLY for the Visual Studio generator (MSVC)
if (MSVC)
    # Path to the freeglut DLL
    set(FREEGLUT_DLL_PATH
    "${OGLX_FREEGLUT_DIR}/freeglut.dll"
    )

    # Using add_custom_command to copy the DLL *after* the executable link (POST_BUILD)
    set(EXE_DESTINATION_DIR "$<TARGET_FILE_DIR:flightControlSystem>")

    add_custom_command(
        TARGET flightControlSystem POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ARGS    "${FREEGLUT_DLL_PATH}" "${EXE_DESTINATION_DIR}"
        COMMENT "Copying freeglut.dll next to the executable (MSVC only)"
    )

    message(STATUS "DLL copy enabled for Visual Studio.")

else()
    message(STATUS "DLL copy disabled (not MSVC).")
endif()

elseif(UNIX)
    set(APP_SOURCE_DIR "${CMAKE_SOURCE_DIR}")
    set(OGLX_LIB_DIR $ENV{OGLX_ROOT})

    # Adding include directories
    include_directories(../kcgdisplay)
    include_directories(src)
    include_directories(${OGLX_LIB_DIR}/include)
    include_directories(${OGLX_LIB_DIR}/extras/utils/include)    
    # --- Source Files Definition ---

    # .c files in code and src
    file(GLOB APP_SOURCES 
    "${APP_SOURCE_DIR}/src/*.c"
    "${APP_SOURCE_DIR}/code/*.c"
    
    ${OGLX_LIB_DIR}/extras/utils//src/oglxReadErrors.c
    )

    add_executable(flightControlSystem ${APP_SOURCES})
    target_link_libraries(flightControlSystem PRIVATE "${OGLX_LIB_DIR}/lib/libOGLX.a")
    target_link_libraries(flightControlSystem PRIVATE glut GL m pthread dl)

endif()