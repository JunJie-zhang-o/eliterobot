'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 09:54:04
Description: 
'''

import time
from elite import EC



if __name__ == "__main__":
    
    
    ec = EC(ip="172.16.11.251", name="" ,auto_connect=True)
    print(ec)
    ec.monitor_thread_run()
    a = 0
    while 1:
        ec.monitor_info_print()
        time.sleep(1)
        a += 1
        print(a)
        if a > 5:
            ec.monitor_thread_stop()
            break

    time.sleep(1)

    print(ec.monitor_thread.is_alive())
    time.sleep(1)
    print(ec.current_pose)
    # ec.logger.info(ec.cycle_mode)
    # print(ec._servo_version)
    # # ec.logger.info(ec._soft_version)
    # print(ec.tool_num_in_teach_mode)
    # # ec.tool_num_in_teach_mode = ec.ToolCoord.TOOL0.value
    # print(ec.tool_num_in_teach_mode)
    # print(type(ec.ToolCoord.TOOL1) == Enum)
    # print(ec.user_num)
    # print(type(ec.robot_type))
    # print(ec.robot_subType)
    # print(ec.DH)
    # print(ec.remote_sys_password)