import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

# Path to the configuration files
pkg_share = get_package_share_directory('localization')
ekf_config_file = PathJoinSubstitution([pkg_share, 'config', 'snot_ekf_config.yaml'])

def generate_launch_description():
    return LaunchDescription([
        # Set console output formatting and colorization
        SetEnvironmentVariable(name='RCUTILS_CONSOLE_OUTPUT_FORMAT', value=["[{time}]: [{severity}] [{name}]: {message}"]),
        SetEnvironmentVariable(name='RCUTILS_COLORIZED_OUTPUT', value=['1']),

        # Declare launch arguments
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation clock if true'),

        # EKF Node without remapping
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            respawn=True,
            parameters=[ekf_config_file, {'use_sim_time': LaunchConfiguration('use_sim_time')}]
        )
    ])
