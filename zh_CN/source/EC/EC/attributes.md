# 属性

## 使用前提

以下属性的使用方法的前提条件为已经创建了实例，如下：

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)
```

## 只读属性

### `soft_version`

> 当前的软件版本

#### Returns

> str:机器人当前的软件版本号

#### Examples

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.soft_version)
# v3.2.2
```

### `servo_version`

>  当前机器人的伺服版本号

#### Returns

> str: 机器人当前的伺服版本号

#### Examples

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

### `current_pose`

>  机器人当前的位姿（工具坐标系为当前设置的工具坐标系）

#### Returns

> List[float]: 当前位姿数据

#### Examples

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)
print(ec.current_pose)
# [-116.42876928044629, -445.8173561092616, 330.01911829033054,
# -2.528732975547022, -0.23334446132951653, 2.9722706513750343]
```

### `current_joint`

> 当前关节信息

#### Returns

> List[float]: 当前关节信息

#### Examples

```

```

### `is_collision`

> 当前碰撞状态(示教器右下角的碰撞状态图标)

#### Returns

> 返回值int: 0:未发生碰撞,1:发生碰撞

#### Examples

```

```

### `robot_series`

>  机器人类型

#### Returns

> int: 62为协作类型

#### Examples

```

```

### `robot_type`

>  机器人子类型

#### Returns

> BaseEC.ECSubType:

#### Examples

```

```

### `DH_parameters`

> 机器人的所有连杆值

#### Returns

> List[float]: 机器人的所有连杆值

#### Examples

```

```

### `remote_sys_password`

>  远程模式下自动生成的加密字符串

#### Returns

> str：远程模式下自动生成的加密字符串

#### Examples

```

```

### `joint_speed`

> 各关节速度

#### Returns

> List[float]: 当前各关节速度

#### Examples

```

```

### `tcp_speed`

>  TCP速度

#### Returns

> str：当前TCP速度

#### Examples

```

```

### `joint_acc`

>  各关节加速度

#### Returns

> List[float]: 当前各关节加速度

#### Examples

```

```

### `tcp_acc`

> TCP加速度

#### Returns

> List[float]：当前TCP加速度

#### Examples

```

```

### `motor_speed`

> 机器人马达速度

#### Returns

> List[float]: [speed_1,speed_2,speed_3,speed_4,speed_5,speed_6,speed_7,speed_8]

#### Examples

```

```

### `joint_torques`

> 机器人当前力矩信息

#### Returns

> List[float]: [torque_1,torque_2,torque_3,torque_4,torque_5,torque_6,torque_7,torque_8]

#### Examples

```

```

### encoder_values

> 获取机器人当前编码器值列表

####  Returns

> List[float]: [encode_1,encode_2,encode_3,encode_4,encode_5,encode_6,encode_7,encode_8]

#### Examples

```

```

### `alarm_info`

> 获取机器人本体异常情况

####  Returns

> str: 返回最近5条机器人报警编号的字符串

#### Examples

```

```

### `TT_state`

>  获取当前机器人是否处于透传状态

####  Returns

> int: 0: 非透传状态 1: 透传状态 

#### Examples

```

```

### `mode`

>  获取机器人的模式

#### Returns

> RobotMode: 0示教,1运行,2远程

#### Examples

```

```

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.mode)  
#  RobotMode.TECH
```

### `state`

>  获取机器人运行状态

#### Returns

> RobotState: 0停止,1暂停,2急停,3运行,4错误,5碰撞

#### Examples

```

```

```python
from elite import EC
ec = EC(ip="192.168.1.200", auto_connect=True)

print(ec.state)  
#  RobotState.STOP
```

### `estop_status`

>  获取机器人的紧急停止状态(硬件的状态)

#### Returns

> int: 0:非急停,1: 急停

#### Examples

```

```

### `servo_status`

>  获取伺服状态

#### Returns

> bool: True启用,False未启用

#### Examples

```

```

### `sync_status`

>  获取同步状态

#### Returns

> bool: True同步,False未同步

#### Examples

```

```


## 读写属性

> 以下属性进行赋值时机器人需要处于remte模式下才可以正常赋值
> 如不在remote模式下，则会提示报错信息

### Examples

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

### `run_speed`

>  获取机器人运行的速度

#### Returns

> float: 自动运行下的速度

#### Examples

```

```

### `current_frame`

>  获取机器人当前坐标系

#### Returns

> BaseEC.Frame: 关节0,直角1,工具2,用户3,圆柱4

#### Examples

```

```

### `cycle_mode`

>  

#### Returns

> 

#### Examples

```

```

### `tool_frame_num_in_teach_mode`

>  

#### Returns

> 

#### Examples

```

```

### `tool_frame_num_in_run_mode`

>  

#### Returns

> 

#### Examples

```

```

### `user_frame_num`

>  

#### Returns

> 

#### Examples

```

```

### `collision_enable_status`

>  

#### Returns

> 

#### Examples

```

```

### `collision_sensitivity`

>  

#### Returns

> 

#### Examples

```

```

### `blue_tool_btn_func`

>  

#### Returns

> 

#### Examples

```

```

### `green_tool_btn_func`

>  

#### Returns

> 

#### Examples

```

```

### `green_tool_btn_func`

>  

#### Returns

> 

#### Examples

```

```