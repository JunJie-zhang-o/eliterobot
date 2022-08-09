'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-17 21:39:00
Description: 
'''

import copy
from enum import Enum
import json
import socket
import sys
import time
from typing import Any, Optional
from loguru import logger
import threading

class BaseEC():

    _communicate_lock = threading.Lock()

    send_recv_info_print = False
    
    # logger.remove(0)
    
    def _log_init(self, ip):
        """日志格式化
        """
        logger.remove()
        self.logger = copy.deepcopy(logger)
        # format_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<yellow>Robot_ip: " + self.ip + "</yellow>|line:{line}| <level>{level} | {message}</level>"
        format_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<yellow>Robot_IP: " + ip + "</yellow>| <level>" + "{level:<8}".ljust(7) +" | {message}</level>"
        self.logger.add(sys.stderr, format = format_str)
        logger.add(sys.stdout)
        pass    


    def __log_init(self, ip):

        def _filter(record):
            """存在多个stderr的输出,根据log_name进行过滤显示
            """
            if record["extra"].get("ip") == ip:
                return True
            return False

        format_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<yellow>Robot_IP: " + ip + "</yellow>| <level>" + "{level:<8}".ljust(7) + "|<cyan>{name}</cyan>:<cyan>{line}</cyan> - | {message}</level>"
        logger.add(sys.stderr, format=format_str, filter=_filter, colorize=True)
        self.logger = logger.bind(ip=ip,).opt(depth=1)


    def us_sleep(self, t):
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

        Args
        ----
            send_buf (int): 要设置的缓存区的大小
            is_print (bool, optional): 是否打印数据. Defaults to False.
        """
        if is_print:
            before_send_buff = self.sock_cmd.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            self.logger.info(f"before_send_buff: {before_send_buff}")
            self.sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf)
            time.sleep(1)
            after_send_buff = self.sock_cmd.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
            self.logger.info(f"after_send_buff: {after_send_buff}")
            time.sleep(1)
        else:
            self.sock_cmd.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, send_buf)


    def connect_ETController(self, ip: str, port: int=8055, timeout: float=2) -> tuple:
        """连接EC系列机器人8055端口

        Args:
            ip (str): 机器人ip
            port (int, optional): SDK端口号. Defaults to 8055.
            timeout (float, optional): TCP通信的超时时间. Defaults to 2.

        Returns
        -------
            [tuple]: (True/False,socket/None),返回的socket套接字已在该模块定义为全局变量
        """
        self.sock_cmd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
        # -------------------------------------------------------------------------------
        # 设置nodelay
        # self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)   # 设置nodelay
        # self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        # sock.settimeout(timeout)
        # -------------------------------------------------------------------------------
        
        try:
            self.sock_cmd.settimeout(5)
            self.sock_cmd.connect((ip,port))
            self.logger.debug(ip + " connect success")
            self.connect_state = True
            return (True,self.sock_cmd)
        except Exception as e:
            self.sock_cmd.close()
            self.logger.critical(ip + " connect fail")
            quit()
            return (False, None)
    

    def disconnect_ETController(self) -> None:
        """断开EC机器人的8055端口
        """
        if(self.sock_cmd):
            self.sock_cmd.close()
            self.sock_cmd=None
        else:
            self.sock_cmd=None
            self.logger.critical("socket have already closed")


    def send_CMD(self, cmd: str, params: Optional[dict] = None, id: int = 1, ret_flag: int = 1) -> Any:
        """向8055发送指定命令

        Args
        ----
            cmd (str): 指令
            params (Dict[str,Any], optional): 参数. Defaults to None.
            id (int, optional): id号. Defaults to 1.
            ret_flag (int, optional): 发送数据后是否接收数据,0不接收,1接收. Defaults to 1.

        Returns
        -------
            Any: 对应指令返回的信息或错误信息
        """
        if(not params):
            params = {}
        else:
            params = json.dumps(params)
        sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(cmd,params,id)+"\n"
        if self.send_recv_info_print:   # print send msg
            self.logger.info(f"Send: Func is {cmd}")
            self.logger.info(sendStr)
        try:
            with BaseEC._communicate_lock :
                self.sock_cmd.sendall(bytes(sendStr,"utf-8"))
                if ret_flag == 1:               
                    ret = self.sock_cmd.recv(1024)
                    jdata = json.loads(str(ret,"utf-8"))

                    if self.send_recv_info_print:   # print recv nsg
                        self.logger.info(f"Recv: Func is {cmd}")
                        self.logger.info(str(ret,"utf-8"))

                    if("result" in jdata.keys()):
                        if jdata["id"] != id :
                            self.logger.warning("id match fail,send_id={0},recv_id={0}",id,jdata["id"])
                        return (json.loads(jdata["result"]))
                    
                    elif("error" in jdata.keys()):
                        self.logger.warning(f"CMD: {cmd} | {jdata['error']['message']}")
                        return (False,jdata["error"]['message'],jdata["id"])
                    else:
                        return (False,None,None)
        except Exception as e:
            self.logger.error(f"CMD: {cmd} |Exception: {e}")
            quit()
            return (False,None,None)


    class Frame(Enum):
        """坐标系(该值用于jog时指定坐标系等)
        """
        JOINT_FRAME    = 0  # 关节坐标系
        BASE_FRAME     = 1  # 笛卡尔坐标系/世界坐标系
        TOOL_FRAME     = 2  # 工具坐标系
        USER_FRAME     = 3  # 用户坐标系
        CYLINDER_FRAME = 4  # 圆柱坐标系


    class ToolNumber(Enum):
        """工具坐标系(该值用于设置查看工具坐标系数据时设定坐标系等)
        """
        TOOL0 = 0   # 工具0
        TOOL1 = 1   # 工具1
        TOOL2 = 2   # 工具2
        TOOL3 = 3   # 工具3
        TOOL4 = 4   # 工具4
        TOOL5 = 5   # 工具5
        TOOL6 = 6   # 工具6
        TOOL7 = 7   # 工具7
        
        
    class UserFrameNumber(Enum):
        """工具坐标系(该值用于设置查看用户坐标系数据时设定坐标系等)
        """
        USER0 = 0   # 用户0
        USER1 = 1   # 用户1
        USER2 = 2   # 用户2
        USER3 = 3   # 用户3
        USER4 = 4   # 用户4
        USER5 = 5   # 用户5
        USER6 = 6   # 用户6
        USER7 = 7   # 用户7
        
        
    class AngleType(Enum):
        """位姿单位(该值用于设定传入和返回位姿数据时的单位)
        """
        DEG = 0     # 角度
        RAD = 1     # 弧度
        
        
    class CycleMode(Enum):
        """循环模式(该值用于查询设置当前的循环模式)
        """
        STEP             = 0    # 单步
        CYCLE            = 1    # 单循环
        CONTINUOUS_CYCLE = 2    # 连续循环
        
    
    class RobotType(Enum):
        """机器人子类型
        """
        EC63  = 3   # EC63
        EC66  = 6   # EC66
        EC612 = 12  # EC612
        
        
    class ToolBtn(Enum):
        """末端按钮
        """
        BLUE_BTN  = 0   # 末端蓝色按钮
        GREEN_BTN = 1   # 末端绿色按钮

    class ToolBtnFunc(Enum):
        """末端按钮功能
        """
        DISABLED     = 0    # 未启用
        DRAG         = 1    # 拖动
        RECORD_POINT = 2    # 拖动记点
        
    
    class JbiRunState(Enum):
        """jbi运行状态
        """
        STOP  = 0           # jbi运行停止    
        PAUSE = 1           # jbi运行暂停
        ESTOP = 2           # jbi运行急停
        RUN   = 3           # jbi运行中
        ERROR = 4           # jbi运行错误
        DEC_TO_STOP = 5     # jbi减速停止中
        DEC_TO_PAUSE = 6    # jbi减速暂停中
        
        
    class MlPushResult(Enum):
        """ml点位push结果
        """
        CORRECT                   = 0       # 正确
        WRONG_LENGTH              = -1      # 长度错误
        WRONG_FORMAT              = -2      # 格式错误
        TIMESTAMP_IS_NOT_STANDARD = -3      # 时间戳不标准
        
        
    class RobotMode(Enum):
        """机器人模式
        """
        TECH   = 0  # 示教模式
        PLAY   = 1  # 运行模式
        REMOTE = 2  # 远程模式
        
        
    class RobotState(Enum):
        """机器人状态
        """
        STOP      = 0   # 停止状态   
        PAUSE     = 1   # 暂停状态
        ESTOP     = 2   # 急停状态
        PLAY      = 3   # 运行状态
        ERROR     = 4   # 错误状态
        COLLISION = 5   # 碰撞状态