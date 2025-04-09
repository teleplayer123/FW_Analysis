import ctypes as ct
import struct
import mmap


class CPUID_Reg(ct.Structure):
    _fields_ = [
        ("eax", ct.c_uint32),
        ("ebx", ct.c_uint32),
        ("ecx", ct.c_uint32),
        ("edx", ct.c_uint32)
    ]


class CPUID:

    def __init__(self):
        pass
