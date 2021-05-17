# Type
"""Primitive指geometry script language支持的关键字和原始类型

"""
import abc
import deepxde.geometry as dg

class _Primitive(object):
    def __init__(self):
        super().__init__()

class _GeoObj1D():
    def __init__(self):
        super().__init__()

class _GeoObj2D(_Primitive):
    pass

class _GeoObj3D(_Primitive):
    pass


class _Geometry:
    def __init__(self, xde_geom = None):
        self.idstr = type(self).__name__
        self.xde_geom = xde_geom
        # self.js_geom = js_geom
        if xde_geom is None:
            self._build_xde_geom()
            # self._build_js_geom()

    @abc.abstractmethod
    def _build_js_geom(self):
        raise NotImplementedError("{}._build_js_geom not implemented".format(self.idstr))

    # @abc.abstractmethod
    # def _build_xde_geom(self):
    #     raise NotImplementedError("{}._build_xde_geom not implemented".format(self.idstr))

    def __and__(self, other):
        return _Geometry(self.xde_geom & other.xde_geom)
    
    def __or__(self, other):
        return _Geometry(self.xde_geom | other.xde_geom)

    def __sub__(self, other):
        return _Geometry(self.xde_geom - other.xde_geom)

# 1D
class Interval(_Geometry): 
    def __init__(self, l, r):
        self.l, self.r = l, r
        super(Interval, self).__init__()

    def _build_xde_geom(self):
        self.xde_geom = dg.Interval(self.l, self.r)


# 2D
class Rectangle(_Geometry): 
    def __init__(self, xmin, xmax):
        self.xmin = xmin
        self.xmax = xmax
        super(Rectangle, self).__init__()

    def _build_xde_geom(self):
        print(dg.__dir__())
        self.xde_geom = dg.Rectangle(self.xmin, self.xmax)

    def _build_js_geom(self):
        self.js_geom = None


class Disk(_Geometry): 
    def __init__(self, center, radius):
        self.center, self.radius = center, radius
        super(Disk, self).__init__()

    def _build_xde_geom(self):
        self.xde_geom = dg.Disk(self.center, self.radius)


class Polygon(_Geometry):
    def __init__(self):
        super(Polygon, self).__init__()


class Triangle(_Geometry): 
    def __init__(self, p1, p2, p3):
        self.p1, self.p2, self.p3 = p1, p2, p3
        super(Triangle, self).__init__()

    def _build_xde_geom(self):
        self.xde_geom = dg.Triangle(self.p1, self.p2, self.p3)


# bool
def diff(geom1, geom2):
    return geom1 - geom2

def union(geom1, geom2):
    return geom1 | geom2

def inter(geom1, geom2):
    return geom1 & geom2


# 3D
# class Cube: pass
# class Sphere: pass

# tranformation
# def scale(): pass
# def mirror(): pass
# def rotate():pass
# def move():pass
# def repeat():pass


