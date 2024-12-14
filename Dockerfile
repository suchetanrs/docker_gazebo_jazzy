FROM osrf/ros:jazzy-desktop-full-noble

# ???
RUN DEBIAN_FRONTEND=noninteractive

# Libs and dependencies : git, ROS2, rviz2, gazebo, PCL, terminator, cmake, colcon, eigen ...
RUN apt-get update && apt-get install -y \
    terminator \
    git-all -y \
    lsb-release -y \
    tmux -y \
    build-essential \
    cmake \
    git \
    libgtk2.0-dev \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev  \
    libgoogle-glog-dev \
    libatlas-base-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libabsl-dev \
    libpcl-dev \
    wget \
    x11-apps -y \
    ros-jazzy-rviz2 \
    ros-jazzy-ros-gz \
    ros-jazzy-cv-bridge \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/* 


# OPENCV + CONTRIB    
RUN     git clone https://github.com/opencv/opencv.git
RUN	git clone https://github.com/opencv/opencv_contrib.git 
RUN     cd opencv \
        &&  mkdir release \
        &&  cd release \
        &&  cmake -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local .. \
        &&  make -j8 \
        &&  make install

# CERES
RUN     wget http://ceres-solver.org/ceres-solver-2.2.0.tar.gz        
RUN     tar -xzf ceres-solver-2.2.0.tar.gz
RUN     rm ceres-solver-2.2.0.tar.gz
RUN     cd ceres-solver-2.2.0 \
        &&  mkdir release \
        &&  cd release \
        &&  cmake .. \
        &&  make -j8 \
        &&  make test \
        &&  make install

# Add other programs to end so that it does not build the entire thing
# for launching terminal (for teleop)
RUN apt-get update && apt-get install xterm -y
RUn apt-get install -y nano ros-jazzy-rmw-cyclonedds-cpp

RUN apt-get install ros-jazzy-grid-map -y

# Use root user & define working environment
USER root
RUN mkdir -p /root/ros_jazzy_ws
WORKDIR /root/ros_jazzy_ws

# ROS2 environment setting for root user
RUN /bin/bash -c "echo source /opt/ros/jazzy/setup.bash >> /root/.bashrc"
RUN /bin/bash -c "echo source /root/ros_jazzy_ws/install/setup.bash >> /root/.bashrc"
RUN /bin/bash -c "echo source /opt/ros/jazzy/setup.bash && cd /root/ros_jazzy_ws && colcon build"
RUN /bin/bash -c "echo export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp >> /root/.bashrc"
RUN /bin/bash -c "export CYCLONEDDS_URI=~/.ros/cyclonedds.xml >> /root/.bashrc"

# Enter the docker in a terminal
ENTRYPOINT ["/bin/bash"]






