import ctypes
import mmap


def get_base_addr():
    """Only works on linux"""
    buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)

    ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
    fpointer = ctypes.c_void_p.from_buffer(buf)

    f = ftype(ctypes.addressof(fpointer))

    buf.write( #need to get hex for opcodes
        b"\x64\x67\xa1\x30\x00\x00\x00",# mov eax, dword ptr fs:[30h]
        b"\x50",# push eax
        # mov eax, offset format
        # push eax
        # call printf
        # pop ebx
        # pop ebx
        # ---- Example---
        # b'\x8b\xc7'  # mov eax, edi
        # b'\x83\xc0\x01'  # add eax, 1
        # b'\xc3'  # ret
    )

    r = f(42)
    print(r)

    del fpointer
    buf.close()