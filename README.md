# docker_gazebo_jazzy:

This Dockerfile will install ROS2 Jazzy with Gazebo on Ubuntu 24.04.
The container is tested and working on ubuntu 22.04.

To install and run:

    git clone https://github.com/DamViv/docker_gazebo_jazzy.git
    cd docker_gazebo_jazzy
    ./launch.sh



## Start and Connect to The Container:

Work you do in the container's `~/ros_jazzy_ws` directory will be saved to your local `ros_jazzy_ws` directory. On your host, create a `ros_jazzy_ws` directory and check docker-compose.yml file line :
    
    ~/ros_jazzy_ws:/root/ros_jazzy_ws:rw


# Launch Terminator inside the opening terminal for simple use: 
terminator

## Divide the terminator terminal 

## Launch the gazebo simulation with a given world:
# For default:
ros2 launch rover_gz_bringup world_gz.launch.py

#Or:
ros2 launch rover_gz_bringup world_gz.launch.py sim_world:=xxxx.sdf


## Spawn a robot inside the simulator
ros2 launch rover_gz_bringup spawn_wheel4Diff.launch.py 

ros2 launch rover_gz_bringup spawn_LeoRover.launch.py 

ros2 launch rover_gz_bringup spawn_ScoutAGX.launch.py



