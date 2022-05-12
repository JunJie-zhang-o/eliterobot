[![](https://img.shields.io/pypi/v/loguru.svg#crop=0&crop=0&crop=1&crop=1&from=url&id=RSLM8&margin=%5Bobject%20Object%5D&originHeight=20&originWidth=78&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)](https://pypi.python.org/pypi/loguru) [![](https://img.shields.io/badge/python-3.5%2B%20%7C%20PyPy-blue.svg#crop=0&crop=0&crop=1&crop=1&from=url&id=iUH7Z&margin=%5Bobject%20Object%5D&originHeight=20&originWidth=126&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)](https://pypi.python.org/pypi/loguru)     [![](https://img.shields.io/github/license/delgan/loguru.svg#crop=0&crop=0&crop=1&crop=1&from=url&id=vLzXb&margin=%5Bobject%20Object%5D&originHeight=20&originWidth=78&originalType=binary&ratio=1&rotation=0&showTitle=false&status=done&style=none&title=)](https://github.com/Delgan/loguru/blob/master/LICENSE)

---

# Elite SDK For Python

> ### 明天比今天更简单一点
>
> ### Always Easier Then Before


elirobot是一个Python库,包含了艾利特机器人的EC系列机器人的SDK封装，用户即开即用，非常方便

# Overview

## Installation

```bash
pip install elirobot
```

## Features

- 从复杂的底层通讯建立到开箱即用，只需要一条命令和几行代码
- 面向对象设计，从而可以更轻松的控制多台机器人
- 完善的日志输出，可以更轻松的debug
- 将机器人的固有信息作为类的属性使用
- 更简洁的接口设计，使您可以更快速的编写逻辑代码
- 数据监控端口，也只是两行代码就可以看到所有的监控信息
- 利用Python平台，
- [ ] 

# API Reference

## Port: 8055

### Predefined enum

> 预定义的枚举均在EC类实现，即该枚举为EC类及其实例的属性

#### 机器人模式

```python
class RobotMode(Enum):
    """机器人模式
    """
    TECH   = 0  # 示教模式
    PLAY   = 1  # 运行模式
    REMOTE = 2  # 远程模式
```

#### 机器人状态

```python
class RobotState(Enum):
    """机器人状态
    """
    STOP      = 0   # 停止状态   
    PAUSE     = 1   # 暂停状态
    ESTOP     = 2   # 急停状态
    PLAY      = 3   # 运行状态
    ERROR     = 4   # 错误状态
    COLLISION = 5   # 碰撞状态
```

#### 坐标系

```python
class Coord(Enum):
    JOINT_COORD    = 0  # 关节坐标系
    CART_COORD     = 1  # 笛卡尔坐标系/世界坐标系
    TOOL_COORD     = 2  # 工具坐标系
    USER_COORD     = 3  # 用户坐标系
    CYLINDER_COORD = 4  # 圆柱坐标系
```

#### 工具坐标系

```python
class ToolCoord(Enum):
    TOOL0 = 0   # 工具0
    TOOL1 = 1   # 工具1
    TOOL2 = 2   # 工具2
    TOOL3 = 3   # 工具3
    TOOL4 = 4   # 工具4
    TOOL5 = 5   # 工具5
    TOOL6 = 6   # 工具6
    TOOL7 = 7   # 工具7
```

#### 用户坐标系

```python
class UserCoord(Enum):
    USER0 = 0   # 用户0
    USER1 = 1   # 用户1
    USER2 = 2   # 用户2
    USER3 = 3   # 用户3
    USER4 = 4   # 用户4
    USER5 = 5   # 用户5
    USER6 = 6   # 用户6
    USER7 = 7   # 用户7
```

#### 位姿单位

```python
class AngleType(Enum):
    DEG = 0     # 角度
    RAD = 1     # 弧度
```

#### 循环模式

```python
class CycleMode(Enum):
    STEP             = 0    # 单步
    CYCLE            = 1    # 单循环
    CONTINUOUS_CYCLE = 2    # 连续循环
```

#### 机器人子类型

```python
class ECSubType(Enum):
    """机器人子类型
    """
    EC63  = 3   # EC63
    EC66  = 6   # EC66
    EC612 = 12  # EC612
```

#### 末端按钮

```python
class ToolBtn(Enum):
    """末端按钮
    """
    BLUE_BTN  = 0   # 末端蓝色按钮
    GREEN_BTN = 1   # 末端绿色按钮
```

#### 末端按钮功能

```python
class ToolBtnFunc(Enum):
    """末端按钮功能
    """
    DISABLED     = 0    # 未启用
    DRAG         = 1    # 拖动
    RECORD_POINT = 2    # 拖动记点
        
```

#### jbi运行状态

```python
class JbiRunState(Enum):
    """jbi运行状态
    """
    JBI_IS_STOP  = 0    # jbi运行停止    
    JBI_IS_PAUSE = 1    # jbi运行暂停
    JBI_IS_ESTOP = 2    # jbi运行急停
    JBI_IS_RUN   = 3    # jbi运行中
    JBI_IS_ERROR = 4    # jbi运行错误
```

#### ml点位push结果

```python
class MlPushResult(Enum):
    """ml点位push结果
    """
    CORRECT                   = 0       # 正确
    WRONG_LENGTH              = -1      # 长度错误
    WRONG_FORMAT              = -2      # 格式错误
    TIMESTAMP_IS_NOT_STANDARD = -3      # 时间戳不标准
```

### Attributes

#### 使用前提

以下属性的使用方法的前提条件为已经创建了实例，如下：

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)
```

#### 只读属性

##### `soft_version`

> 当前的软件版本

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.soft_version)
# v3.2.2
```

##### servo_version

>  当前机器人的伺服版本号

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.servo_version)
# 轴1对应伺服版本为11
# 轴2对应伺服版本为11
# 轴3对应伺服版本为11
# 轴4对应伺服版本为11
# 轴5对应伺服版本为11
# 轴6对应伺服版本为11
```

##### current_pose

>  机器人当前的位姿（工具坐标系为当前设置的工具坐标系）

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)
print(ec.current_pose)
# [-116.42876928044629, -445.8173561092616, 330.01911829033054,
# -2.528732975547022, -0.23334446132951653, 2.9722706513750343]
```

