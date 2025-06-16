import ctypes as ct
import struct


class SectionHeaderBlock(ct.Structure):
    _fields_ = [
        ("block_type", ct.c_uint32),
        ("block_total_length", ct.c_uint32),
        ("byte_order_magic", ct.c_uint32),
        ("major_version", ct.c_uint16),
        ("minor_version", ct.c_uint16),
        ("section_length", ct.c_int64)
    ]

class TypeLength(ct.Structure):
    _fields_ = [
        ("block_type", ct.c_uint32),
        ("block_total_length", ct.c_uint32)
    ]

