'''
Author: ZhangJunJie
CreateDate: 
LastEditTime: 2022-05-16 19:50:18
Description: 
'''
import collections
import socket
import struct
import platform
import os
import time
import threading



class ECMonitorInfo():
    """EC系列机器人8056数据结构
    """

    # 带顺序的字典结构,python3中的字典已经默认有顺序
    _ec_struct = collections.OrderedDict()
    _ec_struct['MessageSize'] = 'I'
    _ec_struct['TimeStamp'] = 'Q'
    _ec_struct['autorun_cycleMode'] = 'B'
    _ec_struct['machinePos']= 'd' * 8
    _ec_struct['machinePose']= 'd' * 6
    _ec_struct['machineUserPose'] = 'd' * 6
    _ec_struct['torque'] = 'd' * 8
    _ec_struct['robotState'] = 'i'
    _ec_struct['servoReady'] = 'i'
    _ec_struct['can_motor_run'] = 'i'
    _ec_struct['motor_speed'] = 'i' * 8
    _ec_struct['robotMode'] = 'i'
    _ec_struct['analog_ioInput'] = 'd' * 3
    _ec_struct['analog_ioOutput'] = 'd' * 5
    _ec_struct['digital_ioInput'] = 'Q'
    _ec_struct['digital_ioOutput'] = 'Q'
    _ec_struct['collision'] = 'B'
    _ec_struct['machineFlangePose'] = 'd' * 6
    _ec_struct['machineUserFlangePose'] = 'd' * 6
    _ec_struct["emergencyStopState"] = "B"
    _ec_struct["tcp_speed"] = "d"
    _ec_struct["joint_speed"] = "d" * 8
    _ec_struct["tcpacc"] = "d"
    _ec_struct["jointacc"] = "d" * 8
    
    
    def __init__(self) -> None:
        self.MessageSize = None
        self.TimeStamp = None
        self.autorun_cycleMode = None
        self.machinePos = [None] * 8
        self.machinePose = [None] * 6
        self.machineUserPose = [None] * 6
        self.torque = [None] * 6
        self.robotState = None
        self.servoReady = None
        self.can_motor_run = None
        self.motor_speed = [None] * 8
        self.robotMode = None
        self.analog_ioInput = [None] * 3
        self.analog_ioOutput = [None] * 5
        self.digital_ioInput = None
        self.digital_ioOutput = None
        self.collision = None
        self.machineFlangePose = [None] * 8
        self.machineUserFlangePose = [None] * 6
        self.emergencyStopState = None
        self.tcp_speed = None
        self.joint_speed = [None] * 8
        self.tcpacc = [None] * 6
        self.jointacc = [None] * 8
        
        
