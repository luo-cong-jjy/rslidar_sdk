# 1 **rslidar_sdk**

 [中文介绍](README_CN.md)

## 1 Introduction

**rslidar_sdk** is the Software Development Kit of the RoboSense Lidar based on Ubuntu. It contains:

+ The lidar driver core [rs_driver](https://github.com/RoboSense-LiDAR/rs_driver),
+ The ROS support,
+ The ROS2 support,

To get point cloud through ROS/ROS2,  please just use this SDK.

To integrate the Lidar driver into your own projects, please use the rs_driver.

### 1.1 LiDAR Supported

- RS-LiDAR-16
- RS-LiDAR-32
- RS-Bpearl
- RS-Helios
- RS-Helios-16P
- RS-Ruby-128
- RS-Ruby-80
- RS-Ruby-48
- RS-Ruby-Plus-128
- RS-Ruby-Plus-80
- RS-Ruby-Plus-48
- RS-LiDAR-M1
- RS-LiDAR-M2
- RS-LiDAR-M3
- RS-LiDAR-E1
- RS-LiDAR-MX
- RS-LiDAR-AIRY
- RS-LiDAR-AIRYLITE-ETH
- RS-LiDAR-EMX
- RS-LiDAR-FAIRY

### 1.2 Point Type Supported

- XYZI - x, y, z, intensity
- XYZIRT - x, y, z, intensity, ring, timestamp

## 2 Download

### 2.1 Download via Git

Download the rslidar_sdk as below. Since it contains the submodule rs_driver, please also use `git submodule` to download the submodule properly.

```sh
git clone https://github.com/RoboSense-LiDAR/rslidar_sdk.git
cd rslidar_sdk
git submodule init
git submodule update
```

### 2.2 Download directly

Instead of using Git, user can also access [rslidar_sdk_release](https://github.com/RoboSense-LiDAR/rslidar_sdk/releases) to download the latest version of rslidar_sdk.

Please download the **rslidar_sdk.tar.gz** archive instead of Source code. The Source code zip file does not contain the submodule rs_driver, so it has to be downloaded manaully.
![](./img/01_01_download_page.png)

## 3 Dependencies

### 3.1 ROS

To run rslidar_sdk in the ROS environment, please install below libraries.

+ Ubuntu 16.04 - ROS Kinetic desktop
+ Ubuntu 18.04 - ROS Melodic desktop
+ Ubuntu 20.04 - ROS Noetic desktop

For installation, please refer to http://wiki.ros.org.

**It's highly recommanded to install ros-distro-desktop-full**. If you do so, the corresponding libraries, such as PCL, will be installed at the same time.

This brings a lot of convenience, since you don't have to handle version conflict.

### 3.2 ROS2

To use rslidar_sdk in the ROS2 environment, please install below libraries.

+ Ubuntu 16.04 - Not supported
+ Ubuntu 18.04 - ROS2 Eloquent desktop
+ Ubuntu 20.04 - ROS2 Galactic desktop
+ Ubuntu 22.04 - ROS2 Humble desktop

For installation, please refer to https://index.ros.org/doc/ros2/Installation/Eloquent/Linux-Install-Debians/

**Please do not install ROS and ROS2 on the same computer, to avoid possible conflict and manually install some libraries, such as Yaml.**

### 3.3 Yaml (Essential)

version: >= v0.5.2

*If ros-distro-desktop-full is installed, this step can be skipped*

Installation:

```sh
sudo apt-get update
sudo apt-get install -y libyaml-cpp-dev
```

### 3.4 libpcap (Essential)

version: >= v1.7.4

Installation:

```sh
sudo apt-get install -y  libpcap-dev
```

## 4 Compile & Run

### 4.1 Compile with ROS catkin tools

(1) Create a new workspace folder, and create a *src* folder in it. Then put the rslidar_sdk project into the *src* folder.

(2) Go back to the root of workspace, run the following commands to compile and run. (if using zsh, replace the 2nd command with *source devel/setup.zsh*).

```sh
catkin_make
source devel/setup.bash
roslaunch rslidar_sdk start.launch
```

### 4.2 Compile with ROS2 colcon

(1) Create a new workspace folder, and create a *src* folder in it. Then put the rslidar_sdk project in the *src* folder.

(2) Download the packet definition project in ROS2 through [link](https://github.com/RoboSense-LiDAR/rslidar_msg), then put the project rslidar_msg in the *src* folder you just created.

(3) Go back to the root of workspace, run the following commands to compile and run. (if using zsh, replace the 2nd command with *source install/setup.zsh*).

```sh
colcon build
source install/setup.bash
ros2 launch rslidar_sdk start.py
```

Another version of start.py may be used, since it is different on different versios of ROS2. For example, elequent_start.py is used instead for ROS2 elequent.

## 5 Introduction to parameters

To change behaviors of rslidar_sdk, change its parameters. please read the following links for detail information.

[Intro to parameters](doc/intro/02_parameter_intro.md)

[Intro to hidden parameters](doc/intro/03_hiding_parameters_intro.md)

## 6 Quick start

Below are some quick guides to use rslidar_sdk.

[Connect to online LiDAR and send point cloud through ROS](doc/howto/06_how_to_decode_online_lidar.md)

[Decode PCAP file and send point cloud through ROS](doc/howto/08_how_to_decode_pcap_file.md)

[Change Point Type](doc/howto/05_how_to_change_point_type.md)

## 7 Advanced Topics

[Online Lidar - Advanced topics](doc/howto/07_online_lidar_advanced_topics.md)

[PCAP file - Advanced topics](doc/howto/09_pcap_file_advanced_topics.md)

[Coordinate Transformation](doc/howto/10_how_to_use_coordinate_transformation.md)

[Record rosbag &amp; Replay it](doc/howto/11_how_to_record_replay_packet_rosbag.md)

[Solution for ROS2_humble frame rate reduction](doc/howto/13_how_to_solve_ROS2_humble_frame_rate_drop.md)

## 8 M20 背部主机：组播转播与双雷达使用说明

本节记录山猫 M20 Pro 背部外部主机接收前后两颗 RoboSense 雷达的实机部署方法。背部主机运行 Ubuntu 20.04、ROS2 Foxy，工作空间为 `~/robodog_nav_system`。

背部主机不直接接入 M20 内部 `10.21.33.0/24` 雷达网，而是通过 NOS（`10.21.31.106`）上的 `multicast-relay.service` 将原始组播包转发到外部 `10.21.31.0/24` 网段，再由 `rslidar_sdk` 加入组播组、解码并发布两路 `PointCloud2`。

### 8.1 已验证的网络和雷达参数

| 数据流 | 组播地址 | MSOP 端口 | DIFOP 端口 | 输出话题 | 坐标系 |
| --- | --- | ---: | ---: | --- | --- |
| 前雷达 | `224.10.10.201` | `6691` | `7781` | `/rslidar_points_front` | `rslidar_front` |
| 后雷达 | `224.10.10.202` | `6692` | `7782` | `/rslidar_points_rear` | `rslidar_rear` |

实测背部主机有线网口为 `enp2s0`，地址为 `10.21.31.192/24`。如果实际使用其他地址，必须同步修改 `config/m20_backpack_multicast.yaml` 中两颗雷达的 `host_address`。不要把 NOS 内部雷达网地址 `10.21.33.106` 填成背部主机地址。

M20 厂商《激光雷达》文档给出了 `base_link` 坐标系下的静态安装参数：

| 雷达 | x (m) | y (m) | z (m) | roll | pitch | yaw |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 前雷达 | `0.32028` | `0` | `-0.013` | `0` | `0` | `0` |
| 后雷达 | `-0.32028` | `0` | `-0.013` | `0` | `0` | `0` |

厂商文档没有给出非零的 pitch 或 yaw。没有独立标定结果时，不要自行加入 `+/-1.57079` 旋转。当前零旋转配置已经通过 RViz 实机检查：前后点云中的同一墙面可以衔接。

### 8.2 在背部主机工作空间中编译

`rslidar_sdk` 通过 Git 子模块引用 `rs_driver`。普通克隆不会自动下载该子模块，编译时会报错：`src/rs_driver does not contain a CMakeLists.txt file`。应递归克隆，或在已有仓库中初始化子模块：

```sh
git clone --branch foxy-m20-compat --recurse-submodules \
  https://github.com/luo-cong-jjy/rslidar_sdk.git

# 修复已有但缺少子模块的仓库
cd rslidar_sdk
git submodule sync --recursive
git submodule update --init --recursive
```

将 `rslidar_msg` 和 `rslidar_sdk` 放在 `~/robodog_nav_system/src` 下，然后只编译所需软件包：

```sh
cd ~/robodog_nav_system
source /opt/ros/foxy/setup.bash
colcon build --packages-select rslidar_msg rslidar_sdk --symlink-install
source install/setup.bash

ros2 pkg list | grep -E '^rslidar_(msg|sdk)$'
ros2 pkg executables rslidar_sdk
```

实机验证的 SDK 与驱动版本均为 `v1.5.20`，解码类型为 `RSAIRY`。前后两路均能发布有效的 `sensor_msgs/msg/PointCloud2`，字段为 `x`、`y`、`z` 和 `intensity`。

### 8.3 网络和转播服务预检

启动 SDK 前，先检查背部主机网口和路由：

```sh
ip -br addr show enp2s0
ip route | grep -E '10.21.31.0/24|224.0.0.0/4'
ping -c 4 10.21.31.106
```

在 NOS 上，仅看到 `active (running)` 不足以证明转播服务健康。健康状态应为 `Tasks: 5`，并且转播进程占用全部四个组播端口：

```sh
ssh user@10.21.31.106 \
  'systemctl status multicast-relay.service --no-pager -l'

ssh -tt user@10.21.31.106 \
  "sudo ss -ulpn | grep -E '6691|6692|7781|7782'"
```

预期转播端点为：

```text
224.10.10.201:6691
224.10.10.202:6692
224.10.10.201:7781
224.10.10.202:7782
```

如果服务显示 active，但 `Tasks` 不是 `5`，或 Python 转播进程没有占用全部四个端口，应在 NOS 上重启服务并再次检查：

```sh
ssh -tt user@10.21.31.106 \
  'sudo systemctl restart multicast-relay.service'
```

在背部主机上绕过 ROS，直接确认原始 UDP 数据是否到达：

```sh
sudo timeout 15 tcpdump -ni enp2s0 \
  'udp and (port 6691 or port 6692 or port 7781 or port 7782)'
```

MSOP（`6691/6692`）承载高频点云主数据；DIFOP（`7781/7782`）以较低频率承载配置和状态数据。SDK 默认会等待 DIFOP，因此只收到 MSOP 不能视为完整健康状态。

### 8.4 推荐启动命令

显式指定 M20 专用配置启动：

```sh
cd ~/robodog_nav_system
source /opt/ros/foxy/setup.bash
source install/setup.bash

export ROS_DOMAIN_ID=0
export ROS_LOCALHOST_ONLY=0
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

ros2 run rslidar_sdk rslidar_sdk_node --ros-args \
  -p config_path:=/home/m20/robodog_nav_system/src/rslidar_sdk/config/m20_backpack_multicast.yaml
```

启动日志必须显示正确的配置路径、两组 MSOP/DIFOP 端口、两个组播地址，以及 `RoboSense-LiDAR-Driver is running`。

### 8.5 使用 `start.py` 简化启动

当前版本的 `launch/start.py` 已修改为默认使用 M20 专用配置，因此背部主机可以直接执行：

```sh
cd ~/robodog_nav_system
source /opt/ros/foxy/setup.bash
source install/setup.bash

ros2 launch rslidar_sdk start.py
```

启动文件默认配置路径为：

```text
/home/m20/robodog_nav_system/src/rslidar_sdk/config/m20_backpack_multicast.yaml
```

该启动文件会同时启动 SDK 和 RViz。自带 RViz 文件仍是上游单雷达模板，默认话题为 `/rslidar_points`、固定坐标系为 `rslidar`，这不代表 SDK 启动失败。查看 M20 双雷达时，请在 RViz 中添加 `/rslidar_points_front` 和 `/rslidar_points_rear`，并将 Fixed Frame 设置为对应的 `rslidar_front` 或 `rslidar_rear`。建议另存一份 M20 专用 RViz 配置，不要覆盖厂商模板。

无界面运行、systemd 自启动和性能测试仍建议使用 8.4 节的 `ros2 run` 命令，因为它不会启动 RViz。不要同时运行 `ros2 run` 和 `ros2 launch ... start.py`，否则会创建两个 SDK 节点，竞争相同的 UDP 数据和 ROS 话题。

### 8.6 运行验证

在第二个终端中执行：

```sh
source /opt/ros/foxy/setup.bash
source ~/robodog_nav_system/install/setup.bash

ros2 topic list | grep rslidar
ros2 topic type /rslidar_points_front
ros2 topic type /rslidar_points_rear
ros2 topic info -v /rslidar_points_front
ros2 topic info -v /rslidar_points_rear
timeout 20 ros2 topic hz /rslidar_points_front
timeout 20 ros2 topic hz /rslidar_points_rear
```

两条 `topic hz` 命令应依次执行，不要同时运行。每个 Python 订阅者在反序列化大体积点云时都会消耗 CPU；在繁忙的四核背部主机上，同时测量会降低观测频率。雷达标称输出频率为 `10 Hz`，实机在资源充足时可接近 `10 Hz`，但相机、机械臂、代理、IDE 和诊断程序并行运行时会降至约 `6-8 Hz`。

可手动运行 `rviz2`。单独查看某一路点云时，将 Fixed Frame 设置为对应的 `rslidar_front` 或 `rslidar_rear`。SDK 已应用厂商安装参数后，可以为临时可视化发布两坐标系之间的零静态变换，但它不能替代正式运行所需的机器人 TF 树。

### 8.7 故障排查

| 现象 | 可能原因 | 检查或处理方法 |
| --- | --- | --- |
| `ERRCODE_MSOPTIMEOUT` | MSOP 转播线程缺失，或没有加入组播组 | 检查 NOS `Tasks: 5`、四个套接字、`tcpdump`、组播路由，以及 `ip maddr show dev enp2s0` |
| `ERRCODE_WRONGMSOPBLKID` | `lidar_type` 与数据包格式不匹配 | 保持网络参数不变，核对解码类型；本机 M20 已验证使用 `RSAIRY` |
| 话题存在但没有消息 | SDK 已创建发布者，但未解码出完整帧 | 同时检查 MSOP 和 DIFOP 流量，并查看 SDK 日志 |
| RViz 报告 `No transform` | 前后话题使用不同 frame | 一次查看一个坐标系，或提供正确的机器人 TF；不要臆造正式外参 |
| 点云方向错误 | 外参旋转错误，或 SDK 与 TF 重复应用变换 | 恢复厂商外参，避免在 SDK 和 TF 中重复应用同一变换 |
| 输出低于 `10 Hz` | CPU 竞争、诊断订阅者或 UDP 接收缓冲区溢出 | 性能测试时关闭 RViz，依次运行 `topic hz`，检查 `vmstat`、高占用进程和 UDP 计数器 |
| 编译找不到 `rs_driver` | 未下载 Git 子模块 | 执行 `git submodule update --init --recursive` |

资源与丢包检查命令：

```sh
nproc
uptime
free -h
vmstat 1 5
ps -eo pid,ppid,psr,stat,pcpu,pmem,cmd --sort=-pcpu | head -20
ip -s link show enp2s0
cat /proc/net/snmp | grep '^Udp:'
```

`Udp InErrors` 和 `RcvbufErrors` 是累计计数器。应在测试前后分别采样并比较增量，不能仅凭历史非零值认定当前正在丢包。不要在繁忙主机上把多线程 SDK 固定到单个 CPU 核心；实测单核亲和性会降低吞吐量。除非受控测试证明有改善，否则应保留默认的 `0-3` 亲和性。

### 8.8 使用注意事项

- 机器人重启、网络重启或长时间闲置后，应重新检查 NOS 转播服务。即使某个 MSOP 转播线程已经失效，服务仍可能显示 `active`。
- 没有数据包格式证据或标定结果时，不要修改 `RSAIRY`、组播地址、端口以及零 pitch/yaw。
- `use_lidar_clock: true` 会保留雷达时间戳。将点云与机器人里程计、IMU 或 TF 融合前，必须确认背部主机与 M20 内部主机具有足够准确的共同时间基准。
- 外部 SDK 发布的两路话题仍然相互独立。本配置不会自动生成厂商合并后的 `/LIDAR/POINTS`；正式合并时必须使用正确时间戳和统一目标坐标系。
- 将点云用于定位或避障前，必须在真实导航负载下验证持续频率。能够解码并在 RViz 中显示，不等于已经满足实时导航要求。
## M20 建图点云格式

Elevator-LIO 需要点云包含逐点时间戳。M20 转播配置必须使用仓库
`CMakeLists.txt` 中的 `POINT_TYPE=XYZIRT`，重新编译后点云字段应包含：

```text
x, y, z, intensity, ring, timestamp
```

检查命令：

```bash
ros2 topic echo --once /rslidar_points_front | sed -n '/fields:/,/is_bigendian:/p'
```

如果仍只有 `x/y/z/intensity`，说明背部主机使用的是旧 install 产物，需清理
`build/rslidar_sdk` 和 `install/rslidar_sdk` 后重新编译。`timestamp` 是雷达帧内的
绝对时间，Elevator-LIO 会转换为相对帧起始时间的毫秒偏移。

### M20 组播 UDP 丢包处理

M20 双雷达运行时，若 `netstat -su` 中的 `packet receive errors` 与
`receive buffer errors` 增长，表示内核 UDP 接收缓冲溢出，与 CPU 或内存空闲并不矛盾。
`config/m20_backpack_multicast.yaml` 已为两路雷达设置：

```yaml
socket_recv_buf: 4194304
```

背部主机还必须允许该大小，否则 Linux 会按 `net.core.rmem_max` 截断请求。一次性验证可用：

```bash
sudo sysctl -w net.core.rmem_max=8388608
sudo sysctl -w net.core.rmem_default=8388608
```

重启 `rslidar_sdk` 后，驱动日志应显示 `After setting: receive buffer size: 8388608 bytes`。
使用 `netstat -su` 或 `nstat -az UdpRcvbufErrors` 对比测试前后计数；稳定运行期间该计数不应继续增长。

如果两路 UDP 报文数量接近且 `tcpdump` 显示内核未丢包，但某一路点云频率明显偏低，应进行单雷达隔离测试：临时复制 M20 YAML，只保留一路 `lidar` 配置分别启动。若单路后雷达恢复 10 Hz，说明双雷达在同一进程中的解码/发布调度存在瓶颈；若单路后雷达仍偏低，则应检查后雷达 DIFOP 参数、设备状态或 SDK 的 RSAIRY 解码。

仓库已提供可直接使用的单雷达配置：`config/m20_front_only.yaml` 和
`config/m20_rear_only.yaml`。`lidar:` 下必须保留列表项 `- driver:`，不能只删除
`driver` 内容或破坏缩进。启动示例：

```bash
ros2 run rslidar_sdk rslidar_sdk_node --ros-args \
  -p config_path:=/home/m20/robodog_nav_system/src/rslidar_sdk/config/m20_rear_only.yaml
```
