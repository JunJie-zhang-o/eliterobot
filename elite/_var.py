'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 10:06:26
Description: 
'''


from typing import List, Optional, Union
from ._baseec import BaseEC



class ECVar(BaseEC):
    # 系统变量部分
    def var_get(self, Type: str, addr: int, auto_print: bool=False) -> Optional[Union[float,int,list]]:
        """获取系统变量值

        Args
        ----
            Type (str): B/I/D/P/V
            addr (int): 0~255
            auto_print (bool, optional): 自动打印变量值. Defaults to False.

        Returns
        -------
            Optional[Union[float,int,list]]: 返回获取的变量值
        """
        Type = Type.upper()
        if not Type in ("B","I","D","P","V"):
            self.logger.error("获取数据的变量类型错误,Type: \"B\" \"I\" \"D\" \"P\" \"V\"")
        if addr < 0 or addr > 255:
            self.logger.error("获取数据的变量区间错误,0 <= addr <= 255")
            self.logger.error("0 <= addr <= 255")
        else:
            var = self.send_CMD("getSysVar"+Type,{"addr":addr})
            if auto_print :
                if Type == "V" or Type == "P":
                    print("%s%03i的值为%.3f,%.3f,%.3f,%.3f,%.3f,%.3f" %(Type,addr,var[0],var[1],var[2],var[3],var[4],var[5]))
                else:
                    print("%s%03i的值为%.3f" %(Type,addr,var))
            return var
        
        
    def var_set(self, Type: str, addr: int, Value) -> Optional[bool]:
        """设置系统变量值,remote模式下使用

        Args
        ----
            Type (str): B/I/D/P/V
            addr (int): 0~255
            Value ([type]): 要设置的变量值

        Returns
        -------
            bool: 成功 True,失败 False
        """
        Type = Type.upper()
        if not Type in ("B","I","D","P","V"):
            self.logger.error("设置数据的变量类型错误,Type: \"B\" \"I\" \"D\" \"P\" \"V\"")
        if addr < 0 or addr > 255:
            self.logger.error("设置数据的变量区间错误,0 <= addr <= 255")
        else:
            param_value = "value"
            if Type == "P" :  param_value = "pos"
            if Type == "V" :  param_value = "pose"
            var = self.send_CMD("setSysVar"+Type,{"addr":addr, param_value:Value})
            return var
       
            
    def var_p_is_used(self, addr: int) -> Optional[int]:
        """查询P变量是否已经打开

        Args
        ----
            addr (int): int 0~255

        Returns
        -------
            Optional[int]: 0:未启用,1:已启用
        """
        if addr < 0 or addr > 255:
            self.logger.error("查询P变量状态的区间错误")
        else:
            return self.send_CMD("getSysVarPState",{"addr":addr})

        
    def var_save(self) -> bool:
        """保存系统变量数据,remote模式下使用

        Returns
        -------
            bool: 成功 True,失败 False
        """
        return self.send_CMD("save_var_data")
    
    
    
    
class IO(BaseEC):
    def io_get(self, Type: str, addr: int, auto_print: bool=False) -> Optional[int]:
        """获取机器人的io状态

        Args
        ----
            Type (str): X/Y/M
            addr (int): 0~63/0~63/0~1535
            auto_print (bool, optional): 是否自动打印数据信息. Defaults to False.

        Returns
        -------
            Optional[int]: io状态,0低电平,1高电平
        """
        var_name = {"X":[0,127],"Y":[0,127],"M":[0,1535]}
        var_cmd = {"X":"getInput","Y":"getOutput","M_IN":"getVirtualInput","M_OUT":"getVirtualOutput"}
        Type = Type.upper()
        if not Type in var_name:
            self.logger.error("获取数据的变量类型错误")
            return None
        else:
            addr_min, addr_max = var_name[Type][0], var_name[Type][1]
            
        if addr < addr_min and addr > addr_max:
            self.logger.error("获取数据的变量区间错误")
        else:
            Type_cope = Type
            if Type == "M" and addr >= 400 : 
                Type_cope = "M_OUT"
            elif Type == "M" :
                Type_cope = "M_IN"
                
            var = self.send_CMD(var_cmd[Type_cope],{"addr":addr})
            if auto_print:
                print("%s%s变量的值为%s" %(Type,addr,var))
            return var
        
        
    def io_set(self, Type: str, addr, value: int) -> Optional[bool]:
        """设置机器人的io,remote模式下使用

        Args
        ----
            Type (str): "Y"/"M"
            addr (int): 0~63/528~799
            value (int): 0 / 1

        Returns
        -------
            Optional[bool]: 成功 True,失败 False
        """
        var_name = {"Y":[0,63],"M":[528,799]}
        var_cmd = {"Y":"setOutput","M_OUT":"setVirtualOutput"}

        Type = Type.upper()
        if not Type in var_name:
            self.logger.error("获取数据的变量类型错误")
            return None
        else:
            addr_min, addr_max = var_name[Type][0],var_name[Type][1]

        if addr < addr_min or addr > addr_max:
            self.logger.error("获取数据的变量区间错误")
        else:
            return self.send_CMD(var_cmd[Type],{"addr":addr,"status":value})
        
        
    def io_read_more_M(self, addr: int, length: int) -> List[int]:
        """读取连续多个的虚拟寄存器(M)

        Args
        ----
            addr (int): 其实地址
            length (int): 读取长度

        Returns
        -------
            List[int]: 虚拟IO值列表(每16个虚拟io值用一个十进制整数进行表示,列表长度为len)
        """
        return self.send_CMD("getRegisters",{"addr":addr,"len":length})
        
        
    def io_AI_get(self, addr: int) -> float:
        """获取模拟量输入

        Args
        ----
            addr (int): 0~2

        Returns
        -------
            float: 模拟量输入电压 -10~10
        """
        return self.send_CMD("getAnalogInput", {"addr":addr})


    def io_AO_get(self, addr: int) -> float:
        """获取模拟量输出

        Args
        ----
            addr (int): 0~4

        Returns
        -------
            float: 模拟量输出电压
        """
        return self.send_CMD("get_analog_output", {"addr":addr})
    
    
    def io_AO_set(self, addr: int, value: float) -> bool:
        """设置模拟量输出

        Args
        ----
            addr (int): 模拟量地址 0~4
            value (float): 模拟量值 -10~10,addr=4时,value=[0,10]

        Returns
        -------
            bool: 成功 True,失败 False
        """
        return self.send_CMD("setAnalogOutput", {"addr":addr, "value":value})