class ECMonitor():
    """EC系列机器人8056监控类实现
    """
    
    __SEND_FREQ = 8       # 8ms
    _FMT_MSG_SIZE = "I"  # 数据长度信息的默认字节
    
    _PORT = 8056
    
    def __init__(self) -> None:
        
        # self.robot_ip = ip
        self.monitor_info = ECMonitorInfo()        
        self._monitor_recv_flag = False   # 是否已经开始接受数据
        self._monitor_lock = threading.Lock()

        
    def __first_connect(self) -> None:
        """首次连接,接受并解析出当前版本对应的8056数据包长度
        """
        # 获取当前ECMonitorInfo版本的数据长度信息
        self.__current_msg_size_get()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.robot_ip, self._PORT))
            byte_msg_size = sock.recv(struct.calcsize(self._FMT_MSG_SIZE))
            sock.shutdown(2)
            sock.close()
            self.MSG_SIZE = struct.unpack("!" + self._FMT_MSG_SIZE, byte_msg_size)[0]   # 实际机器人的字节长度
            # 解析出可以使用的字节长度
            self.__msg_size_judgment()
        except socket.timeout as e:
            print(f"Connect IP : {self.robot_ip} Port : {self._PORT} timeout")
            sock.shutdown(2)
            sock.close()
    
    
    def __current_msg_size_get(self) -> None:
        """获取当前版本信息的所有数据长度信息
        """
        temp = 0
        for i in ECMonitorInfo._ec_struct.values():
            temp += struct.calcsize(i)

        self.version_msg_size = int(temp)    # ECMonitorInfo对应版本的总长度
    
    
    def __msg_size_judgment(self):
        """判断数据长度
        """
        if self.version_msg_size > self.MSG_SIZE:
            self.unpack_size = self.MSG_SIZE
        elif self.version_msg_size < self.MSG_SIZE:
            self.unpack_size = self.version_msg_size    # 结合目前版本和实际机器人上发的字节长度,得出可以使用的字节长度
        
        
    def __socket_create(self):
        """创建socket连接
        """
        self.sock_monitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_monitor.connect((self.robot_ip, self._PORT))
        
        
    def monitor_run(self):
        """监控程序运行
        """
        self.monitor_run_state = True
        self.__first_connect()
        self.__socket_create()
        # ? 测试
        self._tt = 0     # 数据总接受次数
        self.__br = 0     # 重连次数
        # ? 测试

        while 1:
            self._monitor_lock.acquire()
            
            buffer = None
            buffer = self.sock_monitor.recv(self.MSG_SIZE, socket.MSG_WAITALL)
            self._monitor_recv_flag = True
            self._recv_buf_size = len(buffer)
            self._tt += 1

            current_unpack_size = 0
            for k, v in (ECMonitorInfo._ec_struct.items()):

                if current_unpack_size >= self.unpack_size:
                    break
                
                # 计算已解析长度，字节分割
                fmt_size = struct.calcsize(v)
                current_unpack_size += fmt_size
                buff, buffer = buffer[:fmt_size], buffer[fmt_size:]
                # 解包
                value = struct.unpack("!" + v, buff)

                # 包头异常时，重新建立连接
                if k == "MessageSize" and value[0] != self.MSG_SIZE : 
                    self.sock_monitor.close()
                    self.__socket_create() 
                    self._monitor_recv_flag = False
                    # ? 测试
                    self.__br += 1
                    # ? 测试
                    break

                if len(v) > 1:
                    setattr(self.monitor_info, k, [value[i] for i in range(len(v))])
                else:
                    setattr(self.monitor_info, k, value[0])

            self._monitor_lock.release()
            # self.robot_info_print(is_clear_screen=True)
            if self.monitor_run_state == False: 
                self.sock_monitor.close()
                break
    
    
    def monitor_info_print(self,t: float=0.5, is_clear_screen: bool= False):
        """持续显示机器人的当前信息

        Args
        ----
            t (float,optional): 两次数据刷新的时间间隔(即一次数据展示的时间)
            is_clear_screen (bool, optional): 是否自动清屏. Defaults to False.
        """
        def spilt_line():
            print("————————————————————————————————————————————————————————"*2)

        def cls_screen():
            sys_p = platform.system()
            if sys_p == "Windows":
                os.system("cls")
            elif sys_p == "Linux":
                os.system("clear")
        
        if self._monitor_recv_flag:
            print(f"Robot IP: {self.robot_ip} | Current Version Bytes size: {self.unpack_size} | Current Recv Buffer Size: {self._recv_buf_size} | TT: {self._tt} | BR: {self.__br}")
            spilt_line()

            for k, v in (vars(self.monitor_info).items()):
                # 需要再次进行处理的数据
                if k == "TimeStamp":
                    v = time.gmtime(v // 1000)
                    v = time.strftime("%Y-%m-%d %H:%M:%S", v)
                elif k == "digital_ioInput":
                    v = bin(v)[2:].zfill(64)
                elif k == "digital_ioOutput":
                    v = bin(v)[2:].zfill(64)

                print(f"| {k}: {v}")
                spilt_line()
            
            # 清屏
            time.sleep(t)
            if is_clear_screen:
                cls_screen()
        


        
if __name__ == "__main__":

    import threading
    # ec = ECMonitor("192.168.1.200")
    ec = ECMonitor("172.16.11.251")

    thread_ec = threading.Thread(target=ec.monitor_run, args=(), daemon=True)
    thread_ec.start()
    time.sleep(1)
    print("---")
    while 1:
        ec.monitor_info_print()
        
          