'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-13 17:32:33
Description: 
'''


import time
from elite import EC
from loguru import logger

import matplotlib.pyplot as plt

if __name__ == "__main__":

    logger.add("log.log")

    ec = EC(ip="172.16.11.251", auto_connect=True)

    ec.monitor_thread_run()
    ec.robot_servo_on()
    j1 = [-166.00185643564356, -73.90748762376238, 89.49133663366337, -106.92824074074073, 89.73109567901234,
          0.00038580246913580245]
    ec.move_joint(j1, 30)
    ec.wait_stop()
    time.sleep(2)

    ec.run_jbi("main")
    all_torque = [[], [], [], [], [], [], [], []]
    while 1:
        time.sleep(0.1)
        torque = [int(i) for i in ec.monitor_info.torque]
        for k, v in enumerate(torque):
            all_torque[k].append(v)

        if ec.get_jbi_state("main").value == 0:
            break
        if torque[1] < -50:
            ec.set_var("B", 0, 2)
            # ec.


    print(all_torque)
    plt.plot([i for i in range(len(all_torque[0]))], all_torque[1])
    plt.plot([i for i in range(len(all_torque[0]))], all_torque[2])
    plt.show()