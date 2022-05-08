'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-08 18:48:43
Description: 
'''

from ._servo import ECServo
from ._info import ECInfo
from ._kinematics import ECKinematics
from ._move import ECMove
from ._moveml import ECMoveML
from ._movett import ECMoveTT
from ._profinet import ECProfinet
from ._var import ECVar

from loguru import logger
import time



__version__ = "0.0.1"

__recommended_min_robot_version = "3.0.0"




class EC(ECServo, ECInfo, ECKinematics, ECMove, ECMoveML, ECMoveTT, ECProfinet, ECVar):
    
    def __init__(self, ip="192.168.1.200", auto_connect=False, get_version=False) -> None:
        self.ip = ip
        self.connect_state = False
        self.__log_init()
        
        if auto_connect:
            self.connect_ETController(self.ip)
            if get_version:
                self.soft_version = self._robot_get_soft_version()
                self.servo_version = self._robot_get_servo_version()
    
    
    
    def __repr__(self) -> str:
        pass

        # 自定义方法实现 
    # todo:处理透传状态
    def robot_servo_on(self) -> None:
        """自动上伺服,绝大数情况都是成功的
        """
        # 对透传状态进行处理
        
        
        state_str = ["please set Robot Mode to remote","Alarm clear failed","MotorStatus sync failed","servo status set failed"]
        state = 0
        robot_mode = self.robot_mode_get()
        if str(robot_mode) == "2":
            state = 1
            # 清除报警
            if state == 1 :
                clear_num = 0
                # 循环清除报警,排除异常情况
                while 1:
                    self.robot_clear_alarm()
                    time.sleep(0.2)
                    if self.robot_state_get() == 0:
                        state = 2
                        break
                    clear_num += 1
                    if clear_num > 4:
                        self.logger.error("The Alarm can't clear,Please check the robot state")
                        quit()
                self.logger.debug("Alarm clear success")
                time.sleep(0.2)
                # 编码器同步
                if state == 2 and not self.robot_sync_get():
                    if self.robot_sync_set():
                        state = 3
                        self.logger.debug("MotorStatus sync success")
                        time.sleep(0.2)
                        # 循环上伺服
                        while 1:
                            self.robot_servo_set()
                            if self.robot_servo_get() == True:
                                self.logger.debug("servo status set success")
                                return True
                            time.sleep(0.02)
                else:
                    state = 3
                    self.logger.debug("MotorStatus sync success")
                    time.sleep(0.2)
                    # 上伺服
                    if self.robot_servo_set():
                        # 循环上伺服
                        while 1:
                            self.robot_servo_set()
                            if self.robot_servo_get() == True:
                                self.logger.debug("servo status set success")
                                return True
                            time.sleep(0.02)
        self.logger.error(state_str[state])
        quit()
        return False

if __name__ == "__main__":
    
    
    ec = EC(ip="172.16.11.251", auto_connect=True)
    
    ec.mod