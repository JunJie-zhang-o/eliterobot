'''
Author: ZhangJunJie
CreateDate: 
LastEditTime: 2022-05-08 18:44:18
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
    ec_struct = collections.OrderedDict()
    ec_struct['MessageSize'] = 'I'
    ec_struct['TimeStamp'] = 'Q'
    ec_struct['autorun_cycleMode'] = 'B'
    ec_struct['machinePos']= 'd' * 8
    ec_struct['machinePose']= 'd' * 6
    ec_struct['machineUserPose'] = 'd' * 6
    ec_struct['torque'] = 'd' * 8
    ec_struct['robotState'] = 'i'
    ec_struct['servoReady'] = 'i'
    ec_struct['can_motor_run'] = 'i'
    ec_struct['motor_speed'] = 'i' * 8
    ec_struct['robotMode'] = 'i'
    ec_struct['analog_ioInput'] = 'd' * 3
    ec_struct['analog_ioOutput'] = 'd' * 5
    ec_struct['digital_ioInput'] = 'Q'
    ec_struct['digital_ioOutput'] = 'Q'
    ec_struct['collision'] = 'B'
    ec_struct['machineFlangePose'] = 'd' * 6
    ec_struct['machineUserFlangePose'] = 'd' * 6
    ec_struct["emergencyStopState"] = "B"
    ec_struct["tcp_speed"] = "d"
    ec_struct["joint_speed"] = "d" * 8
    ec_struct["tcpacc"] = "d"
    ec_struct["jointacc"] = "d" * 8
    
    
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
    
    SEND_FREQ = 8       # 8ms
    FMT_MSG_SIZE = "I"  # 数据长度信息的默认字节
    
    PORT = 8056
    
    def __init__(self, robot_ip) -> None:
        
        self.ip = robot_ip
        self.robot_info = ECMonitorInfo()        
        self.recv_flag = False   # 是否已经开始接受数据
        self.lock = threading.Lock()

        
    def __first_connect(self) -> None:
        """首次连接,接受并解析出当前版本对应的8056数据包长度
        """
        # 获取当前ECMonitorInfo版本的数据长度信息
        self.__current_msg_size_get()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.ip, self.PORT))
            byte_msg_size = sock.recv(struct.calcsize(self.FMT_MSG_SIZE))
            sock.shutdown(2)
            sock.close()
            self.MSG_SIZE = struct.unpack("!" + self.FMT_MSG_SIZE, byte_msg_size)[0]   # 实际机器人的字节长度
            # 解析出可以使用的字节长度
            self.__msg_size_judgment()
        except socket.timeout as e:
            print(f"Connect IP : {self.ip} Port : {self.PORT} timeout")
            sock.shutdown(2)
            sock.close()
    
    
    def __current_msg_size_get(self) -> None:
        """获取当前版本信息的所有数据长度信息
        """
        temp = 0
        for i in ECMonitorInfo.ec_struct.values():
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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.PORT))
        
        

    def monitor_run(self):
        """监控程序运行
        """

        self.__first_connect()
        self.__socket_create()
        # ? 测试
        self.tt = 0
        self.br = 0
        # ? 测试

        while 1:
            self.lock.acquire()
            
            buffer = None
            buffer = self.sock.recv(self.MSG_SIZE, socket.MSG_WAITALL)
            self.recv_flag = True
            self._recv_buf_size = len(buffer)
            self.tt += 1

            current_unpack_size = 0
            for k, v in (ECMonitorInfo.ec_struct.items()):

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
                    self.sock.close()
                    self.__socket_create() 
                    self.recv_flag = False
                    # ? 测试
                    self.br += 1
                    # ? 测试
                    break

                if len(v) > 1:
                    setattr(self.robot_info, k, [value[i] for i in range(len(v))])
                else:
                    setattr(self.robot_info, k, value[0])

            self.lock.release()
            # self.robot_info_print(is_clear_screen=True)
    
    
    def robot_info_print(self, is_clear_screen: bool= False):
        """打印机器人的当前信息

        Args:
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
        
        if self.recv_flag:
            print(f"Robot IP: {self.ip} | Currnet Version Bytes size: {self.unpack_size} | Current Recv Buffer Size: {self._recv_buf_size} | TT: {self.tt} | BR: {self.br}")
            # print(f"Robot IP: {self.ip} ")
            spilt_line()

            for k, v in (vars(self.robot_info).items()):
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
            time.sleep(0.5)
            if is_clear_screen:
                cls_screen()
        


        
if __name__ == "__main__":

    import threading
    ec = ECMonitor("192.168.1.200")
    # ec = ECMonitor("172.16.11.240")

    thread_ec = threading.Thread(target=ec.monitor_run, args=(), daemon=True)
    thread_ec.start()
    time.sleep(1)
    print("---")
    while 1:
        ec.robot_info_print()
          