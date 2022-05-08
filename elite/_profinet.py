'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-08 18:43:22
Description: 
'''

from .elite import BaseEC


class ECProfinet(BaseEC):
    
# Profinet服务
    def get_profinet_int_input(self, addr: int, length: int) -> list:
        """获取profinet int 型输入寄存器的值,addr+legnth<=32

        Args:
            addr (int): [0~31]
            length (int): [1~32]

        Returns:
            int[length]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_int_input_registers",{"addr":addr,"length":length})


    def get_profinet_float_input(self, addr: int, length: int):
        """获取profinet float 型输入寄存器的值,addr+legnth<=32

        Args:
            addr (int): [0~31]
            length (int): [1~32]

        Returns:
            int[length]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_float_input_registers",{"addr":addr,"length":length})


    def profinet_int_output_get(self, addr: int, length: int):
        """获取profinet int 型输出寄存器的值,addr+legnth<=32

        Args:
            addr (int): [0~31]
            length (int): [1~32]

        Returns:
            int[length]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_int_output_registers",{"addr":addr,"length":length})


    def profinet_int_output_set(self, addr: int, length: int, value: list):
        """设置profinet int 型输出寄存器的值,addr+length<=32

        Args:
            addr (int): [0~31]
            length (int): [1~32]
            value (list): 寄存器值列表
            
        Returns:
            bool: True / False
        """
        return self.send_CMD("set_profinet_int_output_registers", {"addr":addr, "length":length, "value":value})
        

    def profinet_float_output_get(self, addr: int, length: int):
        """获取profinet float 型输出寄存器的值,addr+legnth<=32

        Args:
            addr (int): [0~31]
            length (int): [1~32]

        Returns:
            int[length]: 寄存器值列表
        """
        return self.send_CMD("get_profinet_float_output_registers",{"addr":addr,"length":length})


    def profinet_float_output_set(self, addr: int, length: int, value: float):
        """设置profinet float 型输出寄存器的值,addr+length<=32

        Args:
            addr (int): [0~31]
            length (int): [1~32]
            value (list): 寄存器值列表
            
        Returns:
            bool: True / False
        """
        return self.send_CMD("set_profinet_float_output_registers", {"addr":addr, "length":length, "value":value})
