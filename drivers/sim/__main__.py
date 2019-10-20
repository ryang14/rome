from arm import Arm, Point, Pointj

class Sim(Arm):
    def __init__(self,**kwargs):
        super(Sim,self).__init__(**kwargs)
        self._joints = Pointj()

    def _move_to(self, pointj):
        self._joints = pointj
    
    def _get_position(self):
        return self._joints
    
    def _pointj_to_point(self, pointj: Pointj) -> Point:
        return Point(x=pointj.j1, y=pointj.j2, z=pointj.j3, rx=pointj.j4, ry=pointj.j5, rz=pointj.j6)
    
    def _point_to_pointj(self, point: Point) -> Pointj:
        return Pointj(j1=point.x, j2=point.y, j3=point.z, j4=point.rx, j5=point.ry, j6=point.rz)

arm = Sim()