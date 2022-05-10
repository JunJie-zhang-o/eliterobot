'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 09:55:26
Description: 
'''

import threading
from typing import Optional, overload
from ._servo import ECServo
from elite._info import ECInfo
from elite._kinematics import ECKinematics
from elite._move import ECMove
from elite._moveml import ECMoveML
from elite._movett import ECMoveTT
from elite._profinet import ECProfinet
from elite._var import ECVar
from elite._monitor import ECMonitor

from loguru import logger
import time



__version__ = "0.0.1"

__recommended_min_robot_version = "3.0.0"




class EC(ECServo, ECInfo, ECKinematics, ECMove, ECMoveML, ECMoveTT, ECProfinet, ECVar, ECMonitor):
    

        
    
    def __init__(self, ip: str = "192.168.1.200",name: Optional[str]="None", auto_connect: bool=False, get_version: bool=False) -> None:
        super().__init__(self)
        self.ip = ip
        self.name = name
        self.connect_state = False
        self._log_init()
        
        if auto_connect:
            self.connect_ETController(self.ip)
            if get_version:
                self.soft_version = self._soft_version
                self.servo_version = self._servo_version
    
    

    def __repr__(self) -> str:
        if self.connect_state:
            return "Elite EC6%s, IP:%s, Name:%s"%(self.robot_subType.value, self.ip, self.name)
        else:
            return "Elite EC__, IP:%s, Name:%s"%(self.ip, self.name)

            


    # 自定义方法实现 
    def robot_servo_on(self) -> bool:
        """自动上伺服,绝大数情况都是成功的
        """
        # 对透传状态进行处理
        if self.TT_state:
            self.logger.debug("The TT state is enabled, and the TT cache is automatically cleared")
            time.sleep(0.5)
            if self.TT_clear_buff():
                self.logger.debug("The TT cache has been cleared")
        
        state_str = ["please set Robot Mode to remote","Alarm clear failed","MotorStatus sync failed","servo status set failed"]
        state = 0
        robot_mode = self.mode
        if str(robot_mode) == "2":
            state = 1
            # 清除报警
            if state == 1 :
                clear_num = 0
                # 循环清除报警,排除异常情况
                while 1:
                    self.clear_alarm()
                    time.sleep(0.2)
                    if self.state == 0:
                        state = 2
                        break
                    clear_num += 1
                    if clear_num > 4:
                        self.logger.error("The Alarm can't clear,Please check the robot state")
                        quit()
                self.logger.debug("Alarm clear success")
                time.sleep(0.2)
                # 编码器同步
                if state == 2 and not self.sync_status:
                    if self.sync():
                        state = 3
                        self.logger.debug("MotorStatus sync success")
                        time.sleep(0.2)
                        # 循环上伺服
                        while 1:
                            self.servo_status_set()
                            if self.servo_status == True:
                                self.logger.debug("servo status set success")
                                return True
                            time.sleep(0.02)
                else:
                    state = 3
                    self.logger.debug("MotorStatus sync success")
                    time.sleep(0.2)
                    # 上伺服
                    if self.servo_status_set():
                        # 循环上伺服
                        while 1:
                            self.servo_status_set()
                            if self.servo_status == True:
                                self.logger.debug("servo status set success")
                                return True
                            time.sleep(0.02)
        self.logger.error(state_str[state])
        quit()
        return False


    def monitor_thread_run(self):
        """运行8056数据监控线程
        
        Examples
        --------
        创建实例
        >>> ec = EC(ip="192.168.1.200", auto_connect=True)
        
        监控线程运行
        >>> ec.monitor_thread_run()
        
        当该方法执行后,可以通过以下方法进行查看监控的数据
        >>> while 1:
        >>>     ec.monitor_info_print()
        >>>     time.sleep(1)
        
        以上方法即会在控制台打印数据
        """
        self.monitor_thread = threading.Thread(target=self.monitor_run, args=(), daemon=True, name="Elibot monitor thread,IP:%s"%(self.ip))
        self.monitor_thread.start()
    
    
    def monitor_thread_stop(self):
        """停止8056数据监控线程
        """
        self.monitor_run_state = False
        self.monitor_thread.join()
    
    

    # def monitor_test