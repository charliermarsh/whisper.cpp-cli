cmake_minimum_required(VERSION 3.28...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

set(WHISPER_BUILD_EXAMPLES
    ON
    CACHE BOOL "" FORCE)

include(FetchContent)
FetchContent_Declare(
  whisper-cpp
  URL https://github.com/ggerganov/whisper.cpp/archive/refs/tags/v1.5.5.zip
  URL_HASH MD5=7262e27c619a0e51e5e2892e429d7481
  EXCLUDE_FROM_ALL)
FetchContent_MakeAvailable(whisper-cpp)

set_target_properties(main PROPERTIES OUTPUT_NAME whisper-cpp EXCLUDE_FROM_ALL
                                                              FALSE)

install(TARGETS main RUNTIME DESTINATION "${SKBUILD_SCRIPTS_DIR}")