##### current_joint

>  当前关节信息

##### collision_state

>  

##### robot_type

>  

##### robot_subType

>  

##### DH

>  

##### remote_sys_password

>  

##### joint_speed

##### tcp_speed

>  

##### joint_acc

>  

##### tcp_acc

>  

##### motor_speed

>  

##### joint_torques

>  

##### current_encode

>  

##### alarm_info

>  

##### TT_state

>  

##### mode

>  获取机器人的模式

returns

> RobotMode: 0示教,1运行,2远程

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.mode)  
#  RobotMode.TECH
```

##### state

>  获取机器人运行状态

returns

> RobotState: 0停止,1暂停,2急停,3运行,4错误,5碰撞

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.state)  
#  RobotState.STOP
```

##### estop_status

>  获取机器人的紧急停止状态(硬件的状态)

returns

> int: 0:非急停,1: 急停

##### servo_status

>  获取伺服状态

returns

> bool: True启用,False未启用

##### sync_status

>  获取同步状态

returns

> bool: True同步,False未同步


#### 读写属性

> 以下属性进行赋值时机器人需要处于remte模式下才可以正常赋值
> 如不在remote模式下，则会提示报错信息

Examples

```python
from elite import EC

ec = EC(ip="172.16.11.251", name="" ,auto_connect=True)
print(ec.run_speed)
# 10

ec.run_speed = 10
# 2022-05-11 22:47:34 |Robot_ip: 172.16.11.251|line:139| ERROR | CMD: setSpeed | Can't operate, robot must be in remote mode.

print(ec.run_speed)
# 10
```

##### run_speed

>  

##### current_coord

>  

##### cycle_mode

>  

