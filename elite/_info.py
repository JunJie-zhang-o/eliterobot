'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-22 17:09:56
Description: 
'''
import hashlib
import time
from typing import List, Optional, Union

from ._baseec import BaseEC


class ECInfo(BaseEC):
    """EC信息查询类,该类实现所有的状态数据查询功能
    """
    
    @property
    def soft_version(self) -> str:
        """控制器软件版本号
        
        Returns
        -------
            str: 机器人当前的软件版本号
        
        Examples
        --------
        >>> from elite import EC
        >>> ec = EC(ip="192.168.1.200", auto_connect=True)
        >>> print(ec.soft_version)  # => v3.2.2
        """
        return self.send_CMD("getSoftVersion")


    @property
    def servo_version(self) -> str:
        """伺服版本号
        
        Returns
        -------
            str: 机器人当前的伺服版本号
        
        Examples
        --------
        >>> from elite import EC
        >>> ec = EC(ip="192.168.1.200", auto_connect=True)
        >>> print(ec.servo_version) # => 轴1对应伺服版本为11 轴2对应伺服版本为11 轴3对应伺服版本为11 轴4对应伺服版本为11 轴5对应伺服版本为11 轴6对应伺服版本为11
        """
        servo_versions = ""
        for i in range(6):
            servo_versions += (
                "轴%i对应伺服版本为%i\n" %
                (i+1, self.send_CMD("getJointVersion", {"axis": i})))
        return servo_versions


    def _get_pose(self):
        """获取当前机器人的位姿信息
           旧接口,不推荐使用
           Deprecated
            
        Returns
        -------
            list: 机器人当前的位姿信息
        """
        return self.send_CMD("getRobotPose")


    def get_tcp_pose(self, frame_num: int = -1, tool_num: int = -1, unit_type: Union[int, None] = None) -> List[float]:
        """获取机器人当前位姿信息

        Args
        ----
            frame_num (int, optional): -1:世界坐标系, 0~7:用户坐标系号. Defaults to -1.
            tool_num (int, optional): -1:当前工具号, 0~7:工具坐标系号. Defaults to -1.
            unit_type (int, None], optional): 返回数据单位类型, 0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 机器人对应的位姿信息
            
        Tips:
            当一个参数都不填写时,即为返回当前工具在世界坐标系下的位姿数据
        """

        if unit_type is not None:
            return self.send_CMD("get_tcp_pose", {"coordinate_num": frame_num, "tool_num": tool_num, "unit_type": unit_type})
        else:
            return self.send_CMD("get_tcp_pose", {"coordinate_num": frame_num, "tool_num": tool_num})


    @property
    def current_pose(self) -> List[float]:
        """当前位姿数据

        Returns:
            List[float]: 当前位姿数据
            
        Examples
        --------
        >>> from elite import EC
        >>> ec = EC(ip="192.168.1.200", auto_connect=True)
        >>> print(ec.current_pose)  # => [-116.42876928044629, -445.8173561092616, 330.01911829033054, -2.528732975547022, -0.23334446132951653, 2.9722706513750343]
        """
        return self.get_tcp_pose()
    

    def _get_joint(self) -> List[float]:
        """获取当前机器人的关节信息
           Deprecated
        
        Returns
        -------
            List[float]: 机器人当前的关节信息
        """
        return self.send_CMD("getRobotPos")
    

    def get_joint(self) -> List[float]:
        """获取机器人输出端关节位置信息(为软件计算后的数值)
           
        Returns
        -------
            List[float]: 机器人的位置信息
            
        Minimun Version Require:
            2.19.2
        """
        return self.send_CMD("get_joint_pos")


    @property
    def current_joint(self) -> List[float]:
        """当前关节信息
        """
        return self.get_joint()


    def get_motor_pos(self) -> List[float]:
        """获取机器人输入端关节信息(该信息为从电机直接获取的数据)

        Returns
        -------
            List[float]: 机器人输入端关节位置信息
        """
        return self.send_CMD("get_motor_pos")
    
    
    def _get_tool_coord(self, tool_num: int, unit_type: Optional[int] = None) -> List[float]:
        """获取当前的位姿坐标数据
           Deprecated
        Args:
        -----
            tool_num (int): 工具号 0~7
            unit_type (int, optional):  返回数据单位类型, 0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 对应工具号的数据
        """
        if unit_type is not None:
            return self.send_CMD("getTcpPos", {
                "tool_num": tool_num,
                "unit_type": unit_type
            })
        else:
            return self.send_CMD("getTcpPos", {"tool_num": tool_num})


    def get_servo_precise_position_status(self, is_block: bool = False) -> int:
        """获取机器人的编码器精确状态

        Args:
        -----
            is_block (bool, optional): 阻塞查询机器人的编码器精确状态,直至为精确状态. Defaults to False.
            
        Returns
        -------
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
    def run_speed(self) -> float:
        """获取机器人运行的速度

        Returns
        -------
            float: 自动运行下的速度
        """
        return self.send_CMD("getSpeed")


    @run_speed.setter
    def run_speed(self, speed: float) -> bool:
        """设置机器人运行的速度

        Args:
        -----
            speed (float): 速度,0.05-100

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setSpeed", {"value": speed})


    @property
    def current_frame(self) -> BaseEC.Frame:
        """获取机器人当前坐标系

        Returns
        -------
            BaseEC.Coord: 关节0,直角1,工具2,用户3,圆柱4
        """
        return self.Frame(self.send_CMD("getCurrentCoord"))


    @current_frame.setter
    def current_frame(self, coord: int) -> bool:
        """指定机器人当前坐标系

        Args:
        -----
            coord (int): 关节坐标系0,世界坐标系1,工具坐标系2,用户坐标系3,圆柱坐标系4

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        self.Frame.BASE_FRAME
        return self.send_CMD("setCurrentCoord", {"coord_mode": coord})


    @property
    def cycle_mode(self) -> BaseEC.CycleMode:
        """机器人当前的循环模式

        Returns
        -------
            BaseEC.CycleMode: 0:单步,1:单循环,2:连续循环
        """
        return self.CycleMode(self.send_CMD("getCycleMode"))


    @cycle_mode.setter
    def cycle_mode(self, cycle_mode: int) -> bool:
        """设置机器人的循环模式

        Args:
        -----
            cycle_mode (int): 0:单步,1:单循环,2:连续循环

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCycleMode", {"cycle_mode": cycle_mode})


    @property
    def tool_frame_num_in_teach_mode(self) -> BaseEC.ToolNumber:
        """获取示教模式下机器人的当前工具号

        Returns
        -------
            BaseEC.ToolCoord: 0~7,示教模式下机器人的当前工具号
        """
        return self.ToolNumber(self.send_CMD("getToolNumber"))


    @tool_frame_num_in_teach_mode.setter
    def tool_frame_num_in_teach_mode(self, target_tool_num: int) -> bool:
        """设置示教模式下机器人的当前工具号,工具坐标系的工具号不会发送改变,以下方工具号为准
        
        Args:
        -----
            target_tool_num (int): 工具号,0~7

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setToolNumber", {"tool_num": target_tool_num})


    @property
    def tool_frame_num_in_run_mode(self) -> BaseEC.ToolNumber:
        """获取远程模式下机器人的当前工具号

        Returns
        -------
            ToolCoord: 0~7,远程模式下机器人的当前工具号
        """
        return self.ToolNumber(self.send_CMD("getAutoRunToolNumber"))


    @tool_frame_num_in_run_mode.setter
    def tool_frame_num_in_run_mode(self, tool_num: int) -> bool:
        """设置远程模式下机器人的当前工具号

        Args:
        -----
            tool_num (int): 工具号0~7

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setAutoRunToolNumber", {"tool_num": tool_num})


    @property
    def user_frame_num(self) -> BaseEC.UserFrameNumber:
        """获取当前的用户坐标号

        Returns
        -------
            BaseEC.UserCoord: 0~7,当前的用户坐标系
        """
        return self.UserFrameNumber(self.send_CMD("getUserNumber"))


    @user_frame_num.setter
    def user_frame_num(self, target_user_num: int) -> bool:
        """设置机器人的当前用户坐标号(三种模式统一)

        Args:
        -----
            target_user_num (int): 0~7,用户坐标号

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setUserNumber", {"user_num": target_user_num})
    

    def get_user_frame_data(self, user_num: int, unit_type: Optional[int] = None) -> List[float]:
        """获取用户坐标系数据

        Args:
        -----
            user_num (int): 用户坐标号,0~7
            unit_type (int, optional): 返回数据单位类型, 0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 返回对应的用户坐标系数据
        """
        if unit_type is not None:
            return self.send_CMD("getUserFrame", {
                "user_num": user_num,
                "unit_type": unit_type
            })
        else:
            return self.send_CMD("getUserFrame", {"user_num": user_num})


    def set_user_frame_data(self,
                       user_num: int,
                       frame_value: List[float],
                       unit_type: Optional[int] = None) -> bool:
        """设置用户坐标系的数据

        Args:
        -----
            user_num (int): 用户坐标系序号0~7
            frame_value (List[float]): 坐标系的数据
            unit_type (int, optional): 传入及返回的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        if unit_type is not None:
            return self.send_CMD("setUserFrame", {"user_num": user_num, "user_frame": frame_value, "unit_type": unit_type})
        else:
            return self.send_CMD("setUserFrame", {"user_num": user_num, "user_frame": frame_value})


    def get_pose_in_user_frame(self, unit_type: Optional[int] = None) -> List[float]:
        """获取当前TCP在当前用户坐标系下的位姿

        Args:
        -----
            unit_type (int, optional): 返回单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 当前TCP在当前用户坐标系下的位姿
        """
        if unit_type is not None:
            return self.send_CMD("getTcpPoseInUser", {"unit_type": unit_type})
        else:
            return self.send_CMD("getTcpPoseInUser")


    def get_flange_pose(self, unit_type: Optional[int] = None) -> List[float]:
        """当前的法兰盘位姿

        Args:
        -----
            unit_type (int, optional): 返回数据单位,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 返回的法兰盘中心位姿
        """
        if unit_type is not None:
            return self.send_CMD("get_base_flange_pose", {"unit_type": unit_type})
        else:
            return self.send_CMD("get_base_flange_pose")


    def get_flange_pose_in_user_frame(self, unit_type: Optional[int] = None) -> List[float]:
        """法兰盘在当前用户坐标系下的位姿

        Args:
        -----
            unit_type (int, optional): 返回数据单位,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 法兰盘中心在用户坐标系下的位姿
        """
        if unit_type is not None:
            return self.send_CMD("get_user_flange_pose", {"unit_type": unit_type})
        else:
            return self.send_CMD("get_user_flange_pose")


    # todo:版本提示
    def get_payload(self, tool_num: int) -> List[float]:
        """获取指定工具号中的负载值和负载质心

        Args:
        -----
            tool_num (int): 0~7,工具号

        Returns
        -------
            List[float]: 设定的负载值,负载质心
        """
        # mass = self.send_CMD("getPayload", {"tool_num":tool_num})             #2.19.2该接口不推荐使用
        # center_mass = self.send_CMD("getCentreMass", {"tool_num":tool_num})   #2.19.2该接口不推荐使用
        payload = self.send_CMD("get_tool_payload", {"tool_num": tool_num})
        mass, center_mass = payload["m"], payload["tool_cog"]
        return [mass, center_mass]
    

    def set_payload(self, tool_num: int, mass: float, barycenter: list) -> bool:
        """设置对应工具号的负载值

        Args:
        -----
            tool_num (int): 工具号0~7
            mass (float): 负载重量
            barycenter (list): 重心[x,y,z]

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        # return self.send_CMD("cmd_set_payload", {"tool_num":tool_num, "m":mass, "point":barycenter}) #2.19.2 参数point不推荐使用
        return self.send_CMD("cmd_set_payload", {"tool_num": tool_num, "m": mass, "cog": barycenter})


    @property
    def is_collision(self) -> int:
        """获取碰撞状态(示教器右下角的碰撞状态图标)

        Returns
        -------
            int: 0:未发生碰撞,1:发生碰撞
        """
        return self.send_CMD("getCollisionState")
    

    def clear_collision_alarm(self) -> bool:
        """清楚碰撞状态(启动不能无法复位碰撞状态)

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("resetCollisionState")


    @property
    def collision_enable_status(self) -> int:
        """碰撞检测使能状态

        Returns
        -------
            int: 0:未使能,1:使能
        """
        return self.send_CMD("get_collision_enable_status")


    @collision_enable_status.setter
    def collision_enable_status(self, enable: int) -> bool:
        """设置碰撞使能

        Args:
        -----
            enable (int): 1:打开,0:关闭

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCollisionEnable", {"enable": enable})


    @property
    def collision_sensitivity(self) -> int:
        """获取碰撞灵敏度

        Returns
        -------
            int: 当前的碰撞灵敏度
        """
        return self.send_CMD("getCollisionSensitivity")


    @collision_sensitivity.setter
    def collision_sensitivity(self, sensitivity: int) -> bool:
        """设置碰撞灵敏度
        remote
        Args:
        -----
            sensitivity (int): 0~100

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("setCollisionSensitivity", {"value": sensitivity})


    @property
    def robot_series(self) -> int:
        """机器人类型

        Returns
        -------
            int: 62为协作类型
        """
        return self.send_CMD("getRobotType")


    @property
    def robot_type(self) -> BaseEC.RobotType:
        """机器人子类型

        Returns
        -------
            BaseEC.ECSubType: 3:63,6:66,12:612
        """
        return self.RobotType(self.send_CMD("getRobotSubtype"))


    @property
    def DH_parameters(self) -> List[float]:
        """机器人的所有连杆值

        Returns:
            List[float]: 所有的连杆数据
        """
        link = [self.send_CMD("getDH", {"index": i}) for i in range(11)]
        return link


    @property
    def remote_sys_password(self):
        """远程模式下自动生成的加密字符串
        """
        return self.send_CMD("get_remote_sys_password")


    def get_md5_password(self, remote_pwd: str) -> str:
        """自动生成设置安全参数使能的匹配密码

        Args:
        -----
            remote_pwd (str): 机器人当前的远程密码

        Returns
        -------
            str: 当前远程密码对应的设置安全参数的匹配密码
        """
        word = hashlib.md5()
        pwd1 = self.remote_sys_password
        word.update(pwd1.encode("utf-8"))
        word.update(remote_pwd.encode("utf-8"))
        return word.hexdigest()


    def set_safety_parameters(self,
                        password: str,
                        enable: int,
                        mode: int,
                        power: float,
                        momentum: float,
                        tool_force: float,
                        elbow_force: float,
                        speed: float,
                        collision_enable: Optional[int] = None,
                        collision_sensitivity: Optional[int] = None) -> bool:
        """设置安全参数

        Args:
        -----
            password (str): 安全参数密码,具体参考手册
            enable (int): 安全限制参数使能,1:使能,0:不使能
            mode (int): 模式,0:正常模式,1:缩减莫斯
            power (float): 功率,80~1500
            momentum (float): 动量,5~90
            tool_force (float): 工具力,100~400
            elbow_force (float): 肘部力,100~400
            speed (float): 速度百分比,0~100
            collision_enable (int): 碰撞检测开关,0:关闭,1:打开
            collision_sensitivity(int): 碰撞检测灵敏度,10~100
            
        Returns
        -------
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


    def get_safety_parameters(self) -> list:
        """获取安全参数内容

        Returns
        -------
            list: [使能状态, [正常功率,缩减功率], [正常动量,缩减动量], [正常工具力,缩减工具力], [正常肘部力,缩减肘部力], [正常速度百分比,缩减速度百分比]]
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


    @property
    def joint_speed(self) -> List[float]:
        """当前各关节速度

        Returns:
            List[float]: 各关节速度
        """
        return self.send_CMD("get_joint_speed")


    @property
    def tcp_speed(self) -> float:
        """当前的tcp速度

        Returns:
            float: 对应tcp速度
        """
        return self.send_CMD("get_tcp_speed")


    @property
    def joint_acc(self) -> float:
        """当前各关节加速度

        Returns:
            float: 各关节加速度
        """
        return self.send_CMD("get_joint_acc")


    @property
    def tcp_acc(self) -> float:
        """当前TCP加速度

        Returns:
            float: 对应tcp加速度
        """
        return self.send_CMD("get_tcp_acc")


    @property
    def motor_speed(self) -> List[float]:
        """当前获取机器人马达速度

        Returns
        -------
            List[float]: [speed_1,speed_2,speed_3,speed_4,speed_5,speed_6,speed_7,speed_8]
        """
        # return self.send_CMD("getMotorSpeed")        # 2.19.2 不推荐使用
        return self.send_CMD("get_motor_speed")


    @property
    def joint_torques(self) -> List[float]:
        """获取机器人当前力矩信息

        Returns
        -------
            List[float]: [torque_1,torque_2,torque_3,torque_4,torque_5,torque_6,torque_7,torque_8]
        """
        return self.send_CMD("getRobotTorques")


    @property
    def encoder_values(self) -> List[float]:
        """获取机器人当前编码器值列表

        Returns
        -------
            List[float]: [encode_1,encode_2,encode_3,encode_4,encode_5,encode_6,encode_7,encode_8]
        """
        return self.send_CMD("getCurrentEncode")


    @property
    def blue_tool_btn_func(self) -> BaseEC.ToolBtnFunc:
        """机器人末端蓝色按钮功能

        Returns
        -------
            ToolBtnFunc: DISABLED/DRAG/RECORD_POINT
        """
        return self.ToolBtnFunc(
            self.send_CMD("checkFlangeButton",
                          {"button_num": self.ToolBtn.BLUE_BTN.value}))


    @property
    def green_tool_btn_func(self) -> BaseEC.ToolBtnFunc:
        """机器人末端绿色按钮功能

        Returns
        -------
            ToolBtnFunc: DISABLED/DRAG/RECORD_POINT
        """
        return self.ToolBtnFunc(
            self.send_CMD("checkFlangeButton",
                          {"button_num": self.ToolBtn.GREEN_BTN.value}))


    @blue_tool_btn_func.setter
    def blue_tool_btn_func(self, func: int):
        """设置机器人末端蓝色按钮功能

        Args:
        -----
            func (int): 0禁用, 1拖动, 2记点
        """
        self.send_CMD("setFlangeButton", {"button_num": self.ToolBtn.BLUE_BTN, "state": func})


    @green_tool_btn_func.setter
    def green_tool_btn_func(self, func: int):
        """设置机器人末端蓝色按钮功能

        Args:
        -----
            func (int): 0禁用, 1拖动, 2记点
        """
        return self.send_CMD("setFlangeButton", {"button_num": self.ToolBtn.BLUE_BTN, "state": func})


    def switch_drag_teach(self, mode: int):
        """拖动示教开关

        Args:
        -----
            mode (int): 0:关,1:开

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("drag_teach_switch", {"switch": mode})


    def get_drag_info(self, mode: Optional[int] = None) -> Optional[Union[List[float], float]]:
        """获取拖动相关参数

        Args:
        -----
            mode (int, optional): 0:获取最大启动速度和力矩误差,1:获取最大启动速度,2:获取力矩误差. Defaults to None.

        Returns
        -------
            Optional[Union[List[float], float]]: [最大启动速度,力矩误差]/最大启动速度/力矩误差
        """
        if mode == 0 or mode == None:
            max_speed:float = self.send_CMD("getRobotDragStartupMaxSpeed")
            max_torque:float = self.send_CMD("getRobotTorqueErrorMaxPercents")
            return [max_speed, max_torque]
        elif mode == 1:
            max_speed:float = self.send_CMD("getRobotDragStartupMaxSpeed")
            return max_speed
        elif mode == 2:
            max_torque:float = self.send_CMD("getRobotTorqueErrorMaxPercents")
            return max_torque


    @property
    def alarm_info(self):
        """获取机器人本体异常情况

        Returns
        -------
            str: 返回最近5条机器人报警编号的字符串
        """
        return self.send_CMD("getAlarmNum")
