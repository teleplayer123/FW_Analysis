import ctypes
import mmap
import subprocess
import os


def get_base_addr():
    """Only works on linux"""
    buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)

    ftype = ctypes.CFUNCTYPE(ctypes.c_uint32)
    fpointer = ctypes.c_void_p.from_buffer(buf)

    f = ftype(ctypes.addressof(fpointer))

    buf.write( #need to get hex for opcodes
        b"\x64\x67\xa1\x30\x00\x00\x00" #mov eax, dword ptr fs:[30h]
        b"\xc3" #ret
    )

    r = f()
    print(r)

    del fpointer
    buf.close()

def encode_asm(hexcode):
    buf = mmap.mmap(-1, len(hexcode), flags=mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
    ftype = ctypes.CFUNCTYPE(ctypes.c_uint32)
    fpointer = ctypes.c_void_p.from_buffer(buf)
    func = ftype(ctypes.addressof(fpointer))
    buf.write(hexcode)
    res = func()
    buf.close()
    return res

def get_cpuid():
    # Define the assembly code as a byte buffer
    assembly_code = b'\x66\x0f\xa2\x00'  # CPUID instruction
    assembly_code += b'\x66\x83\xf0\x40'  # mov eax, ecx (store CPU ID in EAX)
    assembly_code += b'\x49\x89\xe4'  # mov rbp, rsp (set up stack frame)
    assembly_code += b'\xc3'  # ret (return from function)
    res = encode_asm(assembly_code)
    return res

def compile_asm(filename):
    name = filename.split(".")[0]
    cmd = f"nasm -f elf64 -o {name}.o {filename}"
    print("Compiling...")
    res = subprocess.run(cmd, shell=True, encoding="utf-8")
    print(res)
    cmd = f"ld {name}.o -o {name}"
    res = subprocess.run(cmd, shell=True, encoding="utf-8")
    print(res)
    return os.path.join(os.getcwd(), name)
    