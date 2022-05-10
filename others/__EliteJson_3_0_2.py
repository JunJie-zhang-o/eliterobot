#! /usr/bin/env python3
# -*- coding:UTF-8 -*-

'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 14:53:17
Description: 用于Elite-ec机器人8055端口访问
'''
import copy
import socket
import json
import sys
import time
import hashlib
from loguru import logger

"""
    Version: 3.0.2
    使用说明:
        1 使用前请先安装 loguru,在命令行中 pip install loguru (请确保安装python版本和实际运行为同一版本).
        2 该库封装的8055接口基于 send_CMD,如需自行封装,可以通过调用send_CMD 函数实现,代码如下:

        --------------------------------------------------------------------    
            # 生成对象
            ec = Elite(ip = "192.168.1.200", auto_connect=True)
            # 以设置伺服状态为例
            cmd = "set_servo_status"
            param = {"status":1}
            print(ec.send_CMD(cmd, param))  # 发送的结果可以直接打印
            # 断开连接
            ec.disconnect_ETController()
        --------------------------------------------------------------------    

        3 部分接口在旧版本之间可能出现无法使用的情况.
        4 接口的实际用法请参考 "SDK_socket" 手册.
"""
"""
    该库接口与SDK手册接口对应规则:
        1 同样一个操作如果有获取和设置两种操作.
            参考:
                io_get()            io_set()
                robot_sync_set()    robot_sync_get()
                
        2 如果只有设置或只有获取操作.
            参考:
                get_tcp_in_now_user()
                get_drag_info()

        3 和机器人本身运动相关的接口,以robot开头.
            参考:
                robot_server_on()
                robot_move_line()
                robot_TT_init()
""" 

class Elite:

    def __init__(self, ip="192.168.1.200", auto_connect=False, get_version=False) -> None:
        self.ip = ip
        self.connect_state = False
        self.__log_init()
        
        if auto_connect:
            self.connect_ETController(self.ip)
            if get_version:
                self.soft_version = self._robot_get_soft_version()
                self.servo_version = self._robot_get_servo_version()

    
    def __log_init(self):
        """日志格式化
        """
        logger.remove()
        self.logger = copy.deepcopy(logger)
        format_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<yellow>Robot_ip: " + self.ip + "</yellow>|line:{line}| <level>{level} | {message}</level>"
        self.logger.add(sys.stderr, format = format_str)
        logger.add(sys.stdout)
        pass    


    def us_sleep(self,t):
        """ us级延时(理论上可以实现us级)
        单位: us
        """
        start, end = 0, 0
        start = time.time()
        t = (t-500)/1000000     #\\500为运行和计算的误差
        while end-start < t:
            end = time.time()


    def _set_sock_sendBuf(self, send_buf: int, is_print: bool=False):
        """设置socket发送缓存区大小

        Args:
            send_buf (int): 要设置的缓存区的大小
            is_print (bool, optional): 是否打印数据. Defaults to False.
        """
        if is_print:
            before_send_buff = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            self.logger.info(f"befor_send_buff: {before_send_buff}")
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf)
            time.sleep(1)
            after_send_buff = self.sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            self.logger.info(f"after_send_buff: {after_send_buff}")
            time.sleep(1)
        else:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf)


    def connect_ETController(self, ip: str, port: int=8055, timeout: float=2):
        """连接EC系列机器人8055端口

        Args:
            ip (str): 机器人ip
            port (int, optional): SDK端口号. Defaults to 8055.
            timeout (float, optional): TCP通信的超时时间. Defaults to 2.

        Returns:
            [tuple]: (True/False,socket/None),返回的socket套接字已在该模块定义为全局变量
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)   # 设置nodelay
        # self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        # sock.settimeout(timeout)
        
        try:
            self.sock.connect((ip,port))
            self.logger.debug(ip + " connect success")
            self.connect_state = True
            return (True,self.sock)
        except Exception as e:
            self.sock.close()
            self.logger.critical(ip + " connect fail")
            quit()
            return (False, None)
    

    def disconnect_ETController(self):
        """断开EC机器人的8055端口
        """
        # global sock
        if(self.sock):
            self.sock.close()
            self.sock=None
        else:
            self.sock=None
            self.logger.critical("socket have already closed")


    def send_CMD(self, cmd: str, params: dict = None, id: int = 1, ret_flag: bool = 1):
        """向8055发送指定命令

        Args:
            cmd (str): 指令
            params (dict, optional): 参数. Defaults to None.
            id (int, optional): id号. Defaults to 1.
            ret_flag (bool, optional): 发送数据后是否接收数据,0不接收,1接收. Defaults to 1.

        Returns:
            [str]: 对应指令返回的信息或错误信息
        """
        if(not params):
            params = []
        else:
            params = json.dumps(params)
        sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(cmd,params,id)+"\n"
        
        try:
            self.sock.sendall(bytes(sendStr,"utf-8"))
            if ret_flag == 1:               
                ret = self.sock.recv(1024)
                jdata = json.loads(str(ret,"utf-8"))
                if("result" in jdata.keys()):
                    if jdata["id"] != id :
                        self.logger.warning("id match fail,send_id={0},recv_id={0}",id,jdata["id"])
                    return (json.loads(jdata["result"]))
                
                elif("error" in jdata.keys()):
                    self.logger.error(f"CMD: {cmd} | {jdata['error']['message']}")
                    return (False,jdata["error"]['message'],jdata["id"])
                else:
                    return (False,None,None)
        except Exception as e:
            self.logger.error(f"CMD: {cmd} | {e}")
            quit()
            return (False,None,None)


# 
    def _robot_get_soft_version(self, is_print: bool=False):
        """获取控制器软件版本号
        """
        self.soft_version = self.send_CMD("getSoftVersion")
        if is_print:
            print(self.send_CMD("getSoftVersion"))


    def _robot_get_servo_version(self):
        """获取伺服版本号
        """
        for i in range(8):
            print("轴%i对应伺服版本为%i" %(i,self.send_CMD("getJointVersion",{"axis":i})))


    def __robot_server_on(self):
        """获取机器人模式,然后同步,清报警,上伺服
        """
        state_str = ["please set Robot Mode to remote","MotorStatus sync faile","Alarm clear faile","servo status set faile"]
        state = 0
        robot_mode = self.send_CMD("getRobotMode")
        if str(robot_mode) == "2":
            state=1
            # 编码器同步
            if not self.send_CMD("getMotorStatus"):
                if self.send_CMD("syncMotorStatus"):
                    state=2
                    self.logger.debug("MotorStatus sync success")
                    time.sleep(0.2)
            else:
                state=2
                self.logger.debug("MotorStatus have already synced")
                time.sleep(0.2)
            # 清报警(并不是强制清除报警),上伺服
            if state==2 and self.send_CMD("clearAlarm",{"force":0}):
                state=3
                self.logger.debug("Alarm clear success")
                time.sleep(0.2)
                if self.send_CMD("set_servo_status",{"status":1}):
                    self.logger.debug("servo status set success")
                    return True
        self.logger.error(state_str[state])
        return False
    
    
# 伺服服务
    def robot_server_on(self):
        """获取机器人模式,然后同步,清报警,上伺服
        """
        state_str = ["please set Robot Mode to remote","Alarm clear faile","MotorStatus sync faile","servo status set faile"]
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
    
    
    def robot_mode_get(self):
        """获取机器人的模式

        Returns:
            [int]: 0示教,1运行,2远程
        """
        return self.send_CMD("getRobotMode")
    
    
    def robot_state_get(self):
        """获取机器人运行状态
            #!本指令获取的急停状态只会短暂存在,很快会被报警覆盖,如果需要获取急停状态,请使用robot_get_estop_status()
            
        Returns:
            [int]: 0停止,1暂停,2急停,3运行,4错误,5碰撞
        """
        return self.send_CMD("getRobotState")
    
    
    def robot_get_estop_status(self):
        """获取机器人的紧急停止状态(硬件的状态)

        Returns:
            int: 0:非急停,1: 急停
        """
        return self.send_CMD("get_estop_status")
    
    
    def robot_servo_get(self):
        """获取伺服状态

        Returns:
            [int]]: True启用,False未启用
        """
        return self.send_CMD("getServoStatus")
    
    
    def robot_servo_set(self, status: int = 1):
        """设置机器人伺服状态

        Args:
            status (int, optional): 1上伺服,0下伺服. Defaults to 1.

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("set_servo_status",{"status":status})
        
        
    def robot_sync_set(self):
        """编码器同步

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("syncMotorStatus")
    
    
    def robot_sync_get(self):
        """获取同步状态

        Returns:
            [bool]: True同步,False未同步
        """
        return self.send_CMD("getMotorStatus")
    
    
    def robot_clear_alarm(self):
        """清除报警

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("clearAlarm")


    def robot_move_prepare(self):
        """运动前准备,目前只判断当前是否正在运动
        其他情况暂不做考虑
        """
        if self.send_CMD("getRobotState") == 3:
            self.send_CMD("stop")
            return True
        else:
            return True


    def wait_stop(self):
        """等待机器人运动停止
        """
        while True:
            time.sleep(0.005)
            result = self.robot_state_get()
            if result != 3:
                if result != 0:
                    str_ = ["","state of robot in the pause","state of robot in the emergency stop","","state of robot in the error","state of robot in the collision"]
                    self.logger.debug(str_[result])
                    break
                break
        self.logger.info("The robot has stopped")


    def robot_calibrate_encoder_zero(self):
        """编码器零位校准,如果可以校准则返回True并不在乎校准结果,如果不可以校准,返回error,

        Returns:
            bool: 成功 True,失败 False
        """
        return self.send_CMD("calibrate_encoder_zero_position")

# 参数服务 
    def cycle_mode_get(self):
        """获取机器人的循环模式

        Returns:
            int: 0:单步,1:单循环,2:连续循环
        """
        return self.send_CMD("getCycleMode")

    
    def cycle_mode_set(self, cycle_mode: int):
        """设置机器人的循环模式

        Args:
            cycle_mode (int): 0:单步,1:单循环,2:连续循环

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCycleMode", {"cycle_mode":cycle_mode})


    def get_Current_job_line(self):
        """获取当前jbi程序的运行行号(为示教器行号-1)

        Returns:
            int: 当前jbi程序的运行行号
        """
        return self.send_CMD("getCurrentJobLine")


    def tool_num_teach_get(self):
        """获取示教模式下机器人的当前工具号

        Returns:
            int: 0~7,示教模式下机器人的当前工具号
        """
        return self.send_CMD("getToolNumber")


    def tool_num_teach_set(self, target_tool_num: int):
        """设置示教模式下机器人的当前工具号,工具坐标系的工具号不会发送改变,以下方工具号为准
        
        Args:
            target_tool_num (int): 工具号,0~7

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setToolNumber", {"tool_num":target_tool_num})


    def tool_num_run_get(self):
        """获取远程模式下机器人的当前工具号

        Returns:
            int: 0~7,远程模式下机器人的当前工具号
        """
        return self.send_CMD("getAutoRunToolNumber")
    
    
    def tool_num_run_set(self, tool_num: int):
        """设置远程模式下机器人的当前工具号

        Args:
            tool_num (int): 工具号0~7

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setAutoRunToolNumber", {"tool_num":tool_num})
    

    def get_tool_coord(self, tool_num: int, unit_type: int=None):
        """获取工具坐标系的数据

        Args:
            tool_num (int): 工具号 0~7
            unit_type (int, optional): 返回的单位类型,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 对应工具号的数据
        """
        if unit_type is not None:
            return self.send_CMD("getTcpPos",{"tool_num":tool_num, "unit_type":unit_type})
        else:
            return self.send_CMD("getTcpPos",{"tool_num":tool_num})


    def current_user_num_get(self):
        """获取当前的用户坐标号

        Returns:
            int: 0~7,当前的用户坐标系
        """
        return self.send_CMD("getUserNumber")
    
    
    def current_user_num_set(self, target_user_num: int):
        """设置机器人的当前用户坐标号(三种模式统一)
        remote
        Args:
            target_user_num (int): 0~7,用户坐标号

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setUserNumber", {"user_num":target_user_num})


    def user_coord_get(self, user_num: int, unit_type: int=None):
        """获取用户坐标系数据

        Args:
            user_num (int): 用户坐标号,0~7
            unit_type (int, optional): 返回数据的单元,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 返回对应的用户坐标系数据
        """
        if unit_type is not None:
            return self.send_CMD("getUserFrame",{"user_num":user_num, "unit_type":unit_type})
        else:
            return self.send_CMD("getUserFrame",{"user_num":user_num})
    
    
    def user_coord_set(self, user_num: int, frame_value: list, unit_type: int=None):
        """设置用户坐标系的数据
        remote
        Args:
            user_num (int): 用户坐标系序号0~7
            frame_value (list): 坐标系的数据
            unit_type (int, optional): 传入及返回的单位类型,0:角度,1:弧度. Defaults to None.

        Returns:
            bool: True操作成功,False操作失败
        """
        if unit_type is not None:
            return self.send_CMD("setUserFrame",{"user_num":user_num, "user_frame":frame_value,"unit_type":unit_type})
        else:
            return self.send_CMD("setUserFrame",{"user_num":user_num, "user_frame":frame_value})
    
    
    def get_tcp_in_now_user(self, unit_type: int=None):
        """获取当前TCP在当前用户坐标系下的位姿

        Args:
            unit_type (int, optional): 返回单位类型,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 当前TCP在当前用户坐标系下的位姿
        """
        if unit_type is not None:
            return self.send_CMD("getTcpPoseInUser",{"unit_type":unit_type})
        else:
            return self.send_CMD("getTcpPoseInUser")


    def get_base_flange_in_cart(self, unit_type: int=None):
        """当前的法兰盘位姿

        Args:
            unit_type (int, optional): 返回数据单位,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 返回的法兰盘中心位姿
        """
        if unit_type is not None:
            return self.send_CMD("get_base_flange_pose",{"unit_type":unit_type})
        else:
            return self.send_CMD("get_base_flange_pose")


    def get_base_flange_in_user(self, unit_type: int=None):
        """法兰盘在当前用户坐标系下的位姿

        Args:
            unit_type (int, optional): 返回数据单位,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 法兰盘中心在用户坐标系下的位姿
        """
        if unit_type is not None:
            return self.send_CMD("get_user_flange_pose",{"unit_type":unit_type})
        else:
            return self.send_CMD("get_user_flange_pose")


    def payload_get(self, tool_num: int):
        """获取指定工具号中的负载值和负载质心

        Args:
            tool_num (int): 0~7,工具号

        Returns:
            tuple: 设定的负载值,负载质心
        """
        # mass = self.send_CMD("getPayload", {"tool_num":tool_num})             #2.19.2该接口不推荐使用
        # center_mass = self.send_CMD("getCentreMass", {"tool_num":tool_num})   #2.19.2该接口不推荐使用
        payload = self.send_CMD("get_tool_payload", {"tool_num":tool_num})
        mass, center_mass = payload["m"], payload["tool_cog"]        
        return mass,center_mass


    def payload_set(self, tool_num: int, mass: float, barycenter:list):
        """设置对应工具号的负载值

        Args:
            tool_num (int): 工具号0~7
            mass (float): 负载重量
            barycenter (list): 重心[x,y,z]

        Returns:
            bool: True操作成功,False操作失败
        """
        # return self.send_CMD("cmd_set_payload", {"tool_num":tool_num, "m":mass, "point":barycenter}) #2.19.2 参数point不推荐使用
        return self.send_CMD("cmd_set_payload", {"tool_num":tool_num, "m":mass, "cog":barycenter})
    

    def collision_state_get(self):
        """获取碰撞状态(示教器右下角的碰撞状态图标)

        Returns:
            int: 0:未发生碰撞,1:发生碰撞
        """
        return self.send_CMD("getCollisionState")


    def collision_state_reset(self):
        """清楚碰撞状态(启动不能无法复位碰撞状态)

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("resetCollisionState")


    def collision_enable_get(self):
        """碰撞检测使能状态

        Returns:
            int: 0:未使能,1:使能
        """
        return self.send_CMD("get_collision_enable_status")


    def collision_enable_set(self, enable: int):
        """设置碰撞使能

        Args:
            enable (int): 1:打开,0:关闭

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCollisionEnable",{"enable":enable})

    
    def collision_sensitivity_get(self):
        """获取碰撞灵敏度

        Returns:
            int: 当前的碰撞灵敏度
        """
        return self.send_CMD("getCollisionSensitivity")


    def collision_sensitivity_set(self, sensitivity: int):
        """设置碰撞灵敏度
        remote
        Args:
            sensitivity (int): 0~100

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCollisionSensitivity",{"value":sensitivity})

    
    def get_robot_type(self):
        """获取机器人类型

        Returns:
            tuple: 机器人类型(int),子类型(int)
        """
        robot_type = self.send_CMD("getRobotType")
        robot_sub_type = self.send_CMD("getRobotSubtype")
        if robot_type != 62:
            self.logger.critical("The Robot type error, Please check Robot's organization parameters")
        return robot_type, robot_sub_type

    
    def get_DH(self, index: int=None):
        """获取机器人的DH参数

        Args:
            index (int, optional): 连杆序号0~11对应1~12. Defaults to None,get all.

        Returns:
            float/list: 单个连杆值或全部连杆值
        """
        if index is not None:
            return self.send_CMD("getDH",{"index":index})
        else:
            link = [self.send_CMD("getDH",{"index":i}) for i in range(11)]
            return link


    def get_sys_password(self):
        """获取自动生成的加密字符串

        Returns:
            str: 加密字符串
        """
        return self.send_CMD("get_remote_sys_password")


    def get_md5_password(self, remote_pwd: str):
        """自动生成设置安全参数使能的匹配密码

        Args:
            remote_pwd (str): 机器人当前的远程密码

        Returns:
            str: 当前远程密码对应的设置安全参数的匹配密码
        """
        word = hashlib.md5()
        pwd1 = self.get_sys_password()
        word.update(pwd1.encode("utf-8"))
        word.update(remote_pwd.encode("utf-8"))
        return word.hexdigest()


    def safety_func_set(self, password: str, enable:int, mode: int, power: float, momentum: float, tool_force: float, elbow_force: float, speed: float, collision_enable: int=None, collision_sensitivity: int=None):
        """设置安全参数

        Args:
            password (str): 安全参数密码,具体参考手册
            enable (int): 安全限制参数使能,1:使能,0:不使能
            mode (int): 模式,0:正常模式,1:缩减莫斯
            power (float): 功率,80~1500
            momentum (float): 动量,5~90
            tool_force (float): 工具力,100~400
            elbow_force (float): 肘部力,100~400
            speed (float): 速度百分比,0~100
            collision_enable (int): 碰撞检测开关,0:关闭,1:打开
            collision_senitivity(int): 碰撞检测灵敏度,10~100
            
        Returns:
            bool: True操作成功,False操作失败
        """
        param_dict = {"password":password, "enable":enable, "mode":mode,
                    "power":power, "momentum":momentum, "tool_force":tool_force,
                    "elbow_force":elbow_force, "speed":speed}
        if collision_enable is not None:
            param_dict.update({"collision_enable":collision_enable})
        if collision_sensitivity is not None:
            param_dict.update({"collision_sensitivity":collision_sensitivity})
                
        return self.send_CMD("setSafetyParams",param_dict)


    def safety_func_get(self):
        """获取安全参数内容

        Returns:
            list: [使能状态,[正常功率,缩减功率],[正常动量,缩减动量],[正常工具力,缩减工具力],[正常肘部力,缩减肘部力],[正常速度百分比,缩减速度百分比]]
        """
        safety_enable = self.send_CMD("getRobotSafetyParamsEnabled")
        safety_power = self.send_CMD("getRobotSafeyPower")
        safety_momentum = self.send_CMD("getRobotSafetyMomentum")
        safety_toolForce = self.send_CMD("getRobotSafetyToolForce")
        safety_elbowForce = self.send_CMD("getRobotSafetyElbowForce")
        safety_speed_percentage = self.send_CMD("getRobotSpeedPercentage")
        return [safety_enable, safety_power, safety_momentum, safety_toolForce, safety_elbowForce, safety_speed_percentage]

    
    def get_joint_v_acc(self, mode: int=None):
        """获取关节速度/加速度

        Args:
            mode (int, optional): 0:获取速度和加速度,1:获取速度,2:获取加速度. Defaults to None.

        Returns:
            list: [[v1,v2,v3,v4,v5,v6,v7,v8],[acc1,acc2,acc3,acc4,acc5,acc6,acc7,acc8]]/[v1,v2,v3,v4,v5,v6,v7,v8]/[acc1,acc2,acc3,acc4,acc5,acc6,acc7,acc8]
        """
        if mode == 0 or mode == None:
            joint_v = self.send_CMD("get_joint_speed")
            joint_acc = self.send_CMD("get_joint_acc")
            return joint_v,joint_acc
        elif mode == 1:
            joint_v = self.send_CMD("get_joint_speed")
            return joint_v
        elif mode == 2:
            joint_acc = self.send_CMD("get_joint_acc")
            return joint_acc
            
            
    def get_tcp_v_acc(self, mode: int=None):
        """获取TCP速度/加速度

        Args:
            mode (int, optional): 0:获取速度和加速度,1:获取速度,2:获取加速度. Defaults to None.

        Returns:
            list: [[v_x,v_y,v_z,v_rx,v_ry,v_rz],[acc_x,acc_y,acc_z,acc_rx,acc_ry,acc_rz]]/v_x,v_y,v_z,v_rx,v_ry,v_rz]/[acc_x,acc_y,acc_z,acc_rx,acc_ry,acc_rz]
        """
        if mode == 0 or mode == None:
            tcp_v = self.send_CMD("get_tcp_speed")
            tcp_acc = self.send_CMD("get_tcp_acc")
            return tcp_v,tcp_acc
        elif mode == 1:
            tcp_v = self.send_CMD("get_tcp_speed")
            return tcp_v
        elif mode == 2:
            tcp_acc = self.send_CMD("get_tcp_acc")
            return tcp_acc
            
            
    def get_Current_encode(self):
        """获取机器人当前编码器值列表

        Returns:
            list: [encode_1,encode_2,encode_3,encode_4,encode_5,encode_6,encode_7,encode_8]
        """
        return self.send_CMD("getCurrentEncode")
            
            
    def get_motor_speed(self):
        """获取机器人马达速度

        Returns:
            list: [speed_1,speed_2,speed_3,speed_4,speed_5,speed_6,speed_7,speed_8]
        """
        # return self.send_CMD("getMotorSpeed")        # 2.19.2 不推荐使用
        return self.send_CMD("get_motor_speed")        
            
            
    def get_joint_torques(self):
        """获取机器人当前力矩信息

        Returns:
            list: [torque_1,torque_2,torque_3,torque_4,torque_5,torque_6,torque_7,torque_8]
        """
        return self.send_CMD("getRobotTorques")
            
            
    def tool_btn_func_get(self,button_num: int=None):
        """获取机器人末端按钮功能

        Args:
            button_num (int, optional): None:获取两个按钮的功能,0:获取蓝色按钮功能,1:获取绿色按钮功能. Defaults to None.

        Returns:
            list/int: 0:禁用,1:拖动,2:记点
        """
        if button_num is not None:
            blue_btn = self.send_CMD("checkFlangeButtonFlangeButton", {"button_num":0})
            green_btn = self.send_CMD("checkFlangeButtonFlangeButton", {"button_num":1})
            return blue_btn,green_btn
        else:
            return self.send_CMD("checkFlangeButtonFlangeButton", {"button_num":button_num})


    def tool_btn_func_set(self,button_num: int, func: int):
        """设置末端按钮功能

        Args:
            button_num (int): 0:蓝色按钮,1:绿色按钮
            func (int): 0:禁用,1:拖动,2:记点
        """
        return self.send_CMD("setFlangeButton",{"button_num":button_num,"state":func})


    def drag_teach_switch(self, mode: int):
        """拖动示教开关

        Args:
            mode (int): 0:关,1:开

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("drag_teach_switch",{"switch": mode})


    def get_drag_info(self, mode: int=None):
        """获取拖动相关参数

        Args:
            mode (int, optional): 0:获取最大启动速度和力矩误差,1:获取最大启动速度,2:获取力矩误差. Defaults to None.

        Returns:
            list/float: [最大启动速度,力矩误差]/最大启动速度/力矩误差
        """
        if mode == 0 or mode == None:
            max_speed = self.send_CMD("getRobotDragStartupMaxSpeed")
            max_torque = self.send_CMD("getRobotTorqueErrorMaxPercents")
            return max_speed,max_torque
        elif mode == 1:
            max_speed = self.send_CMD("getRobotDragStartupMaxSpeed")
            return max_speed
        elif mode == 2:
            max_torque = self.send_CMD("getRobotTorqueErrorMaxPercents")
            return max_torque


    def get_robot_alarm_info(self):
        """获取机器人本体异常情况

        Returns:
            str: 返回最近5条机器人报警编号的字符串
        """
        return self.send_CMD("getAlarmNum")


# 运动学服务
    def pose_2_joint(self, pose: list ,ref_joint: list = None, unit_type: int = None):
        """运动学逆解

        Args:
            pose (list): 需要进行逆解的位姿
            ref_joint (list): 参考关节角
            unit_type (int, optional): 输入和返回位姿的单位类型,0: 角度,1: 弧度. Defaults to 1.

        Returns:
            list: 逆解后的关节角
        """
        if ref_joint == None:
            if unit_type is not None:
                return self.send_CMD("inverseKinematic",{"targetPose":pose, "unit_type":unit_type})
            else:
                return self.send_CMD("inverseKinematic",{"targetPose":pose})
        else:
            if unit_type is not None:
                return self.send_CMD("inverseKinematic",{"targetPose":pose,"referencePos":ref_joint, "unit_type":unit_type})
            else:
                return self.send_CMD("inverseKinematic",{"targetPose":pose,"referencePos":ref_joint})


    def joint_2_pose(self, joint: list, unit_type: int=None):
        """运动学正解

        Args:
            joint (list): 需要进行正解的关节角
            unit_type (int, optional): 输入和返回位姿的单位类型,0: 角度,1: 弧度. Defaults to 1.

        Returns:
            list: 正解后的位姿数据
        """
        if unit_type is not None:
            return self.send_CMD("positiveKinematic",{"targetPos":joint, "unit_type":unit_type})
        else:
            return self.send_CMD("positiveKinematic",{"targetPos":joint})


    def pose_mul(self, pose1: list, pose2: list, unit_type: int=None):
        """位姿相乘

        Args:
            pose1 (list): 位姿信息
            pose2 (list): 位姿信息
            unit_type (int, optional): 输入和返回位姿的单位类型,0: 角度,1: 弧度. Defaults to 1.

        Returns:
            list: 位姿相乘后的结果
        """
        if unit_type is not None:
            return self.send_CMD("poseMul",{"pose1":pose1, "pose2":pose2, "unit_type":unit_type})
        else:
            return self.send_CMD("poseMul",{"pose1":pose1, "pose2":pose2})
        

    def pose_inv(self, pose: list, unit_type: int=None):
        """位姿求逆

        Args:
            pose (list): 要求逆的位姿
            unit_type (int, optional): 输入和返回位姿的单位类型,0: 角度,1: 弧度. Defaults to 1.

        Returns:
            list: 求逆后的结果
        """
        if unit_type is not None:
            return self.send_CMD("poseInv",{"pose1":pose, "unit_type":unit_type})
        else:
            return self.send_CMD("poseInv",{"pose1":pose})
        
        
    def cartPose_2_userPose(self, cart_pose: list, user_no: int, unit_type: int=None):
        """基坐标系位姿转化为用户坐标系位姿

        Args:
            cart_pose (list): 基坐标系下的位姿数据
            user_no (int): 用户坐标系号
            unit_type (int, optional): 输入和返回位姿的单位类型,0: 角度,1: 弧度. Defaults to 1.

        Returns:
            list: 用户坐标系下的位姿信息
        """
        if unit_type is not None:
            return self.send_CMD("convertPoseFromCartToUser",{"TargetPose":cart_pose, "userNo":user_no, "unit_type":unit_type})
        else:
            return self.send_CMD("convertPoseFromCartToUser",{"TargetPose":cart_pose, "userNo":user_no})
            
        
    def userPose_2_cartPose(self, user_pose: list, user_no: int, unit_type: int=None):
        """用户坐标系转化为基坐标系

        Args:
            user_pose (list): 用户坐标系下的数据
            user_no (int): 用户坐标系号
            unit_type (int, optional): 输入和返回位姿的单位类型,0: 角度,1: 弧度. Defaults to 1.

        Returns:
            list: 基坐标系下的位姿信息
        """
        if unit_type is not None:
            return self.send_CMD("convertPoseFromUserToCart",{"TargetPose":user_pose, "userNo":user_no, "unit_type":unit_type})
        else:
            return self.send_CMD("convertPoseFromUserToCart",{"TargetPose":user_pose, "userNo":user_no})


    def _get_now_pose(self):
        """获取当前机器人的位姿信息
            旧接口,不推荐使用
        Returns:
            list: 机器人当前的位姿信息
        """
        return self.send_CMD("getRobotPose")
    
    
    def get_tcp_pose(self, coord_num: int = -1, tool_num: int = -1, unit_type: int = None):
        """获取机器人当前位姿信息
            addBy2.19.2
            #!coord_num和tool_num单独使用,则返回基坐标系下的机器人位姿
            
        Args:
            coord_num (int, optional): [-1,7],-1:基坐标系,0~7:用户坐标系. Defaults to -1.
            tool_num (int, optional): [-1,7],-1:当前工具号,0~7:对应工具号. Defaults to -1.
            unit_type (int, optional): 返回pose的姿态的单位类型,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 机器人当前位姿信息
        """
        if unit_type is not None:
            return self.send_CMD("get_tcp_pose", {"coordinate_num":coord_num, "tool_num":tool_num, "unit_type":unit_type})
        else:
            return self.send_CMD("get_tcp_pose", {"coordinate_num":coord_num, "tool_num":tool_num})
            


    def _get_now_joint(self):
        """获取当前机器人的关节信息
        
        Returns:
            list: 机器人当前的关节信息
        """
        return self.send_CMD("getRobotPos")
      
    
    def get_now_joint(self):
        """获取机器人输出端关节位置信息(为软件计算后的数值)
            addBy2.19.2
        Returns:
            list: 机器人的位置信息
        """
        return self.send_CMD("get_joint_pos")
    
    
    def get_motor_pos(self):
        """获取机器人输入端关节信息(该信息为从电机直接获取的数据)

        Returns:
            list: 机器人输入端关节位置信息
        """
        return self.send_CMD("get_motor_pos")


    def get_servo_precise_position_status(self, is_block: bool=False):
        """获取机器人的编码器精确状态

        Args:
            is_block (bool, optional): 阻塞查询机器人的编码器精确状态,直至为精确状态. Defaults to False.
        Returns:
            int: 1:精确,0:非精确
        """
        self.logger.info("Querying the exact state of the encoder...")
        if is_block == True:
            while 1:
                encoder_status = self.send_CMD("get_servo_precise_position_status")
                if encoder_status == 1: 
                    self.logger.info("The robot's servo status is precise")
                    break
                time.sleep(0.002)
        return self.send_CMD("get_servo_precise_position_status")

# 运动服务
    def robot_stop(self):
        """停止机器人运动

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("stop")


    def robot_run(self):
        """机器人自动运行,暂停后重新运行使用

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("run")
    
    
    def robot_pause(self):
        """机器人暂停

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("pause")
    
    
    def robot_run_speed_set(self, speed:float):
        """设置机器人运行的速度
            适用于2.13.1及以上版本
        Args:
            speed (float): 速度,0.05-100

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("setSpeed",{"value":speed})
    
    
    def robot_run_speed_get(self):
        """获取机器人运行的速度

        Returns:
            float: 自动运行下的速度
        """
        return self.send_CMD("getSpeed")
    
    
    def current_coord_get(self):
        """获取机器人当前坐标系

        Returns:
            int: 关节0,直角1,工具2,用户3,圆柱4
        """
        return self.send_CMD("getCurrentCoord")
    
    
    def current_coord_set(self, coord: int):
        """指定机器人当前坐标系

        Args:
            coord (int): 关节0,直角1,工具2,用户3,圆柱4

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("setCurrentCoord",{"coord_mode":coord})
        
        
# jbi文件处理
    def jbi_is_exist(self, file_name: str):
        """检查jbi文件是否存在

        Args:
            file_name (str): jbi文件名

        Returns:
            int: 0: 不存在 1: 存在
        """
        return self.send_CMD("checkJbiExist",{"filename":file_name})


    def jbi_run(self, file_name: str):
        """运行jbi文件

        Args:
            file_name (str): 待运行文件名

        Returns:
            bool: True 成功 False 失败
        """
        return self.send_CMD("runJbi",{"filename":file_name})
    
    
    def jbi_run_state(self, file_name):
        """获取jbi文件运行状态

        Args:
            file_name (str): jbi文件名

        Returns:
            int: 0 停止状态,1 暂停状态,2 急停状态,3 运行状态,4 错误状态
        """
        return self.send_CMD("getJbiState",{"filename":file_name})
    
    
# 关节运动
    def robot_move_joint(self, target_joint: list, speed: float, acc: int = None, dec: int = None, cond_type: int=None, cond_num: int=None,cond_value: int=None):
        """关节运动,运行后需要根据机器人运动状态去判断是否运动结束

        Args:
            target_joint (list): 目标关节数据,为8个,6个会报错
            speed (float): 关节速度百分比
            acc (int, optional): 加速度,不写默认为0. Defaults to 0.
            dec (int, optional): 减速度,不写默认为0. Defaults to 0.
            cond_type (int, optional): IO类型,0为输入,1为输出
            cond_num (int, optional): IO地址,0~63
            cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        params = {"targetPos":target_joint,"speed":speed}
        if acc is not None: params["acc"] = acc
        if dec is not None: params["dec"] = dec
        if cond_type is not None: params["cond_type"] = cond_type
        if cond_num is not None: params["cond_num"] = cond_num
        if cond_value is not None: params["cond_value"] = cond_value

        return self.send_CMD("moveByJoint",params)
        
        
    def robot_move_line(self, target_joint: list, speed: int, speed_type: int=None, acc: int = None, dec: int = None, cond_type: int=None, cond_num: int=None,cond_value: int=None):
        """直线运动,运行后需根据机器人运动状态去判断是否运动结束

        Args:
            target_joint (list): 目标关节数据
            speed (int): 直线速度: 1-3000；旋转角速度: 1-300；
            speed_type (int, optional): 0为V直线速度,1为VR旋转角速度,2为AV,3为AVR. Defaults to None.
            acc (int, optional): 加速度,不写默认为0. Defaults to None.
            dec (int, optional): 减速度,不写默认为0. Defaults to None.
            cond_type (int, optional): IO类型,0为输入,1为输出.
            cond_num (int, optional): IO地址,0~63.
            cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令.

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        params = {"targetPos":target_joint,"speed":speed}
        if speed_type is not None: params["speed_type"] = speed_type
        if acc is not None: params["acc"] = acc
        if dec is not None: params["dec"] = dec
        if cond_type is not None: params["cond_type"] = cond_type
        if cond_num is not None: params["cond_num"] = cond_num
        if cond_value is not None: params["cond_value"] = cond_value
        return self.send_CMD("moveByLine", params)
    
    
    def robot_move_speed_j(self, vj: list, acc: float, t: float):
        """关节匀速运动

        Args:
            vj (list): 8个关节的速度值,单位: 度/秒
            acc (float): 关节加速度 大于0, 度/s**2
            t (float): 关节匀速运动的时间

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        return self.send_CMD("moveBySpeedj",{"vj":vj, "acc":acc, "t":t})


    def robot_move_stop_speed_j(self, stop_acc: int):
        """停止关节匀速运动

        Args:
            stop_acc (int): 以此加速度停止运动,>0

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        return self.send_CMD("stopj", {"acc":stop_acc})

    
    def robot_move_speed_l(self, v: list, acc: float, t: float, arot: float=None):
        """直线匀速运动

        Args:
            v (list): 沿6个方向运动的速度值,前三个单位为mm/s,后三个为度/s
            acc (float): 位移加速度,>0,单位mm/s**2
            t (float): 直线匀速运动总时间, >0 
            arot (float, optional): 姿态加速度,>0,单位度/s**2. Defaults to None.

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        params = {"v":v, "acc":acc, "t":t}
        if arot is not None:
            params["arot"] = arot
        return self.send_CMD("moveBySpeedl", params)
    
    
    def robot_move_stop_speed_l(self, stop_acc:int):
        """停止直线匀速运动

        Args:
            stop_acc (int): 以此加速度停止运动,范围:>0

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        return self.send_CMD("stopl", {"acc":stop_acc})

    
    def _robot_move_rotate(self, target_joint: list, speed: int, speed_type: int=0, acc: int=0, dec: int=0):
        """旋转运动,其实就是直线运动,该接口为旧接口,是以前区分直线运动的角速度

        Args:
            target_joint (list): 目标关节数据
            speed (int): 直线速度: 1-3000；旋转角速度: 1-300；
            speed_type (int, optional): 0为V直线速度,1为VR旋转角速度,2为AV,3为AVR. Defaults to 0.
            acc (int, optional): 加速度. Defaults to 0.
            dec (int, optional): 减速度. Defaults to 0.

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败
        """
        return self.send_CMD("moveByRotate",{"targetPos":target_joint, "speed_type":speed_type, "speed":speed})

        
    def robot_move_by_line_coord(self, target_user_pose: list, speed: float, speed_type: int, user_coord: list, acc: int=0, dec: int=0, cond_type: int=None, cond_num: int=None, cond_value: int=None, unit_type: int=None):
        """指定坐标系下直线运动

        Args:
            target_user_pose (list): 指定坐标系下的位姿.
            speed (float): 直线速度: 1-3000；旋转角速度: 1-300.
            speed_type (int): 0为V直线速度,1为VR旋转角速度,2为AV,3为AVR.
            user_coord (list): 指定坐标系的数据.
            acc (int, optional): 加速度. Defaults to 0.
            dec (int, optional): 减速度. Defaults to 0.
            cond_type (int, optional): IO类型,0为输入,1为输出.
            cond_num (int, optional): IO地址,0~63.
            cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令.
            unit_type (int, optional): 用户坐标的rx、ry、rz,0:角度,1: 弧度. Defaults to 1.
        """
        params = {"targetUserPose":target_user_pose, "speed":speed, "speed_type":speed_type}
        if user_coord is not None: params["user_oord"] = user_coord
        if acc is not None: params["acc"] = acc
        if dec is not None: params["dec"] = dec
        if cond_type is not None: params["cond_type"] = cond_type
        if cond_num is not None: params["cond_num"] = cond_num
        if cond_value is not None: params["cond_value"] = cond_value
        if unit_type is not None: params["unit_type"] = unit_type

        return self.send_CMD("moveByLineCoord", params)
    
    
# jog运动
    def robot_jog(self, index: int, speed: float=None):
        """jog运动: 
                停止发送jog命令后,机器人并不会立马停止运动,需要通过stop命令去停止
                超过1s未接收到下一条jog运动,停止接收,机器人jog运动停止
        Args:
            index (int): 0~11 偶数为负方向运动,奇数位正反向运动
            speed (float, optional): 0.05 ~ 100. Defaults to None.

        Returns:
            bool: 执行结果,True: 执行成功,False: 执行失败    
        """
        if speed:
            return self.send_CMD("jog",{"index":index,"speed":speed})
        else:
            return self.send_CMD("jog",{"index":index})
    
    
# 路点运行部分
    def robot_path_clear_joint(self):
        """清除路点信息2.0

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("clearPathPoint")


    def robot_path_move(self):
        """路点运动

        Returns:
            [int]: 失败-1,成功: 路点总个数
        """
        return self.send_CMD("moveByPath")
        
        
    def robot_path_add_point(self, way_point: list, move_type: int,  speed: float,  smooth: int, speed_type: int=None, cond_type: int = None, cond_num: int = None, cond_value: int = None):
        """添加路点信息
           #!若运动类型为关节运动,则speed_type无效,不推荐使用

        Args:
            way_point (list): 目标位置
            move_type (int): 0 关节运动,1 直线运动(旋转速度由直线速度决定),2 直线运动(直线速度由旋转速度决定),3 圆弧运动
            speed_type (int): 速度类型,0:V(直线速度)对应speed为[1,3000],1:VR(旋转角速度)对应speed为[1-300],2:AV(绝对直线速度)对应[min_AV,max_AV],3:AVR(绝对旋转角速度)对应[min_AVR,max_AVR]
            speed (float): 运动速度,无speed_type参数时,对应关节速度[1,100]、直线及圆弧速度[1,3000],旋转速度[1,300]
            smooth (int): 平滑度,0~7
            cond_type (int, optional): IO类型,0为输入,1为输出.
            cond_num (int, optional): IO地址,0~63.
            cond_value (int, optional): IO状态,0/1,io状态一致时,立即放弃该运动,执行下一条指令.

        Returns:
            [bool]: True操作成功,False操作失败
        """
        params = {"wayPoint":way_point, "moveType":move_type, "speed":speed, "smooth":smooth}
        if speed_type is not None: params["speed_type"] = speed_type
        if cond_type is not None: params["cond_type"] = cond_type
        if cond_num is not None: params["cond_num"] = cond_num
        if cond_value is not None: params["cond_value"] = cond_value
        
        return self.send_CMD("addPathPoint",params)
        
    
    def robot_path_get_index(self):
        """获取机器人当前运行点位序号

        Returns:
            int: 当前运行的点位序号,-1为非路点运动
        """
        return self.send_CMD("getPathPointIndex")
    
    
# moveml运动
    def robot_ml_init_head(self, lenth: int, point_type: int, ref_joint: list, ref_frame: list, ret_flag: int):
        """初始化带时间戳轨迹文件运动
           #!传输的第一个点位的时间戳必须为0
           
        Args:
            lenth (int): 点位数量
            point_type (int): 点位类型,0: 关节,1: 位姿
            ref_joint (list): 参考关节角,如果点位类型为位姿,参考点为第一个点的逆解参考点
            ref_frame (list): 用户坐标系,如果为基座坐标系全为0
            ret_flag (int): 添加点位指令是否有返回值,0无,1有

        Returns:
            [bool]: True操作成功,False操作失败
        """
        self.ml_ret_flag = ret_flag
        return self.send_CMD("start_push_pos",{"path_lenth":lenth, "pos_type":point_type, "ref_joint_pos":ref_joint, "ref_frame":ref_frame, "ret_flag":ret_flag})
    
    
    def robot_ml_push(self, time_stamp: float, pos: list):
        """添加带时间戳文件运动点位

        Args:
            time_stamp (float): 时间戳,大于等于0,且递增单位: s
            pos (list): 点位数据

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("push_pos", {"timestamp":time_stamp, "pos":pos}, ret_flag=self.ml_ret_flag)

    
    def robot_ml_push_end(self):
        """停止添加时间戳点位,并返回push结果,push结果正确返回True

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("stop_push_pos")
    
    
    def robot_ml_check_push_result(self):
        """检查push结果

        Returns:
            int: 0:push点位和时间戳正确,-1:点位长度不符,-2:点位格式错误,-3:时间戳不规范
        """
        return self.send_CMD("check_trajectory")
    
    
    def robot_ml_flush(self):
        """清空缓存

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("flush_trajectory")
     
    
    def robot_ml_start(self, speed_percent: float=0.1):
        """开始运行带时间戳的轨迹文件

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("start_trajectory",{"speed_percent":speed_percent})
    
    
    def robot_ml_pause(self):
        """暂停运行带时间戳的轨迹文件

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("pause_trajectory")
    
    
    def robot_ml_stop(self):
        """停止运行带时间戳的轨迹运动

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("stop_trajectory")
        
        
    def robot_ml_resume(self):
        """恢复运行带时间戳的轨迹文件

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("resume_trajectory")
        
        
# 透传运动部分
    def robot_TT_init(self, t: int = 10, lookahead: int = 400, smoothness: float = 0.1, response_enable: int = None):
        """机器人透传初始化

        Args:
            t (int, optional): 采样时间(ms),2~100 . Defaults to 10.
            lookahead (int, optional): 前瞻时间(ms),10~1000 . Defaults to 400.
            smoothness (float, optional): 增益,0~1 . Defaults to 0.1.
            response_enable(int, optional): 添加点位指令是否有回复,不写默认有返回值,0:无返回值,1:有返回值.
        """

        if self.robot_TT_state() :
            self.logger.debug("透传状态已开启,透传缓存自动清空中")
            time.sleep(0.5)
            if self.robot_TT_clear_buff():
                self.logger.debug("透传缓存已清空,透传开始初始化")
        self.logger.debug("透传初始化中")

        self.TT_ret_flag = 1
        if response_enable is not None:
            self.TT_ret_flag = response_enable
            return self.send_CMD("transparent_transmission_init",{"lookahead":lookahead,"t":t,"smoothness":smoothness,"response_enable":response_enable})
        else:
            return self.send_CMD("transparent_transmission_init",{"lookahead":lookahead,"t":t,"smoothness":smoothness})


    def robot_TT_start_joint(self,joint: list):
        """旧接口,设置透传数据,旧接口有时候会丢失数据

        Args:
            joint (list): 关节数据
        """
        return self.send_CMD("tt_set_current_servo_joint", {"targetPos":joint}, ret_flag = self.TT_ret_flag)


    def robot_TT_add_joint(self,joint: list):
        """透传目标关节点到缓存

        Args:
            joint (list): 目标关节点
        """
        return self.send_CMD("tt_put_servo_joint_to_buf", {"targetPos":joint}, ret_flag = self.TT_ret_flag)


    def robot_TT_add_pose(self, pose: list):
        """添加透传目标位姿点到缓存

        Args:
            pose (list): 目标位姿点
        """
        return self.send_CMD("tt_put_servo_joint_to_buf",{"targetPose":pose}, ret_flag = self.TT_ret_flag)


    def robot_TT_clear_buff(self):
        """清空透传缓存
        """
        return self.send_CMD("tt_clear_servo_joint_buf",{"clear":0})


    def robot_TT_state(self):
        """获取当前机器人是否处于透传状态

        Returns:
            int: 0: 非透传状态   1: 透传状态 
        """
        return self.send_CMD("get_transparent_transmission_state")


# 系统变量部分
    def var_get(self, Type: str, addr: int, auto_print: bool=False):
        """获取系统变量值

        Args:
            Type (str): B/I/D/P/V
            addr (int): 0~255
            auto_print (bool, optional): 自动打印变量值. Defaults to False.

        Returns:
            [type]: 返回获取的变量值
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
        
        
    def var_set(self, Type: str, addr: int, Value):
        """设置系统变量值,remote模式下使用

        Args:
            Type (str): B/I/D/P/V
            addr (int): 0~255
            Value ([type]): 要设置的变量值

        Returns:
            bool: True/False
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
       
            
    def var_P_is_used(self, addr: int):
        """查询P变量是否已经打开

        Args:
            addr (int): int 0~255

        Returns:
            int: 0:未启用,1:已启用
        """
        if addr < 0 or addr > 255:
            self.logger.error("查询P变量状态的区间错误")
        else:
            return self.send_CMD("getSysVarPState",{"addr":addr})

        
    def var_save(self):
        """保存系统变量数据,remote模式下使用

        Returns:
            [type]: True / False
        """
        return self.send_CMD("save_var_data")
        
        
# io服务
    def io_get(self, Type: str, addr: int, auto_print: bool=False):
        """获取机器人的io状态

        Args:
            Type (str): X/Y/M
            addr (int): 0~63/0~63/0~1535
            auto_print (bool, optional): 是否自动打印数据信息. Defaults to False.

        Returns:
            [type]: 0 / 1
        """
        var_name = {"X":[0,127],"Y":[0,127],"M":[0,1535]}
        var_cmd = {"X":"getInput","Y":"getOutput","M_IN":"getVirtualInput","M_OUT":"getVirtualOutput"}
        Type = Type.upper()
        if not Type in var_name:
            self.logger.error("获取数据的变量类型错误")
        else:
            addr_min,addr_max = var_name[Type][0],var_name[Type][1]
            
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
        
        
    def io_set(self, Type: str, addr, value: int):
        """设置机器人的io,remote模式下使用

        Args:
            Type (str): "Y"/"M"
            addr (int): 0~63/528~799
            value (int): 0 / 1

        Returns:
            [bool]: True / False
        """
        var_name = {"Y":[0,63],"M":[528,799]}
        var_cmd = {"Y":"setOutput","M_OUT":"setVirtualOutput"}

        Type = Type.upper()
        if not Type in var_name:
            self.logger.error("获取数据的变量类型错误")
        else:
            addr_min, addr_max = var_name[Type][0],var_name[Type][1]

        if addr < addr_min or addr > addr_max:
            self.logger.error("获取数据的变量区间错误")
        else:
            return self.send_CMD(var_cmd[Type],{"addr":addr,"status":value})
        
        
    def io_read_more_M(self, addr: int, length: int):
        """读取连续多个的虚拟寄存器(M)

        Args:
            addr (int): 其实地址
            length (int): 读取长度

        Returns:
            [type]: 虚拟IO值列表(每16个虚拟io值用一个十进制整数进行表示,列表长度为len)
        """
        return self.send_CMD("getRegisters",{"addr":addr,"len":length})
        
        
    def io_AI_get(self, addr: int):
        """获取模拟量输入

        Args:
            addr (int): 0~2

        Returns:
            float: 模拟量输入电压 -10~10
        """
        return self.send_CMD("getAnalogInput", {"addr":addr})


    def io_AO_get(self, addr: int):
        """获取模拟量输出

        Args:
            addr (int): 0~4

        Returns:
            float: 模拟量输出电压
        """
        return self.send_CMD("get_analog_output", {"addr":addr})
    
    
    def io_AO_set(self, addr: int, value: float):
        """设置模拟量输出

        Args:
            addr (int): 模拟量地址 0~4
            value (float): 模拟量值 -10~10,addr=4时,value=[0,10]

        Returns:
            [bool]: True / False
        """
        return self.send_CMD("setAnalogOutput", {"addr":addr, "value":value})


# Profinet服务
    def get_profinet_int_input(self, addr: int, length: int):
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


if __name__ == "__main__":  
    
    # 机 器 人 IP 地 址
    ip = "192.168.1.200"

    # 生成已经连接的对象    
    ec = Elite(ip, auto_connect=True)

    # 自动上伺服
    if  ec.robot_server_on():
        # 获取当前
        pose = ec.get_tcp_pose()
        print(pose)
        time.sleep(2)

    # 断开机器人的连接
    ec.disconnect_ETController()