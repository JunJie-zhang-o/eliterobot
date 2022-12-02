# Move

>  移动相关指令
>
>  move_line和move_joint为单条非阻塞运动接口，而move_by_path可以运动多条运动指令，并且以上指令在运行时会在示教器上显示对应的运行jbi。

------
### `stop()`

>  停止机器人运动

#### Args

> 

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```python
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.stop())
#True
```

### `run()`

>  机器人自动运行,暂停后重新运行使用

#### Args

> 

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```python
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.run())
#True
```

### `pause()`

>  机器人暂停

#### Args

> 

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```python
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.pause())
#True
```

### `check_if_jbi_exists(file_name = str)`

> 检查jbi文件是否存在

#### Args

> str: jbi文件名

#### Returns

>  int: 0: 不存在 1: 存在

#### Examples

```python
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.check_if_jbi_exists(file_name = "34"))
#1
```

### `run_jbi(file_name = str)`

> 运行jbi文件

#### Args

> str: 待运行文件名

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.run_jbi(file_name = "34"))
#True
```

### `get_jbi_state(file_name = str)`

> 获取jbi文件运行状态

#### Args

> str: jbi文件名

#### Returns

>  JbiRunState: 0 停止状态,1 暂停状态,2 急停状态,3 运行状态,4 错误状态

#### Examples

```python
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.get_jbi_state(file_name = "34").value)
#0
```

### `jog(index: int, speed: Optional[float] = None)`

> jog运动
>
>    停止发送jog命令后,机器人并不会立马停止运动,需要通过stop命令去停止
>
>    超过1s未接收到下一条jog运动,停止接收,机器人jog运动停止

#### Args

> index (int): 0~11 偶数为负方向运动,奇数位正反向运动
>
> speed (float, optional): 0.05 ~ 100. Defaults to None.

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```python
from elite import EC 
ec = EC(ip="192.168.1.200",auto_connect=True)
print(ec.jog(0,10))
#True
```

### `move_joint(target_joint: list, speed: float, acc: Optional[int] = None, dec: Optional[int] = None, cond_type: Optional[int] = None, cond_num: Optional[int] = None,cond_value: Optional[int] = None)`

> 关节运动,运行后需要根据机器人运动状态去判断是否运动结束

#### Args

> target_joint (list): 目标关节数据,为8个,6个会报错
>
> speed (float): 关节速度百分比
>
> acc (int, optional): 加速度,不写默认为0. Defaults to 0.
>
> dec (int, optional): 减速度,不写默认为0. Defaults to 0.
>
> cond_type (int, optional): IO类型,0为输入,1为输出
>
> cond_num (int, optional): IO地址,0~63
>
> cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令

#### Returns

>  bool: 执行结果,True: 执行成功,False: 执行失败

#### Examples

```

```

### `move_line(target_joint: list, speed: int, speed_type: Optional[int]=None, acc: Optional[int] = None, dec: Optional[int] = None, cond_type: Optional[int]=None, cond_num: Optional[int]=None,cond_value: Optional[int]=None)`

> 直线运动,运行后需根据机器人运动状态去判断是否运动结束

#### Args

> target_joint (list): 目标关节数据
>
> speed (int): 直线速度: 1-3000;旋转角速度: 1-300;
>
> speed_type (int, optional): 0为V直线速度,1为VR旋转角速度,2为AV,3为AVR. Defaults to None.
>
> acc (int, optional): 加速度,不写默认为0. Defaults to None.
>
> dec (int, optional): 减速度,不写默认为0. Defaults to None.
>
> cond_type (int, optional): IO类型,0为输入,1为输出.
>
> cond_num (int, optional): IO地址,0~63.
>
> cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令.

#### Returns

>  bool: 执行结果,True: 执行成功,False: 执行失败

#### Examples

```

