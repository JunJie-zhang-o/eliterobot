'''
Author: Elite_zhangjunjie
CreateDate: 
LastEditors: Elite_zhangjunjie
LastEditTime: 2022-05-10 13:35:46
Description: 基于list实现的Pose类,主要实现打印和调试中角度和弧度的显示,以及求逆和乘
'''
import math
from typing import Any, SupportsIndex, overload

from others.ElitePoseCali import pose_inv, pose_mul


class Pose(list):

    MAX_BITS = 6
    
    __solts__ = ("x", "y", "z", "rx", "ry", "rz")
    
    
    @overload
    def __init__(self,_list: list, is_rad:bool=True): ...


    @overload
    def __init__(self, _x: float, _y: float, _z: float, _rx: float, _ry: float, _rz: float, is_rad:bool=True): ...
    
    
    def __init__(self, *args, **kwargs):
        is_rad = kwargs["is_rad"] if "is_rad" in kwargs else True
        if type(args[0]) == list:
            self.__refresh(args[0], is_rad)
        elif len(args) == 6:
            self.__refresh(args[:6], is_rad)
        super().__init__([self.x, self.y ,self.z, self.rx, self.ry, self.rz])
 
 
    def __refresh(self, _pose: list, is_rad: bool=True):
        self.x,  self.y,  self.z = _pose[0], _pose[1], _pose[2]
        if is_rad:
            self.rx, self.ry, self.rz = _pose[3], _pose[4], _pose[5]
        else:
            self.rx, self.ry, self.rz = math.radians(_pose[3]), math.radians(_pose[4]), math.radians(_pose[5])


    def __to_deg(self):
        return self.__round([self.x, self.y, self.z, math.degrees(self.rx), math.degrees(self.ry), math.degrees(self.rz)])
    
    
    def __round(self, pose: list=None):
        if pose is not None:
            return [round(i, self.MAX_BITS) for i in pose]
        else:
            return [round(i, self.MAX_BITS) for i in [self.x, self.y, self.z, self.rx, self.ry, self.rz]]
   

    def __str__(self) -> str:
        return f"Pose:{self.__to_deg()} in deg"


    def __repr__(self) -> str:
        return f"Pose:{self.__round()} in rad"


    def __mul__(self, __n: SupportsIndex) -> list:
        return Pose(pose_mul(self, __n))


    @property
    def inv(self) -> list:
        return Pose(pose_inv(self))


if __name__ == "__main__":
    x = Pose([30, 40, 50, 90.030030303, 180.030030303, 30.030030303], is_rad=False)
    y = Pose(1,2,3,4,5,6)

    a = Pose([1,2,3,1,1,1])
    b = Pose([1,2,3,1,1,1])
    c = a* b
    print(a.inv)
    print(a * b)
    print(x.x)
    print(x)
    print(x[-1])
