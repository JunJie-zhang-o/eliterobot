'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-08 18:40:42
Description: 
'''
from enum import Enum
import hashlib
import time
from .elite import BaseEC


class ECInfo(BaseEC):

    @property
    def soft_version(self) -> str:
        """获取控制器软件版本号
        """
        return self.send_CMD("getSoftVersion")

    @property
    def servo_version(self) -> str:
        """获取伺服版本号
        """
        servo_versions = ""
        for i in range(6):
            servo_versions += (
                "轴%i对应伺服版本为%i\n" %
                (i, self.send_CMD("getJointVersion", {"axis": i})))
        return servo_versions

    def _get_now_pose(self):
        """获取当前机器人的位姿信息
            旧接口,不推荐使用
        Returns:
            list: 机器人当前的位姿信息
        """
        return self.send_CMD("getRobotPose")

    def get_tcp_pose(self,
                     coord_num: int = -1,
                     tool_num: int = -1,
                     unit_type: int = None):
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
            return self.send_CMD(
                "get_tcp_pose", {
                    "coordinate_num": coord_num,
                    "tool_num": tool_num,
                    "unit_type": unit_type
                })
        else:
            return self.send_CMD("get_tcp_pose", {
                "coordinate_num": coord_num,
                "tool_num": tool_num
            })

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

    def get_servo_precise_position_status(self, is_block: bool = False):
        """获取机器人的编码器精确状态

        Args:
            is_block (bool, optional): 阻塞查询机器人的编码器精确状态,直至为精确状态. Defaults to False.
        Returns:
            int: 1:精确,0:非精确
        """
        self.logger.info("Querying the exact state of the encoder...")
        if is_block == True:
            while 1:
                encoder_status = self.send_CMD(
                    "get_servo_precise_position_status")
                if encoder_status == 1:
                    self.logger.info("The robot's servo status is precise")
                    break
                time.sleep(0.002)
        return self.send_CMD("get_servo_precise_position_status")

    @property
    def run_speed(self):
        """获取机器人运行的速度

        Returns:
            float: 自动运行下的速度
        """
        return self.send_CMD("getSpeed")

    @run_speed.setter
    def run_speed(self, speed: float):
        """设置机器人运行的速度
            适用于2.13.1及以上版本
        Args:
            speed (float): 速度,0.05-100

        Returns:
            [bool]: True操作成功,False操作失败
        """
        return self.send_CMD("setSpeed", {"value": speed})

    class Coord(Enum, int):
        JOINT_COORD = 0
        CART_COORD = 1
        TOOL_COORD = 2
        USER_COORD = 3
        CYLINDER_COORD = 4

    @property
    def current_coord(self) -> Coord:
        """获取机器人当前坐标系

        Returns:
            int: 关节0,直角1,工具2,用户3,圆柱4
        """
        return self.Coord(self.send_CMD("getCurrentCoord"))

    @current_coord.setter
    def current_coord(self, coord: Coord):
        """指定机器人当前坐标系

        Args:
            coord (int): 关节0,直角1,工具2,用户3,圆柱4

        Returns:
            [bool]: True操作成功,False操作失败
        """
        self.Coord.CART_COORD
        return self.send_CMD("setCurrentCoord", {"coord_mode": coord})

    class CycleMode(Enum):
        STEP = 0
        CYCLE = 1
        CONTINUOUS_CYCLE = 2

    @property
    def cycle_mode(self) -> CycleMode:
        """获取机器人的循环模式

        Returns:
            CycleMode: 0:单步,1:单循环,2:连续循环
        """
        return self.CycleMode(self.send_CMD("getCycleMode"))

    @cycle_mode.setter
    def cycle_mode(self, cycle_mode: CycleMode) -> bool:
        """设置机器人的循环模式

        Args:
            cycle_mode (CycleMode): 0:单步,1:单循环,2:连续循环

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCycleMode", {"cycle_mode": cycle_mode})

    @property
    def tool_num_in_teach_mode(self):
        """获取示教模式下机器人的当前工具号

        Returns:
            int: 0~7,示教模式下机器人的当前工具号
        """
        return self.send_CMD("getToolNumber")

    @tool_num_in_teach_mode.setter
    def tool_num_in_teach_mode(self, target_tool_num: int):
        """设置示教模式下机器人的当前工具号,工具坐标系的工具号不会发送改变,以下方工具号为准
        
        Args:
            target_tool_num (int): 工具号,0~7

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setToolNumber", {"tool_num": target_tool_num})

    @property
    def tool_num_in_run_mode(self):
        """获取远程模式下机器人的当前工具号

        Returns:
            int: 0~7,远程模式下机器人的当前工具号
        """
        return self.send_CMD("getAutoRunToolNumber")

    @tool_num_in_run_mode.setter
    def tool_num_in_run_mode(self, tool_num: int):
        """设置远程模式下机器人的当前工具号

        Args:
            tool_num (int): 工具号0~7

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setAutoRunToolNumber", {"tool_num": tool_num})

    def get_tool_coord(self, tool_num: int, unit_type: int = None):
        """获取工具坐标系的数据

        Args:
            tool_num (int): 工具号 0~7
            unit_type (int, optional): 返回的单位类型,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 对应工具号的数据
        """
        if unit_type is not None:
            return self.send_CMD("getTcpPos", {
                "tool_num": tool_num,
                "unit_type": unit_type
            })
        else:
            return self.send_CMD("getTcpPos", {"tool_num": tool_num})

    @property
    def user_num(self):
        """获取当前的用户坐标号

        Returns:
            int: 0~7,当前的用户坐标系
        """
        return self.send_CMD("getUserNumber")

    @user_num.setter
    def user_num(self, target_user_num: int):
        """设置机器人的当前用户坐标号(三种模式统一)
        remote
        Args:
            target_user_num (int): 0~7,用户坐标号

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setUserNumber", {"user_num": target_user_num})

    def user_coord_get(self, user_num: int, unit_type: int = None):
        """获取用户坐标系数据

        Args:
            user_num (int): 用户坐标号,0~7
            unit_type (int, optional): 返回数据的单元,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 返回对应的用户坐标系数据
        """
        if unit_type is not None:
            return self.send_CMD("getUserFrame", {
                "user_num": user_num,
                "unit_type": unit_type
            })
        else:
            return self.send_CMD("getUserFrame", {"user_num": user_num})

    def user_coord_set(self,
                       user_num: int,
                       frame_value: list,
                       unit_type: int = None):
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
            return self.send_CMD(
                "setUserFrame", {
                    "user_num": user_num,
                    "user_frame": frame_value,
                    "unit_type": unit_type
                })
        else:
            return self.send_CMD("setUserFrame", {
                "user_num": user_num,
                "user_frame": frame_value
            })

    def get_tcp_in_now_user(self, unit_type: int = None):
        """获取当前TCP在当前用户坐标系下的位姿

        Args:
            unit_type (int, optional): 返回单位类型,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 当前TCP在当前用户坐标系下的位姿
        """
        if unit_type is not None:
            return self.send_CMD("getTcpPoseInUser", {"unit_type": unit_type})
        else:
            return self.send_CMD("getTcpPoseInUser")

    def get_base_flange_in_cart(self, unit_type: int = None):
        """当前的法兰盘位姿

        Args:
            unit_type (int, optional): 返回数据单位,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 返回的法兰盘中心位姿
        """
        if unit_type is not None:
            return self.send_CMD("get_base_flange_pose",
                                 {"unit_type": unit_type})
        else:
            return self.send_CMD("get_base_flange_pose")

    def get_base_flange_in_user(self, unit_type: int = None):
        """法兰盘在当前用户坐标系下的位姿

        Args:
            unit_type (int, optional): 返回数据单位,0:角度,1:弧度. Defaults to None.

        Returns:
            list: 法兰盘中心在用户坐标系下的位姿
        """
        if unit_type is not None:
            return self.send_CMD("get_user_flange_pose",
                                 {"unit_type": unit_type})
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
        payload = self.send_CMD("get_tool_payload", {"tool_num": tool_num})
        mass, center_mass = payload["m"], payload["tool_cog"]
        return mass, center_mass

    def payload_set(self, tool_num: int, mass: float, barycenter: list):
        """设置对应工具号的负载值

        Args:
            tool_num (int): 工具号0~7
            mass (float): 负载重量
            barycenter (list): 重心[x,y,z]

        Returns:
            bool: True操作成功,False操作失败
        """
        # return self.send_CMD("cmd_set_payload", {"tool_num":tool_num, "m":mass, "point":barycenter}) #2.19.2 参数point不推荐使用
        return self.send_CMD("cmd_set_payload", {
            "tool_num": tool_num,
            "m": mass,
            "cog": barycenter
        })

    @property
    def collision_state(self):
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

    @property
    def collision_enable_status(self):
        """碰撞检测使能状态

        Returns:
            int: 0:未使能,1:使能
        """
        return self.send_CMD("get_collision_enable_status")

    @collision_enable_status.setter
    def collision_enable_status(self, enable: int):
        """设置碰撞使能

        Args:
            enable (int): 1:打开,0:关闭

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCollisionEnable", {"enable": enable})

    @property
    def collision_sensitivity(self):
        """获取碰撞灵敏度

        Returns:
            int: 当前的碰撞灵敏度
        """
        return self.send_CMD("getCollisionSensitivity")

    @collision_sensitivity.setter
    def collision_sensitivity(self, sensitivity: int):
        """设置碰撞灵敏度
        remote
        Args:
            sensitivity (int): 0~100

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCollisionSensitivity", {"value": sensitivity})

    # todo
    def get_robot_type(self):
        """获取机器人类型

        Returns:
            tuple: 机器人类型(int),子类型(int)
        """
        robot_type = self.send_CMD("getRobotType")
        robot_sub_type = self.send_CMD("getRobotSubtype")
        if robot_type != 62:
            self.logger.critical(
                "The Robot type error, Please check Robot's organization parameters"
            )
        return robot_type, robot_sub_type

    # todo
    def get_DH(self, index: int = None):
        """获取机器人的DH参数

        Args:
            index (int, optional): 连杆序号0~11对应1~12. Defaults to None,get all.

        Returns:
            float/list: 单个连杆值或全部连杆值
        """
        if index is not None:
            return self.send_CMD("getDH", {"index": index})
        else:
            link = [self.send_CMD("getDH", {"index": i}) for i in range(11)]
            return link

    # todo
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

    def safety_func_set(self,
                        password: str,
                        enable: int,
                        mode: int,
                        power: float,
                        momentum: float,
                        tool_force: float,
                        elbow_force: float,
                        speed: float,
                        collision_enable: int = None,
                        collision_sensitivity: int = None):
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
        param_dict = {
            "password": password,
            "enable": enable,
            "mode": mode,
            "power": power,
            "momentum": momentum,
            "tool_force": tool_force,
            "elbow_force": elbow_force,
            "speed": speed
        }
        if collision_enable is not None:
            param_dict.update({"collision_enable": collision_enable})
        if collision_sensitivity is not None:
            param_dict.update({"collision_sensitivity": collision_sensitivity})

        return self.send_CMD("setSafetyParams", param_dict)

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
        return [
            safety_enable, safety_power, safety_momentum, safety_toolForce,
            safety_elbowForce, safety_speed_percentage
        ]

    # todo
    @property
    def joint_speed(self) -> list:
        joint_v = self.send_CMD("get_joint_speed")
        return joint_v

    @property
    def tcp_speed(self) -> list:
        tcp_v = self.send_CMD("get_tcp_speed")
        return tcp_v

    @property
    def joint_acc(self) -> list:
        joint_acc = self.send_CMD("get_joint_acc")
        return joint_acc

    @property
    def tcp_acc(self) -> list:
        tcp_acc = self.send_CMD("get_tcp_acc")
        return tcp_acc

    @property
    def motor_speed(self):
        """获取机器人马达速度

        Returns:
            list: [speed_1,speed_2,speed_3,speed_4,speed_5,speed_6,speed_7,speed_8]
        """
        # return self.send_CMD("getMotorSpeed")        # 2.19.2 不推荐使用
        return self.send_CMD("get_motor_speed")

    @property
    def joint_torques(self):
        """获取机器人当前力矩信息

        Returns:
            list: [torque_1,torque_2,torque_3,torque_4,torque_5,torque_6,torque_7,torque_8]
        """
        return self.send_CMD("getRobotTorques")

    @property
    def get_Current_encode(self):
        """获取机器人当前编码器值列表

        Returns:
            list: [encode_1,encode_2,encode_3,encode_4,encode_5,encode_6,encode_7,encode_8]
        """
        return self.send_CMD("getCurrentEncode")

    class ToolBtn(Enum):
        BLUE_BTN = 0
        GREEN_BTN = 1

    class ToolBtnFunc(Enum):
        DISABLED = 0
        DRAG = 1
        RECORD_POINT = 2

    @property
    def blue_tool_btn_func(self) -> ToolBtnFunc:
        """机器人末端蓝色按钮功能

        Returns:
            ToolBtnFunc: DISABLED/DRAG/RECORD_POINT
        """
        return self.ToolBtnFunc(
            self.send_CMD("checkFlangeButtonFlangeButton",
                          {"button_num": self.ToolBtn.BLUE_BTN}))

    @property
    def green_tool_btn_func(self) -> ToolBtnFunc:
        """机器人末端蓝色按钮功能

        Returns:
            ToolBtnFunc: DISABLED/DRAG/RECORD_POINT
        """
        return self.ToolBtnFunc(
            self.send_CMD("checkFlangeButtonFlangeButton",
                          {"button_num": self.ToolBtn.GREEN_BTN}))

    @blue_tool_btn_func.setter
    def blue_tool_btn_func(self, func: ToolBtnFunc):
        """设置机器人末端蓝色按钮功能

        Args:
            func (ToolBtnFunc): DISABLED/DRAG/RECORD_POINT
        """
        self.send_CMD("setFlangeButton", {
            "button_num": self.ToolBtn.BLUE_BTN,
            "state": func
        })

    @green_tool_btn_func.setter
    def green_tool_btn_func(self, func: ToolBtnFunc):
        """设置机器人末端蓝色按钮功能

        Args:
            func (ToolBtnFunc): DISABLED/DRAG/RECORD_POINT
        """
        return self.send_CMD("setFlangeButton", {
            "button_num": self.ToolBtn.BLUE_BTN,
            "state": func
        })

    def drag_teach_switch(self, mode: int):
        """拖动示教开关

        Args:
            mode (int): 0:关,1:开

        Returns:
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("drag_teach_switch", {"switch": mode})

    def get_drag_info(self, mode: int = None):
        """获取拖动相关参数

        Args:
            mode (int, optional): 0:获取最大启动速度和力矩误差,1:获取最大启动速度,2:获取力矩误差. Defaults to None.

        Returns:
            list/float: [最大启动速度,力矩误差]/最大启动速度/力矩误差
        """
        if mode == 0 or mode == None:
            max_speed = self.send_CMD("getRobotDragStartupMaxSpeed")
            max_torque = self.send_CMD("getRobotTorqueErrorMaxPercents")
            return max_speed, max_torque
        elif mode == 1:
            max_speed = self.send_CMD("getRobotDragStartupMaxSpeed")
            return max_speed
        elif mode == 2:
            max_torque = self.send_CMD("getRobotTorqueErrorMaxPercents")
            return max_torque

    @property
    def alarm_info(self):
        """获取机器人本体异常情况

        Returns:
            str: 返回最近5条机器人报警编号的字符串
        """
        return self.send_CMD("getAlarmNum")