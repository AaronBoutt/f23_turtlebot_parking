<a name="readme-top"></a>
## CS-460 Project
Members: Aaron Bouttapanith, Joshua Jacobs

CS-460-001 Group Project

Instructor: Monica Anderson Herzog

## Summary of Work and Relevant Literature
This project is the mid-semester project for Intro to Autonomous Robotics in Fall 2023.
### Approach
#### Goal

  The goal is to program a robot to park between a designated parking space.
  
  At the very least the goal is to be able to run park a robot in simulation.
  
  The best outcome is an implementation into an actual turtlebot.
#### Assumptions

  We assume that in a real scenario the LIDAR and other sensors would work correctly.

  We can also assume that there is some way to identify a parking space. In this project we use reflectivity but other examples could be the lines of the parking space itself.
  
#### Implementation

  The project will be implemented in ros2.
  
  We will be using the turtlebot model BURGER.
  
  The turtlebot will be equiped with a LIDAR and odometry.
  
  Webots will be the choice the implementation
  
  * I have taken the previous homeworks with the Lab world and implemented it into this project
    
  Detection using LIDAR will be the main resource.

  * LIDAR will detect an object and then the robot will begin to park.
    
  * Reflectivity will be used to detect the parking space
#### Results
10 Trials. The main factor we wanted to see was how close we can get to the space and how long it took to get into place.
![image](https://github.com/AaronBoutt/f23_turtlebot/assets/144275992/0340fe64-0b38-468d-8b4a-a9308b35e063)
This would technically not be in a parking space. (Well you could say this is how we park in the US.)

Out of the 10 trials
* 3 Failed to go to the parking space.
* 4 Took over 10 seconds.
  
This gives us around 60-70% success rate.

#### Conclusion

Even something a "simple" as parking can take some work to program.

We found that there were a lot of factors that contributed to the success or failure of our robot.
* Lidar sensor would see the reflectivity wall from too far and instead of aligning with it, would instead head straight to it.
* Orientation and start position also lead to some trials finishing in odd positions.
#### External Resources
  [1]
“turtlebot3_applications/turtlebot3_automatic_parking at master · ROBOTIS-GIT/turtlebot3_applications,” GitHub. https://github.com/ROBOTIS-GIT/turtlebot3_applications/tree/master/turtlebot3_automatic_parking (accessed Dec. 16, 2023).

[2]
Y. Name, “ROBOTIS e-Manual,” ROBOTIS e-Manual. https://emanual.robotis.com/docs/en/platform/turtlebot3/applications/ (accessed Dec. 16, 2023).

‌

‌

  
  
  
