## A web application for Navigation and Mapping ROS
## This is a modified version of rizwin work

This is a web application that is build on Flask,serves the purpose of Mapping and Navigation of a robot that is build on ROS from a web browser.


## Prerequisite

- Robotic Operating System(Kinetic) installed on Ubuntu 16.04
- Runs on python 2.7(Run flask on python 2.7 environment)


## Installation
Clone this repo in your catkin_ws and catkin_make it
Here turtlebot3 simulation is used to display the demo.
All turtlebot3 packages are installed in the src folder
open bashrc,

`sudo gedit ~/.bashrc`

place the following at the end,

`source` **path to your ros workspace's setup.bash**  (source /home/user/catkin_ws/devel/setup.bash)
change the user to your username, mine is y

`export TURTLEBOT3_MODEL=waffle`

Install Flask,

`pip install flask`

Install ROS dependecies,

- `sudo apt-get install ros-kinetic-navigation`
- `sudo apt-get install ros-kinetic-slam-gmapping`
- `sudo apt-get install ros-kinetic-rosbridge-suite`
- `sudo apt-get install ros-kinetic-tf2-web-republisher`
- `sudo apt-get install ros-kinetic-robot-pose-publisher`

## Features
- Real time mapping of environment and save the map at same time on browser.
- Zoom,pan,Switch between graphical and live images.
- Real time monitoring of autonomous navigation of robot and its path.
- Load multiple maps and delete from browser.


## Technologies and Languages
  - ROS
  - Python
  - HTML
  - CSS
  - JavaScript
  - sqlite
  - Flask
  - Tkinter
## Advanced
- You could edit the png file of map located in the static folder to make the map attractive.
- If you are using your own robot write the common nodes in navigation and mapping in one launch file and replace the 

           `subprocess.Popen(["roslaunch", "turtlebot3_navigation", "turtlebot3_bringup.launch"])` 

in **app.py** with the corresponding package and launch file name.Replace your mapping file and navigation file in following,

-          `subprocess.Popen(["roslaunch","--wait", "turtlebot3_navigation",            
            "turtlebot3_navigation.launch","map_file:="+os.getcwd()+"/static/"+mapname+".yaml"])`

-          `subprocess.Popen(["roslaunch", "--wait", "turtlebot3_slam", "turtlebot3_slam.launch"])`

`For any help contact me on yousfineji1@gmail.com`



