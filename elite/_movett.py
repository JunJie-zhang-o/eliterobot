'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-21 17:14:43
Description: 
'''
import time

from ._baseec import BaseEC
from typing import List, Optional

class ECMoveTT(BaseEC):
    """EC透传服务类,该类实现所有的透传相关接口
    """
    # 透传运动部分
    def TT_init(self, t: int = 10, lookahead: int = 400, smoothness: float = 0.1, response_enable: Optional[int] = None) -> bool:
        """透传模式初始化

        Args
        ----
            t (int, optional): 采样时间(ms),2~100 . Defaults to 10.
            lookahead (int, optional): 前瞻时间(ms),10~1000 . Defaults to 400.
            smoothness (float, optional): 增益,0~1 . Defaults to 0.1.
            response_enable(int, optional): 添加点位指令是否有回复,不写默认有返回值,0:无返回值,1:有返回值.

        Returns
        -------
            bool: True操作成功,False操作失败
        """

        if self.TT_state:
            self.logger.debug("透传状态已开启,透传缓存自动清空中")
            time.sleep(0.5)
            if self.TT_clear_buff():
                self.logger.debug("透传缓存已清空,透传开始初始化")
        self.logger.debug("透传初始化中")

        self.TT_ret_flag = 1
        if response_enable is not None:
            self.TT_ret_flag = response_enable
            return self.send_CMD("transparent_transmission_init",{"lookahead":lookahead,"t":t,"smoothness":smoothness,"response_enable":response_enable})
        else:
            return self.send_CMD("transparent_transmission_init",{"lookahead":lookahead,"t":t,"smoothness":smoothness})


    def TT_start_joint(self, joint: List[float]) -> bool:
        """旧接口,设置透传数据,旧接口有时候会丢失数据
           Deprecated

        Args
        ----
            joint (List[float]): 关节数据
            
        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("tt_set_current_servo_joint", {"targetPos":joint}, ret_flag = self.TT_ret_flag)


    def TT_add_joint(self, joint: List[float]) -> bool:
        """透传添加目标关节点到缓存

        Args
        ----
            joint (List[float]): 目标关节点
            
        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("tt_put_servo_joint_to_buf", {"targetPos":joint}, ret_flag = self.TT_ret_flag)


    def TT_add_pose(self, pose: List[float]) -> bool:
        """透传添加目标位姿点到缓存

        Args
        ----
            pose (List[float]): 目标位姿点
            
        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("tt_put_servo_joint_to_buf",{"targetPose":pose}, ret_flag = self.TT_ret_flag)


    def TT_clear_buff(self) -> bool:
        """清空透传缓存

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("tt_clear_servo_joint_buf",{"clear":0})


    @property
    def TT_state(self) -> int:
        """获取当前机器人是否处于透传状态

        Returns
        -------
            int: 0: 非透传状态 1: 透传状态 
        """
        return self.send_CMD("get_transparent_transmission_state")