##### tool_num_in_teach_mode

>  

##### tool_num_in_run_mode

>  

##### user_num

>  

##### collision_enable_status

>  

##### collision_sensitivity

>  

##### blue_tool_btn_func

>  

##### green_tool_btn_func

>  

##### green_tool_btn_func

>  

### Method

##### `TT_add_joint(joint)`

> 透传添加目标关节点到缓存

**Args**

> joint (List[float]): 目标关节点

**Returns**

>  bool: True操作成功,False操作失败

Examples

##### `TT_add_pose(pose)`

> 透传添加目标位姿点到缓存

**Args**

>  pose (List[float]): 目标位姿点

**Returns**

>   bool: True操作成功,False操作失败

**Examples**

##### `TT_clear_buff()`

> 清空透传缓存

**Args**

> None

**Returns**

>  bool: True操作成功,False操作失败

**Examples**

##### `TT_init(t, lookahead, smoothness, response_enable)`

> 透传模式初始化

**Args**

> t (int, optional): 采样时间(ms),2~100 . Defaults to 10.
> lookahead (int, optional): 前瞻时间(ms),10~1000 . Defaults to 400.
> smoothness (float, optional): 增益,0~1 . Defaults to 0.1.
> response_enable(int, optional): 添加点位指令是否有回复,不写默认有返回值,0:无返回值,1:有返回值.

**Returns**

>  bool: True操作成功,False操作失败

**Examples**

##### `TT_start_joint(joint)`

> deprecated 
> 透传添加目标关节点到缓存

**Args**

> joint (List[float]): 关节数据

**Returns**

>  bool: True操作成功,False操作失败

**Examples**

---

##### calibrate_encoder_zero

**Args**

> 

**Returns**

>  

**Examples**

##### clear_alarm

**Args**

> 

**Returns**

>  

**Examples**

##### collision_state_reset

**Args**

> 

**Returns**

>  

**Examples**

##### connect_ETController

**Args**

> 

**Returns**

>  

**Examples**

##### disconnect_ETController

**Args**

> 

**Returns**

>  

**Examples**

##### drag_teach_switch

**Args**

> 

**Returns**

>  

**Examples**

##### get_base_flange_in_cart

**Args**

> 

**Returns**

>  

**Examples**

##### get_base_flange_in_user

**Args**

> 

**Returns**

>  

**Examples**

##### get_drag_info

**Args**

> 

**Returns**

>  

**Examples**

##### get_md5_password

**Args**

> 

**Returns**

>  

**Examples**

##### get_motor_pos

**Args**

> 

**Returns**

>  

**Examples**

##### get_now_joint

**Args**

> 

**Returns**

>  

**Examples**

##### get_profinet_float_input

**Args**

> 

**Returns**

>  

**Examples**

##### get_profinet_int_input

**Args**

> 

**Returns**

>  

**Examples**

##### get_servo_precise_position_status

**Args**

> 

**Returns**

>  

**Examples**

##### get_tcp_in_now_user

**Args**

> 

**Returns**

>  

**Examples**

##### get_tcp_pose

**Args**

> 

**Returns**

>  

**Examples**

##### get_tool_coord

**Args**

> 

**Returns**

>  

**Examples**

##### jbi_is_exist

**Args**

> 

**Returns**

>  

**Examples**

##### jbi_run

**Args**

> 

**Returns**

>  

**Examples**

##### jbi_run_state

**Args**

> 

**Returns**

>  

**Examples**

##### jog

**Args**

> 

**Returns**

>  

**Examples**
##### 

##### ml_check_push_result

**Args**

> 

**Returns**

>  

**Examples**

##### ml_flush

**Args**

> 

**Returns**

>  

**Examples**

##### ml_init_head

**Args**

> 

**Returns**

>  

**Examples**

##### ml_pause

**Args**

> 

**Returns**

>  

**Examples**

##### ml_push

**Args**

> 

**Returns**

>  

**Examples**

##### ml_push_end

**Args**

> 

**Returns**

>  

**Examples**