```

### `move_line_in_coord(target_user_pose: list, speed: float, speed_type: int, user_coord: list, acc: int=0, dec: int=0, cond_type: Optional[int]=None, cond_num: Optional[int]=None, cond_value: Optional[int]=None, unit_type: Optional[int]=None)`

> 指定坐标系下直线运动

#### Args

> target_user_pose (list): 指定坐标系下的位姿.
>
> speed (float): 直线速度: 1-3000;旋转角速度: 1-300.
>
> speed_type (int): 0为V直线速度,1为VR旋转角速度,2为AV,3为AVR.
>
> user_coord (list): 指定坐标系的数据.
>
> acc (int, optional): 加速度. Defaults to 0.
>
> dec (int, optional): 减速度. Defaults to 0.
>
> cond_type (int, optional): IO类型,0为输入,1为输出.
>
> cond_num (int, optional): IO地址,0~63.
>
> cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令.
>
> unit_type (int, optional): 用户坐标的rx、ry、rz,0:角度,1: 弧度, 不填默认为弧度. Defaults to None.

#### Returns

>  

#### Examples

```

```

### `move_speed_j(vj: list, acc: float, t: float)`

> 关节匀速运动

#### Args

> vj (list): 8个关节的速度值,单位: 度/秒
>
> acc (float): 关节加速度 大于0, 度/s**2
>
> t (float): 关节匀速运动的时间

#### Returns

>  bool: 执行结果,True: 执行成功,False: 执行失败

#### Examples

```

```

### `move_speed_l(v: list, acc: float, t: float, arot: Optional[float]=None)`

> 直线匀速运动

#### Args

> v (list): 沿6个方向运动的速度值,前三个单位为mm/s,后三个为度/s
>
> acc (float): 位移加速度,>0,单位mm/s**2
>
> t (float): 直线匀速运动总时间, >0 
>
> arot (float, optional): 姿态加速度,>0,单位度/s**2. Defaults to None.

#### Returns

>  bool: 执行结果,True: 执行成功,False: 执行失败

#### Examples

```

```

### `move_stop_speed_j(stop_acc:int)`

> 停止关节匀速运动

#### Args

> stop_acc (int): 以此加速度停止运动,>0

#### Returns

>  bool: 执行结果,True: 执行成功,False: 执行失败

#### Examples

```

```

### `move_stop_speed_l(stop_acc:int)`

> 停止直线匀速运动

#### Args

> stop_acc (int): 以此加速度停止运动,范围:>0

#### Returns

>  bool: 执行结果,True: 执行成功,False: 执行失败

#### Examples

```

```

### `add_path_point(way_point: list, move_type:int, speed: float,smooth: int,speed_type:Optional[int]=None,cond_type: Optional[int] = None, cond_num: Optional[int] = None, cond_value: Optional[int] = None)`

>  添加路点信息
>
>  #!若运动类型为关节运动,则speed_type无效,不推荐使用

#### Args

> way_point (list): 目标位置
>
> move_type (int): 0 关节运动,1 直线运动(旋转速度由直线速度决定),2 直线运动(直线速度由旋转速度决定),3 圆弧运动
>
> speed_type (int): 速度类型,0:V(直线速度)对应speed为[1,3000],1:VR(旋转角速度)对应speed为[1-300],2:AV(绝对直线速度)对应[min_AV,max_AV],3:AVR(绝对旋转角速度)对应[min_AVR,max_AVR]
>
> speed (float): 运动速度,无speed_type参数时,对应关节速度[1,100]、直线及圆弧速度[1,3000],旋转速度[1,300]
>
> smooth (int): 平滑度,0~7
>
> cond_type (int, optional): IO类型,0为输入,1为输出.
>
> cond_num (int, optional): IO地址,0~63.
>
> cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令.

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```

```

### `clear_path_point()`

>  清除路点信息2.0

#### Args

> 

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```

```

### `get_running_path_index()`

>  获取机器人当前运行点位序号

#### Args

> 

#### Returns

>  int: 当前运行的点位序号,-1为非路点运动

#### Examples

```

```

### `move_by_path()`

>  路点运动

#### Args

> 

#### Returns

>  int: 失败-1,成功: 路点总个数

#### Examples

```

```

