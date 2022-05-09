'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-09 21:38:58
Description: 
'''

import copy
from enum import Enum
import json
import socket
import sys
import time
from typing import Any, Dict, Union
from loguru import logger

class BaseEC():
    
    
    def _log_init(self):
        """日志格式化
        """
        logger.remove()
        self.logger = copy.deepcopy(logger)
        format_str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<yellow>Robot_ip: " + self.ip + "</yellow>|line:{line}| <level>{level} | {message}</level>"
        self.logger.add(sys.stderr, format = format_str)
        logger.add(sys.stdout)
        pass    


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


    def connect_ETController(self, ip: str, port: int=8055, timeout: float=2) -> tuple:
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
    

    def disconnect_ETController(self) -> None:
        """断开EC机器人的8055端口
        """
        # global sock
        if(self.sock):
            self.sock.close()
            self.sock=None
        else:
            self.sock=None
            self.logger.critical("socket have already closed")


    def send_CMD(self, cmd: str, params: Dict[str,Any] = None, id: int = 1, ret_flag: int = 1) -> Any:
        """向8055发送指定命令

        Args:
            cmd (str): 指令
            params (dict, optional): 参数. Defaults to None.
            id (int, optional): id号. Defaults to 1.
            ret_flag (int, optional): 发送数据后是否接收数据,0不接收,1接收. Defaults to 1.

        Returns:
            [str]: 对应指令返回的信息或错误信息
        """
        if(not params):
            params = {}
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

    class Coord(Enum):
        JOINT_COORD = 0
        CART_COORD = 1
        TOOL_COORD = 2
        USER_COORD = 3
        CYLINDER_COORD = 4


    class ToolCoord(Enum):
        
        TOOL0 = 0   # 工具0
        TOOL1 = 1   # 工具1
        TOOL2 = 2   # 工具2
        TOOL3 = 3   # 工具3
        TOOL4 = 4   # 工具4
        TOOL5 = 5   # 工具5
        TOOL6 = 6   # 工具6
        TOOL7 = 7   # 工具7
        
        
    class UserCoord(Enum):
        
        USER0 = 0   # 用户0
        USER1 = 1   # 用户1
        USER2 = 2   # 用户2
        USER3 = 3   # 用户3
        USER4 = 4   # 用户4
        USER5 = 5   # 用户5
        USER6 = 6   # 用户6
        USER7 = 7   # 用户7
        
    class AngleType(Enum):
        DEG = 0
        RAD = 1
        
        
    class CycleMode(Enum):
        STEP = 0
        CYCLE = 1
        CONTINUOUS_CYCLE = 2
        
    
    class ECSubType(Enum):
        EC63 = 3
        EC66 = 6
        EC612 = 12
        
    class ToolBtn(Enum):
        BLUE_BTN = 0
        GREEN_BTN = 1

    class ToolBtnFunc(Enum):
        DISABLED = 0
        DRAG = 1
        RECORD_POINT = 2
        
    
    class JbiRunState(Enum):
        JBI_IS_STOP  = 0
        JBI_IS_PAUSE = 1
        JBI_IS_ESTOP = 2
        JBI_IS_RUN   = 3
        JBI_IS_ERROR = 4
        
    class MlPushResult(Enum):
        CORRECT = 0
        WRONG_LENGTH = -1
        WRONG_FORMAT = -2
        TIMESTAMP_IS_NOT_STANDARD = -3
        
        
    class RobotMode(Enum):
        """机器人模式
        """
        TECH = 0
        PLAY = 1
        REMOTE = 2
        
    class RobotState(Enum):
        STOP  = 0
        PAUSE = 1
        ESTOP = 2
        PLAY = 3
        ERROR = 4
        COLLISION = 5