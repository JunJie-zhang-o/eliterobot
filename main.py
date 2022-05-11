'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 09:54:04
Description: 
'''


import time
from elite import EC

from loguru import logger

if __name__ == "__main__":
    from pprint import pprint
    import inspect
    
    pprint(dir(EC))
    # print(EC.__class__)
    ec = EC(ip="172.16.11.251", name="" ,auto_connect=True)
    # print(ec.run_speed())
    # ec.run_speed = 10
    # print(ec.run_speed)
    
    # print(ec.mode)
    # print(ec.state)
    # print(ec.estop_status)
    # print(ec.servo_status)
    # print(ec.sync_status)
    # help(ec.state.__doc__)
    
    a = [
        "_ECMonitor__current_msg_size_get",
"_ECMonitor__first_connect",
"_ECMonitor__msg_size_judgment",
"_ECMonitor__socket_create",
"_get_now_joint",
"_get_now_pose",
"_log_init",
"_set_sock_sendBuf",
]
    b = 0
    c = 0
    for i in dir(EC):
        # if(hasattr(EC,i)):
        #     print(i)
        if i in a: continue
        if i[1] == "_":
            continue
        if (inspect.ismethod(eval(f"ec.{i}"))):
            print(i)
            b += 1
        c+=1
    print(b,c)
    print(len(dir(EC)))
    # 80+34