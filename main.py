'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-08 23:43:47
Description: 
'''
from enum import Enum
from elite import EC



if __name__ == "__main__":
    
    
    ec = EC(ip="172.16.11.251", auto_connect=True)
    
    ec.logger.info(ec.cycle_mode)
    print(ec._servo_version)
    # ec.logger.info(ec._soft_version)
    print(ec.tool_num_in_teach_mode)
    # ec.tool_num_in_teach_mode = ec.ToolCoord.TOOL0.value
    print(ec.tool_num_in_teach_mode)
    print(type(ec.ToolCoord.TOOL1) == Enum)
    print(ec.user_num)
    print(type(ec.robot_type))
    print(ec.robot_subType)
    print(ec.DH)
    print(ec.remote_sys_password)