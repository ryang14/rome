from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    rz: float = 0.0

@dataclass
class Pointj:
    j1: float = 0.0
    j2: float = 0.0
    j3: float = 0.0
    j4: float = 0.0
    j5: float = 0.0
    j6: float = 0.0

# Generic arm class implments a standard API
class Arm(metaclass=ABCMeta):
    def __init__(self,**kwargs):
        pass

    # Get the current position as a point
    def here(self) -> Point:
        return self._pointj_to_point(self._get_position())

    # Move to a point
    def move(self, point: Point):
        self._move_to(self._point_to_pointj(point))

    # Get the current joint position
    def herej(self) -> Pointj:
        return self._get_position()
    
    # Move to a joint position
    def movej(self, pointj: Pointj):
        self._move_to(pointj)
    
    # Classes to override

    # Move to a joint location
    @abstractmethod
    def _move_to(self, pointj: Pointj):
        pass

    # Get current position
    @abstractmethod
    def _get_position(self) -> Pointj:
        pass
    
    # Convert a point in the world frame to a joint position
    @abstractmethod
    def _pointj_to_point(self, pointj: Pointj) -> Point:
        pass

    # Convert a joint position to a point in the world frame
    @abstractmethod
    def _point_to_pointj(self, point: Point) -> Pointj:
        pass