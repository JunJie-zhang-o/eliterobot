'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-22 14:24:45
Description: 
'''

from ._baseec import BaseEC


class ECMoveML(BaseEC):
    """ECMoveML类,实现时间戳服务(movml)相关的接口
    """
    # moveml运动
    def ml_init(self, length: int, point_type: int, ref_joint: list, ref_frame: list, ret_flag: int) -> bool:
        """初始化带时间戳轨迹文件运动
           #!传输的第一个点位的时间戳必须为0
           
        Args
        ----
            length (int): 点位数量
            point_type (int): 点位类型,0: 关节,1: 位姿
            ref_joint (list): 参考关节角,如果点位类型为位姿,参考点为第一个点的逆解参考点
            ref_frame (list): 用户坐标系,如果为基座坐标系全为0
            ret_flag (int): 添加点位指令是否有返回值,0无,1有

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        self.ml_ret_flag = ret_flag
        return self.send_CMD("start_push_pos",{"path_lenth":length, "pos_type":point_type, "ref_joint_pos":ref_joint, "ref_frame":ref_frame, "ret_flag":ret_flag})
    
    
    def ml_push(self, time_stamp: float, pos: list) -> bool:
        """添加带时间戳文件运动点位

        Args
        ----
            time_stamp (float): 时间戳,大于等于0,且递增单位: s
            pos (list): 点位数据

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("push_pos", {"timestamp":time_stamp, "pos":pos}, ret_flag=self.ml_ret_flag)

    
    def ml_end_push(self) -> bool:
        """停止添加时间戳点位,并返回push结果,push结果正确返回True

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("stop_push_pos")
    
    
    def ml_check_push_result(self) -> BaseEC.MlPushResult:
        """检查push结果

        Returns
        -------
            MlPushResult: 0:push点位和时间戳正确,-1:点位长度不符,-2:点位格式错误,-3:时间戳不规范
        """
        return self.MlPushResult(self.send_CMD("check_trajectory"))
    
    
    def ml_flush(self) -> bool:
        """清空缓存

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("flush_trajectory")
     
    
    def ml_run(self, speed_percent: float=0.1) -> bool:
        """开始运行带时间戳的轨迹文件

        Args
        ----
            speed_percent (float, optional): 轨迹速度百分比,即以原始速度乘百分比的速度运动.单位 %, 范围>=0.1. Defaults to 0.1.

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("start_trajectory",{"speed_percent":speed_percent})
    
    
    def ml_pause(self) -> bool:
        """暂停运行带时间戳的轨迹文件

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("pause_trajectory")
    
    
    def ml_stop(self) -> bool:
        """停止运行带时间戳的轨迹运动

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("stop_trajectory")
        
        
    def ml_resume(self) -> bool:
        """恢复运行带时间戳的轨迹文件

        Returns
        -------
            bool: True操作成功,False操作失败
        """
        return self.send_CMD("resume_trajectory")