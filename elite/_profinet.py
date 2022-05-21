'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-21 16:43:52
Description: 
'''

from typing import List
from ._baseec import BaseEC


class ECProfinet(BaseEC):
    """ECProfinet类,该类实现所有的Profinet相关的数据查询
    """
# Profinet服务
    def get_profinet_int_input(self, addr: int, length: int) -> List[int]:
        """获取profinet int 型输入寄存器的值,addr+legnth<=32

        Args
        ----
            addr (int): [0~31]
            length (int): [1~32]

        Returns
        -------
            List[int]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_int_input_registers",{"addr":addr,"length":length})


    def get_profinet_float_input(self, addr: int, length: int) -> List[float]:
        """获取profinet float 型输入寄存器的值,addr+legnth<=32

        Args
        ----
            addr (int): [0~31]
            length (int): [1~32]

        Returns
        -------
            List[float]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_float_input_registers",{"addr":addr,"length":length})


    def get_profinet_int_output(self, addr: int, length: int) -> List[int]:
        """获取profinet int 型输出寄存器的值,addr+legnth<=32

        Args
        ----
            addr (int): [0~31]
            length (int): [1~32]

        Returns
        -------
            List[int]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_int_output_registers",{"addr":addr,"length":length})


    def set_profinet_int_output(self, addr: int, length: int, values: List[int]) -> bool:
        """设置profinet int 型输出寄存器的值,addr+length<=32

        Args
        ----
            addr (int): [0~31]
            length (int): [1~32]
            values (List[int]): 寄存器值列表
            
        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("set_profinet_int_output_registers", {"addr":addr, "length":length, "value":values})
        

    def get_profinet_float_output(self, addr: int, length: int) -> List[float]:
        """获取profinet float 型输出寄存器的值,addr+legnth<=32

        Args
        ----
            addr (int): [0~31]
            length (int): [1~32]

        Returns
        -------
            List[float]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_float_output_registers",{"addr":addr,"length":length})


    def set_profinet_float_output(self, addr: int, length: int, values: List[float]) -> bool:
        """设置profinet float 型输出寄存器的值,addr+length<=32

        Args
        ----
            addr (int): [0~31]
            length (int): [1~32]
            values (List[float]): 寄存器值列表
            
        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("set_profinet_float_output_registers", {"addr":addr, "length":length, "value":values})
