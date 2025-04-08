import ctypes
import mmap
import struct


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
    buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
    ftype = ctypes.CFUNCTYPE(ctypes.c_uint32)
    fpointer = ctypes.c_void_p.from_buffer(buf)
    func = ftype(ctypes.addressof(fpointer))
    buf.write(hexcode)
    res = func()
    del fpointer
    buf.close()
    return res

def get_cpuid():
    # Define the assembly code as a byte buffer
    assembly_code = b'\x66\x0f\xa2\x00'  # CPUID instruction
    assembly_code += b'\x66\x83\xf0\x40'  # mov eax, ecx (store CPU ID in EAX)
    assembly_code += b'\x49\x89\xe4'  # mov rbp, rsp (set up stack frame)
    assembly_code += b'\xc3'  # ret (return from function)

    # Create a shared object (SO) file and load it into memory using mmap
    with open('cpuid.so', 'w+b') as f:
        f.write(b'\0' * 4098)  # allocate 4KB of memory for the SO file
        mm = mmap.mmap(f.fileno(), 4098, access=mmap.ACCESS_WRITE)

    # Convert the assembly code to machine code
    machine_code = bytes()
    # machine_code = mmap.mmap(-1, mmap.PAGESIZE, access=mmap.ACCESS_WRITE)
    for i in range(0, len(assembly_code), 2):
        byte = int.from_bytes(assembly_code[i:i+2], 'big')
        if byte == 0:
            break
        machine_code += struct.pack('<I', byte)

    # Load the machine code into a ctypes buffer
    code_buffer = (ctypes.c_ubyte * len(machine_code)).from_buffer(machine_code)

    # Create a ctypes function prototype for the assembly code
    lib = ctypes.CDLL('cpuid.so')
    lib._start.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
    lib._start.restype = None

    # Call the _start function with the machine code buffer as an argument
    lib._start(code_buffer)

    # Get the CPU ID information using mmap
    with open('cpuid.so', 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        cpu_id = bytes()
        for i in range(0, len(mm), 4):
            byte = int.from_bytes(mm[i:i+4], 'little')
            if byte == 0:
                break
            cpu_id += struct.pack('<I', byte)

    # Clean up
    mm.close()
    f.close()
    return cpu_id

def unpack_cpuid():
    cpuid_struct = get_cpuid()
    cpuid = cpuid_struct.unpack("<I")[0]
    print("CPUID: {}".format(hex(cpuid)))