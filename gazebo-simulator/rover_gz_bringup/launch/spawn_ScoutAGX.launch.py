import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchContext, LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def spawn_robot(context: LaunchContext, namespace: LaunchConfiguration):
    pkg_project_description = get_package_share_directory("scout_description")
    robot_ns = context.perform_substitution(namespace)

    robot_desc = xacro.process(
        os.path.join(
            pkg_project_description,
            "urdf",
            "scout_v2.xacro",
        ),
        mappings={"robot_ns": robot_ns},
    )

    if robot_ns == "":
        robot_gazebo_name = "scoutv2_rover"
        node_name_prefix = ""
    else:
        robot_gazebo_name = "scout_rover_" + robot_ns
        node_name_prefix = robot_ns + "_"

    # Launch robot state publisher node
    robot_state_publisher = Node(
        namespace=robot_ns,
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[
            {"use_sim_time": True},
            {"robot_description": robot_desc},
        ],
    )
    # Spawn a robot inside a simulation
    scout_rover = Node(
        namespace=robot_ns,
        package="ros_gz_sim",
        executable="create",
        name="ros_gz_sim_create",
        output="both",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            robot_gazebo_name,
            "-z",
            "1.65",
        ],
    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    topic_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name=node_name_prefix + "parameter_bridge",
        arguments=[
            robot_ns + "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
            robot_ns + "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry",
            robot_ns + "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
            robot_ns + "/imu/data_raw@sensor_msgs/msg/Imu[gz.msgs.IMU",
            robot_ns
            + "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
            robot_ns + "/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model",
        ],
        parameters=[
            {
                "qos_overrides./tf_static.publisher.durability": "transient_local",
            }
        ],
        output="screen",
    )

    # Camera image bridge
    image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        name=node_name_prefix + "image_bridge",
        arguments=[robot_ns + "camera/image_raw"],
        output="screen",
    )


    key_teleop_cmd = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        namespace=robot_ns,
        parameters=[{'speed': '0.4'}],
        prefix=["xterm -e"],
        #remappings=[('cmd_vel', 'cmd_vel')],
    )

    return [
        robot_state_publisher,
        scout_rover,
        topic_bridge,
        image_bridge,
        key_teleop_cmd,
    ]


def generate_launch_description():
    name_argument = DeclareLaunchArgument(
        "robot_ns",
        default_value="",
        description="Robot namespace",
    )

    namespace = LaunchConfiguration("robot_ns")

    return LaunchDescription(
        [name_argument, OpaqueFunction(function=spawn_robot, args=[namespace])]
    )
