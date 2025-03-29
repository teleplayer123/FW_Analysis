import ctypes as ct
import struct
from typing import NamedTuple


class DeviceDescriptor(ct.Structure):
    _fields_ = [
        ("b_length", ct.c_byte),
        ("b_descriptor_type", ct.c_byte),
        ("bcd_usb", ct.c_ushort),
        ("b_device_class", ct.c_byte),
        ("b_device_sub_class", ct.c_byte),
        ("b_device_protocol", ct.c_byte),
        ("b_max_packet_size", ct.c_byte),
        ("id_vendor", ct.c_ushort),
        ("id_product", ct.c_ushort),
        ("bcd_device", ct.c_ushort),
        ("")
    ]
