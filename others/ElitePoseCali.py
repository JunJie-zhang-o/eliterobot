'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 13:36:45
Description: python位姿的计算,欧拉角对应Elite_ec
'''

import numpy as np
import math
import transformations
from transformations.transformations import euler_from_matrix, inverse_matrix




def euler_2_matrix(euler_pose: list, unit_type: int=0):
    """欧拉角转齐次变换矩阵

    Args:
        euler_pose (list): 欧拉角位姿
        unit_type (int, optional): 0为弧度,1为角度. Defaults to 0.

    Returns:
        list: 齐次变换矩阵
    """
    # 角度转弧度
    if unit_type == 1:
        euler_pose[3] = math.radians(euler_pose[3])
        euler_pose[4] = math.radians(euler_pose[4])
        euler_pose[5] = math.radians(euler_pose[5])

    m = transformations.euler_matrix(euler_pose[3], euler_pose[4], euler_pose[5])
    m[0][3] = euler_pose[0]
    m[1][3] = euler_pose[1]
    m[2][3] = euler_pose[2]
    # print(m)
    return m


def mat_mul(mat1: list, mat2: list):
    """矩阵的乘

    Args:
        mat1 (list): 矩阵1
        mat2 (list): 矩阵2

    Returns:
        list: 相乘后的矩阵
    """
    return np.matmul(mat1, mat2)


def mat_inv(mat: list):
    """矩阵的逆

    Args:
        mat (list): 矩阵

    Returns:
        list: 求逆后的矩阵
    """
    return inverse_matrix(mat)


def matrix_2_euler(mat: list, unit_type: int=0):
    """齐次变换矩阵转欧拉角

    Args:
        mat (list): 齐次变换矩阵
        unit_type (int, optional): 0为弧度,1为角度. Defaults to 0.

    Returns:
        list: 欧拉角
    """
    x, y, z = mat[0][3], mat[1][3], mat[2][3]
    mat[0][3] = 0
    mat[1][3] = 0
    mat[2][3] = 0
    # 旋转矩阵到弧度的欧拉角
    rx, ry, rz = euler_from_matrix(mat)
    if unit_type == 1:
        rx = math.degrees(rx)
        ry = math.degrees(ry)
        rz = math.degrees(rz)
    return [x, y, z, rx, ry, rz]


def pose_inv(pose: list,unit_type: int=0):
    """位姿的逆

    Args:
        pose (list): 欧拉角
        unit_type (int, optional): 0为弧度,1为角度. Defaults to 0.

    Returns:
        list: 求逆后的欧拉角
    """
    mat = euler_2_matrix(pose,unit_type)
    return matrix_2_euler(mat_inv(mat),unit_type)


def pose_mul(pose1: list, pose2: list, unit_type: int = 0):
    """位姿的乘

    Args:
        pose1 (list): 位姿1
        pose2 (list): 位姿2
        unit_type (int, optional): 0为弧度,1为角度. Defaults to 0.

    Returns:
        list: 相乘后的位姿
    """
    mat1 = euler_2_matrix(pose1,unit_type)
    mat2 = euler_2_matrix(pose2,unit_type)
    mat = mat_mul(mat1, mat2)
    pose = matrix_2_euler(mat,unit_type)

    return pose

"""
    tool = [3.599,75.165,115.147,-178.238,-2.593,141.413]
    without_tool = [533.247,663.674,137.863,179.358,2.803,135.467]
    with_tool = [588.286,716.772,23.527,0.515,0.001,-5.959]
    p = pose_mul(pose_inv(without_tool),with_tool)          # 已知带工具和不带工具的位姿,求工具
    p = pose_mul(with_tool,pose_inv(tool))                  # 已知带工具的位姿和工具,求出当前法兰盘的位姿

    # world_2_user
    user_pose = pose_mul(pose_inv(user_frame),cart_pose)
    # user_2_world
    cart_pose = pose_mul(user_frame,user_pose)
    
    #求出v10相对V1的距离
    trsf = pose_mul(v1, pose_inv(v10))
"""
if __name__ == "__main__":
    a = [1,2,3,1,1,1]
    b = [1,2,3,1,1,1]
    print(pose_mul(a,b))
    print(pose_inv(a))
    pass


    

