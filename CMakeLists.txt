if(NOT ENABLE_GUI)
  return()
endif()

option(BUILD_ODENS "Building the ODENS files" ON)
if(NOT BUILD_ODENS)
  return()
endif()

if(UNIX)
  add_custom_target(
    symlink_to_ODENS ALL
    COMMAND ${CMAKE_COMMAND} -E create_symlink
    ${CMAKE_CURRENT_SOURCE_DIR} ${CNOID_BINARY_SHARE_DIR}/ODENS)
endif()

install(DIRECTORY
  model
  project
  script
  DESTINATION ${CNOID_SHARE_SUBDIR}/ODENS)

