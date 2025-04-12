import ctypes as ct
import struct
import mmap
import os


class CPUID_Struct(ct.Structure):
    _fields_ = [
        ("eax", ct.c_uint32),
        ("ebx", ct.c_uint32),
        ("ecx", ct.c_uint32),
        ("edx", ct.c_uint32)
    ]


class CPUID:

    def __init__(self, hexcode):
        size = len(hexcode)
        self.mm = mmap.mmap(-1, size, flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS, prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)
        func_type = ct.CFUNCTYPE(None, ct.POINTER(CPUID_Struct), ct.c_uint32, ct.c_uint32)
        self.addr = ct.addressof(ct.c_int.from_buffer(self.mm))
        self.func_type = func_type(self.addr)