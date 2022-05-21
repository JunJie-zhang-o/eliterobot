# Profinet

> Profinet相关接口用于当系统开启prifinet功能后，通过该接口可以获取和控制与外部设备交互的数据

------

### `get_profinet_float_input(addr: int, length: int)`

> 获取profinet float 型输入寄存器的值,addr+legnth<=32

#### Args

> addr (int): [0~31]
>
> length (int): [1~32]

#### Returns

>  List[float]: 寄存器值列表

#### Examples

```

```

### `get_profinet_int_input(addr: int, length: int)`

> 获取profinet int 型输入寄存器的值,addr+legnth<=32

#### Args

> addr (int): [0~31]
>
> length (int): [1~32]

#### Returns

>  List[int]: 寄存器值列表

#### Examples

```

```

### `get_profinet_float_output(addr: int, length: int)`

>  获取profinet float 型输出寄存器的值,addr+legnth<=32

#### Args

> addr (int): [0~31]
>
> length (int): [1~32]

#### Returns

>  List[float]: 寄存器值列表

#### Examples

```

```

### `set_profinet_float_output(addr: int, length: int, values: List[float])`

>  设置profinet float 型输出寄存器的值,addr+length<=32

#### Args

> addr (int): [0~31]
>
> length (int): [1~32]
>
> values (List[float]): 寄存器值列表

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```

```

### `get_profinet_int_output(addr: int, length: int)`

>  获取profinet int 型输出寄存器的值,addr+legnth<=32

#### Args

> addr (int): [0~31]
>
> length (int): [1~32]

#### Returns

>  List[int]: 寄存器值列表

#### Examples

```

```

### `set_profinet_int_output(addr: int, length: int, values: List[float])`

>  设置profinet int 型输出寄存器的值,addr+length<=32

#### Args

> addr (int): [0~31]
>
> length (int): [1~32]
>
> values (List[int]): 寄存器值列表

#### Returns

>  bool: True操作成功,False操作失败

#### Examples

```

```

