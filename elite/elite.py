'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-08 16:32:31
Description: 
'''

import copy
import json
import socket
import sys
import time
from typing import Any, Dict
from loguru import logger

class BaseEC():
    # def __init__(self, ip="192.168.1.200", auto_connect=False, get_version=False) -> None:
    #     self.ip = ip
    #     self.connect_state = False
    #     self.__log_init()
        
    #     if auto_connect:
    #         self.connect_ETController(self.ip)
    #         if get_version:
    #             self.soft_version = self._robot_get_soft_version()
    #             self.servo_version = self._robot_get_servo_version()

    
    def __log_init(self):
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


    def send_CMD(self, cmd: str, params: Dict[str,Any] = None, id: int = 1, ret_flag: int = 1):
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
