***Homework 1: Part 2***

**Links to ROS resources**
Tutorials to complete: 
1. https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools.html
2. https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries.html

Short video overview
https://vimeo.com/639236696

**Background Section**


TO INSTALL PACKAGE FOR ASSIGNMENT 

1. Set up environment variables for ROS

<pre>source /opt/ros/humble/setup.bash</pre>

2. Fork your own repository of f23_robotics (using web interface)

3. Clone your fork

<pre>
git clone <your github url for this repository>
</pre>

4. Make the package (for python, it really just installs the files

<pre>
cd f23_robotics
colcon build
</pre>

5. Set up variables to use the package you just created

<pre>
source install/setup.bash
</pre>

6. Start webots simulation with connect back to ROS in the virtual machine

<pre>
ros2 launch webots_ros2_homework1_python f23_robotics_1_launch.py
</pre>


TEST THE CONNECTION BETWEEN ROS2 AND WEBOTS

Test the connection between webots and ROS, use a ROS based ASCII keyboard to move the simulated robot in Webots

1. Open another terminal

2. Redo the source commands (you can add to your bash to execute it automatically each time) 
<pre>
source /opt/ros/humble/setup.bash
source install/setup.bash
</pre>

3. Run the ROS-based keyboard
<pre>
ros2 run teleop_twist_keyboard teleop_twist_keyboard
</pre>


TO VISUALIZE LASER DATA

1. Open another terminal

2. Redo the source commands (you can add to your bash to execute it automatically each time) 
<pre>
source /opt/ros/humble/setup.bash
source install/setup.bash
</pre>

3. Run the ROS-based keyboard
<pre>
ros2 run teleop_twist_keyboard teleop_twist_keyboard
</pre>

<pre>
  rviz2
</pre>

