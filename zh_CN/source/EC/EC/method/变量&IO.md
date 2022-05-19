# 变量与IO

### `var_p_is_used(addr: int)`

> 查询P变量是否已经打开
>

#### Args

> addr (int): int 0~255

#### Returns
> Optional[int]: 0:未启用,1:已启用

#### Examples

```python
from elite import EC

ec = EC(ip="172.16.11.251", auto_connect=True)
```

### `save_var()`

> 保存系统变量数据,

#### Args

> 

#### Returns

> bool: 成功 True,失败 False

#### Examples

```python

```

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

### `get_register(addr: int, length: int)`

>  读取连续多个的虚拟寄存器(M)

#### Args

> addr (int): 起始地址
>
> length (int): 读取长度(位数)

#### Returns

> List[int]: 虚拟IO值列表(每16个虚拟io值用一个十进制整数进行表示,列表长度为len)

#### Examples

```python

```

### `get_analog_input(addr: int)`

>  获取模拟量输入

#### Args

> addr (int): 0~2

#### Returns

> float: 模拟量输入电压 -10~10

#### Examples

```python

```

### `get_analog_output(addr: int)`

>  获取模拟量输入

#### Args

> addr (int): 0~4

#### Returns

> float: 模拟量输出电压

#### Examples

```python

```

### `set_analog_output(addr: int, value: float)`

>  获取模拟量输入

#### Args

> addr (int): 模拟量地址 0~4
>
> value (float): 模拟量值 -10~10,addr=4时,value=[0,10]

#### Returns

> bool: 成功 True,失败 False

#### Examples

```python

```

