'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-20 11:47:19
Description: 
'''

from typing import List,Optional
from ._baseec import BaseEC

class ECKinematics(BaseEC):
    """EC运动学类,提供了机器人本身的运动学相关接口
    """
# 运动学服务
    def get_inverse_kinematic(self, pose: List[float] ,ref_joint: Optional[List[float]] = None, unit_type: Optional[int] = None) -> List[float]:
        """运动学逆解

        Args
        ----
            pose (List[float]): 需要进行逆解的位姿
            ref_joint (List[float]): 参考关节角
            unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
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


    def get_forward_kinematic(self, joint: List[float], unit_type: Optional[int] = None) -> List[float]:
        """运动学正解

        Args
        ----
            joint (List[float]): 需要进行正解的关节角
            unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 正解后的位姿数据
        """
        if unit_type is not None:
            return self.send_CMD("positiveKinematic",{"targetPos":joint, "unit_type":unit_type})
        else:
            return self.send_CMD("positiveKinematic",{"targetPos":joint})


    def pose_mul(self, pose1: List[float], pose2: List[float], unit_type: Optional[int] = None) -> List[float]:
        """位姿相乘

        Args
        ----
            pose1 (List[float]): 位姿信息
            pose2 (List[float]): 位姿信息
            unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 位姿相乘后的结果
        """
        if unit_type is not None:
            return self.send_CMD("poseMul",{"pose1":pose1, "pose2":pose2, "unit_type":unit_type})
        else:
            return self.send_CMD("poseMul",{"pose1":pose1, "pose2":pose2})
        

    def pose_inv(self, pose: List[float], unit_type: Optional[int] = None) -> List[float]:
        """位姿求逆

        Args
        ----
            pose (List[float]): 要求逆的位姿
            unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 求逆后的结果
        """
        if unit_type is not None:
            return self.send_CMD("poseInv",{"pose":pose, "unit_type":unit_type})
        else:
            return self.send_CMD("poseInv",{"pose":pose})
        
        
    def convert_base_pose_to_user_pose(self, base_pose: List[float], user_num: int, unit_type: Optional[int] = None) -> List[float]:
        """基坐标系位姿转化为用户坐标系位姿

        Args
        ----
            cart_pose (List[float]): 基坐标系下的位姿数据
            user_num (int): 用户坐标系号
            unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 用户坐标系下的位姿信息
        """
        if unit_type is not None:
            return self.send_CMD("convertPoseFromCartToUser",{"TargetPose":base_pose, "userNo":user_num, "unit_type":unit_type})
        else:
            return self.send_CMD("convertPoseFromCartToUser",{"TargetPose":base_pose, "userNo":user_num})
            
        
    def convert_user_pose_to_base_pose(self, user_pose: List[float], user_num: int, unit_type: Optional[int] = None) -> List[float]:
        """用户坐标系转化为基坐标系

        Args
        ----
            user_pose (List[float]): 用户坐标系下的数据
            user_num (int): 用户坐标系号
            unit_type (int, optional): 输入和返回位姿的单位类型,0:角度, 1:弧度, 不填默认弧度. Defaults to None.

        Returns
        -------
            List[float]: 基坐标系下的位姿信息
            
        Versions:
        

        """
        if unit_type is not None:
            return self.send_CMD("convertPoseFromUserToCart",{"TargetPose":user_pose, "userNo":user_num, "unit_type":unit_type})
        else:
            return self.send_CMD("convertPoseFromUserToCart",{"TargetPose":user_pose, "userNo":user_num})
