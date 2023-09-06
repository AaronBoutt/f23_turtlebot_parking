Homework 1 Part 2

This is a ros2 package that contains the simulation files you need.  

//Set up environment variables for ros
source /opt/ros/humble/setup.bash

//Fork your own repository of f23_robotics only
//grab the contents
git clone <your github url for this repository>
cd f23_robotics
colcon build
source install/setup.bash

ros2 launch webots_ros2_homework1_python f23_robotics_1_launch.py

//to test movement
//open another terminal
//redo the source commands (you can add to your bash... 
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run teleop_twist_keyboard teleop_twist_keyboard