##### ml_resume

**Args**

> 

**Returns**

>  

**Examples**

##### ml_start

**Args**

> 

**Returns**

>  

**Examples**

##### ml_stop

**Args**

> 

**Returns**

>  

**Examples**

##### monitor_info_print

**Args**

> 

**Returns**

>  

**Examples**

##### monitor_run

**Args**

> 

**Returns**

>  

**Examples**

##### monitor_thread_run

**Args**

> 

**Returns**

>  

**Examples**

##### monitor_thread_stop

**Args**

> 

**Returns**

>  

**Examples**

##### move_joint

**Args**

> 

**Returns**

>  

**Examples**

##### move_line

**Args**

> 

**Returns**

>  

**Examples**

##### move_line_in_coord

**Args**

> 

**Returns**

>  

**Examples**

##### move_speed_j

**Args**

> 

**Returns**

>  

**Examples**

##### move_speed_l

**Args**

> 

**Returns**

>  

**Examples**

##### move_stop_speed_j

**Args**

> 

**Returns**

>  

**Examples**

##### move_stop_speed_l

**Args**

> 

**Returns**

>  

**Examples**

##### path_add_point

**Args**

> 

**Returns**

>  

**Examples**

##### path_clear_joint

**Args**

> 

**Returns**

>  

**Examples**

##### path_get_index

**Args**

> 

**Returns**

>  

**Examples**

##### path_move

**Args**

> 

**Returns**

>  

**Examples**

##### pause

**Args**

> 

**Returns**

>  

**Examples**

##### payload_get

**Args**

> 

**Returns**

>  

**Examples**

##### payload_set

**Args**

> 

**Returns**

>  

**Examples**

##### `joint_2_pose(joint:, unit_type)`

> 运动学正解

**Args**

>  joint (List[float]): 需要进行正解的关节角
>  unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

**Returns**

> List[float]: 正解后的位姿数据

**Examples**

##### pose_2_joint

> 

**Args**

> 

**Returns**

>  

**Examples**

##### pose_inv

**Args**

> 

**Returns**

>  

**Examples**

##### pose_mul

**Args**

> 

**Returns**

>  

**Examples**

##### cartPose_2_userPose

**Args**

> 

**Returns**

>  

**Examples**

##### userPose_2_cartPose

**Args**

> 

**Returns**

>  

**Examples**

---

##### profinet_float_output_get

**Args**

> 

**Returns**

>  

**Examples**

##### profinet_float_output_set

**Args**

> 

**Returns**

>  

**Examples**

##### profinet_int_output_get

**Args**

> 

**Returns**

>  

**Examples**

##### profinet_int_output_set

**Args**

> 

**Returns**

>  

**Examples**

##### robot_servo_on

**Args**

> 

**Returns**

>  

**Examples**

##### run

**Args**

> 

**Returns**

>  

**Examples**

##### safety_func_get

**Args**

> 

**Returns**

>  

**Examples**

##### safety_func_set

**Args**

> 

**Returns**

>  

**Examples**

##### send_CMD

**Args**

> 

**Returns**

>  

**Examples**

##### servo_status_set

**Args**

> 

**Returns**

>  

**Examples**

##### stop

**Args**

> 

**Returns**

>  

**Examples**

##### sync

**Args**

> 

**Returns**

>  

**Examples**

##### us_sleep

**Args**

> 

**Returns**

>  

**Examples**
##### 

##### user_coord_get

**Args**

> 

**Returns**

>  

**Examples**

##### user_coord_set

**Args**

> 

**Returns**

>  

**Examples**

##### var_P_is_used

**Args**

> 

**Returns**

>  

**Examples**

##### var_get

**Args**

> 

**Returns**

>  

**Examples**

##### var_save

**Args**

> 

**Returns**

>  

**Examples**

##### var_set

**Args**

> 

**Returns**

>  

**Examples**

##### wait_stop

**Args**

> 

**Returns**

>  

**Examples**

## Port: 8056

# ChangeLog

# 问题反馈

