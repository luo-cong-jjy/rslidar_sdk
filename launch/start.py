from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    rviz_config=get_package_share_directory('rslidar_sdk')+'/rviz/rviz2.rviz'

    # M20 背部主机固定使用的双雷达配置。
    config_file = '/home/m20/robodog_nav_system/src/rslidar_sdk/config/m20_backpack_multicast.yaml'
    
    return LaunchDescription([
        Node(namespace='rslidar_sdk', package='rslidar_sdk', executable='rslidar_sdk_node', output='screen', parameters=[{'config_path': config_file}]),
        Node(namespace='rviz2', package='rviz2', executable='rviz2', arguments=['-d',rviz_config])
    ])
