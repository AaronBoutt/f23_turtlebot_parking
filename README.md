 # Steps to run the project
 ## Source
 - `source install/setup.bash`
  ## Start webots simulation
 - `ros2 launch webots_ros2_homework1_python f23_robotics_1_launch.py `
 - This will start up the simulation in the lab with a parking space
## Run controller
 - `ros2 run webots_ros2_homework1_python webots_ros2_homework1_python`
 - This will move the robot to the parking space and proceed to park it

Commands may be updated to fit with the theme of the project

At first thought
  * The LIDAR sensor may be useful in identifying what is a parking space.
   *  Is there an obstacle X away from my left, right, and front?
     ** If so then park using arcs, else continue searching.

We may also make the parking slot fixed so that the robot will not have to search for the spot
