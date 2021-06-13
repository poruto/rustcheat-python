from ctypes import *

class Vector2(Structure):
    _fields_ = [('x', c_float), ("y", c_float)]

class Vector3(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]
