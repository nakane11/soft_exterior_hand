cmake_minimum_required(VERSION 2.8.3)

project(soft_exterior_hand)

find_package(catkin REQUIRED
  message_generation std_msgs)

find_package(roslaunch)

add_message_files(
  FILES
  UInt16Array.msg
  )

generate_messages(
  DEPENDENCIES
  std_msgs
  )

catkin_package()

install(PROGRAMS scripts/rfcomm.sh DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
