find_program(PYTHON "python")

MESSAGE (STATUS "binary dir" ${CMAKE_CURRENT_BINARY_DIR})

if (PYTHON)
    file(GLOB pysrc ${CMAKE_CURRENT_SOURCE_DIR}/*.py)
    set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
    set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
    set(DEPS       ${pysrc})
    set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/build_timestamp")
    set(OUTPUT2      "${CMAKE_CURRENT_BINARY_DIR}/build/install_timestamp")

    MESSAGE (STATUS "binary dir" ${OUTPUT})
    
    configure_file(${SETUP_PY_IN} ${SETUP_PY})

    add_custom_command(OUTPUT ${OUTPUT}
                       COMMAND ${PYTHON} ${SETUP_PY} build
                       COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                       DEPENDS ${DEPS} ${SETUP_PY_IN})


    add_custom_command(
      OUTPUT ${OUTPUT2}
      COMMAND ${PYTHON} ${SETUP_PY} install --home=${CMAKE_BINARY_DIR}/bin
      COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT2}      
      DEPENDS ${OUTPUT}
      )

    file(COPY ASTRID
      DESTINATION ${CMAKE_BINARY_DIR}/bin/
      FILE_PERMISSIONS OWNER_EXECUTE OWNER_READ)
    
    add_custom_target(target ALL DEPENDS ${OUTPUT} ${OUTPUT2} ASTRID)

    
endif()