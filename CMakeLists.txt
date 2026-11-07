cmake_minimum_required(VERSION 3.20)
project(cb2_recompiled C)

set(SDL2_DIR "D:/SDL2" CACHE PATH "Path to SDL2")
include_directories("${SDL2_DIR}/include")
link_directories("${SDL2_DIR}/lib/x64")

file(GLOB_RECURSE RAW_SOURCES 
    "${CMAKE_CURRENT_SOURCE_DIR}/generated/*.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/framework/src/*.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/common/*.c"
)

set(ALL_SOURCES "")
foreach(SRC ${RAW_SOURCES})
    get_filename_component(FNAME "${SRC}" NAME)
    
    # Выкидываем старый раннер и ImGui
    if(FNAME STREQUAL "apu.c" OR 
       FNAME STREQUAL "apu_shadow.c" OR
       FNAME STREQUAL "audio_shadow.c" OR
       FNAME STREQUAL "nes_video.c" OR
       FNAME STREQUAL "controller.c" OR
       FNAME STREQUAL "launcher.c" OR
       FNAME STREQUAL "main_runner.c" OR
       FNAME STREQUAL "cyc_ui_launcher.c" OR
       FNAME STREQUAL "cyc_ui_menu.c" OR
       FNAME STREQUAL "cyc_net.c" OR
       FNAME STREQUAL "debug_server_stub.c" OR
       FNAME STREQUAL "cyc_native_none.c" OR
       FNAME STREQUAL "main_nes.c" OR
       FNAME STREQUAL "rom_parser.c" OR
       FNAME STREQUAL "code_generator.c" OR
       FNAME STREQUAL "cyc_codegen.c" OR
       FNAME STREQUAL "function_finder.c" OR
       FNAME STREQUAL "function_dedup.c" OR
       FNAME STREQUAL "coverage.c" OR
       FNAME STREQUAL "annotations.c" OR
       FNAME STREQUAL "symbol_table.c" OR
       FNAME STREQUAL "hdpack_probe.c")
        # Пропускаем
    else()
        if(NOT SRC MATCHES "/tests/" AND NOT SRC MATCHES "_test\\.c" AND NOT SRC MATCHES "/netplay/" AND NOT SRC MATCHES "/rollback/")
            list(APPEND ALL_SOURCES ${SRC})
        endif()
    endif()
endforeach()

add_executable(cb2_cyc ${ALL_SOURCES})

file(GLOB_RECURSE ALL_HEADERS "${CMAKE_CURRENT_SOURCE_DIR}/*.h")
list(FILTER ALL_HEADERS EXCLUDE REGEX ".*/build/.*")
set(INCLUDE_DIRS "")
foreach(HEADER ${ALL_HEADERS})
    get_filename_component(DIR ${HEADER} DIRECTORY)
    list(APPEND INCLUDE_DIRS ${DIR})
endforeach()
list(REMOVE_DUPLICATES INCLUDE_DIRS)
include_directories(${INCLUDE_DIRS})

if(MSVC)
    target_compile_options(cb2_cyc PRIVATE /bigobj /std:c17)
    target_link_libraries(cb2_cyc PRIVATE SDL2)
else()
    target_link_libraries(cb2_cyc PRIVATE mingw32 SDL2)
endif()

# Включаем SDL-фронтенд
target_compile_definitions(cb2_cyc PRIVATE CYC_WITH_SDL=1)

add_custom_command(TARGET cb2_cyc POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    "${SDL2_DIR}/lib/x64/SDL2.dll"
    $<TARGET_FILE_DIR:cb2_cyc>
)
