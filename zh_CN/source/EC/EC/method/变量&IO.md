# 变量与IO

> 变量与IO相关接口用于查询和设置系统全局变量B、I、D、P、V以及数字量IO、模拟量IO和虚拟io(即M变量，连续多个M变量即为寄存器)
>
> 其中P变量用于存储机器人的关节数据，即对应机器人6个关节的数据，使用Python中的list数据类型即可
>
> 其中V变量用于存储机器人笛卡尔空间位姿，使用Python中的list数据类型即可
>
> 以上所有变量中，P变量和V变量再使用前需要打开该变量，否则对应的地址是无法使用的

------

###  `set_var(address: str, value:Union[int, list])`

>  设置系统变量值,remote模式下使用

#### Args

> address (str): 变量地址,B0~B255, I0~I255, D0~D255, P0~P255, V0~V255
>
> value (Union[int, list]): 要设置的地址

#### Returns

>  bool: 成功 True,失败 False

#### Examples

```python

```

### `get_var(address: str, auto_print: bool=False)`

>  获取系统变量值,remote模式下使用

#### Args

> address (str): 变量地址,B0~B255, I0~I255, D0~D255, P0~P255, V0~V255
>
> auto_print (bool, optional): 自动打印变量值. Defaults to False.

#### Returns

>  Optional[Union[float,int,list]]: 返回获取的变量值

#### Examples

```python

```

### `var_p_is_opened(address: int)`

> 查询P变量是否已经打开

#### Args

> address(int): int 0~255

#### Returns

> Optional[int]: 0:未启用,1:已启用

#### Examples

```python
from elite import EC

ec = EC(ip="172.16.11.251", auto_connect=True)
```

### `save_var()`

> 保存系统变量数据
>
> 该接口用于，当使用示教器上的备份变量信息前，如果进行变量数据的修改后，用该接口刷新保存变量数据以便于备份的数据为最新数据

#### Args

> 

#### Returns

> bool: 成功 True,失败 False

#### Examples

```

```

### `get_digital_io(address: str, auto_print: bool=False)`

>  获取机器人的数字量状态

#### Args

> address (str): io地址,X0~X63/Y0~Y63/M0~1535
>
> auto_print (bool, optional): 自动打印变量值. Defaults to False.

#### Returns

> Optional[int]: io状态,0低电平,1高电平

#### Examples

```python

```

### `set_digital_io(address:str, value: int)`

>  设置机器人的数字量状态

#### Args

> address (str): Y0~Y63/M528~M799
>
> value (int): 0 / 1

#### Returns

> Optional[bool]: 成功 True,失败 False

#### Examples

```python

```

### `get_registers(address: int, length: int)`

>  读取连续多个的虚拟寄存器(M)

#### Args

> address(int): 起始地址
>
> length (int): 读取长度(位数)

#### Returns

> List[int]: 虚拟IO值列表(每16个虚拟io值用一个十进制整数进行表示,列表长度为len)

#### Examples

```python

```

### `get_analog_input(address: int)`

>  获取模拟量输入

#### Args

> address(int): 0~2

#### Returns

> float: 模拟量输入电压 -10~10

#### Examples

```python

```

### `get_analog_output(address: int)`

>  获取模拟量输入

#### Args

> address(int): 0~4

#### Returns

> float: 模拟量输出电压

#### Examples

```python

```

### `set_analog_output(address: int, value: float)`

>  获取模拟量输入

#### Args

> address(int): 模拟量地址 0~4
>
> value (float): 模拟量值 -10~10,address=4时,value=[0,10]

#### Returns

> bool: 成功 True,失败 False

#### Examples

```python

```

