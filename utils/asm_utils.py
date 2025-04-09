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

def cpuid_info(leaf=0):
        """Executes the CPUID instruction and returns the result."""
        eax, ebx, ecx, edx = 0, 0, 0, 0  # Initialize registers
        # Define the CPUID function signature
        cpuid_func = ctypes.windll.kernel32.VirtualAlloc(0, 12, 0x3000, 0x40)
        # Write assembly code to memory
        ctypes.memset(cpuid_func, 0x55, 1)  # push ebp
        ctypes.memset(cpuid_func + 1, 0x8b, 1)  # mov ebp, esp
        ctypes.memset(cpuid_func + 2, 0x51, 1)  # push ecx
        ctypes.memset(cpuid_func + 3, 0xb8, 1)  # mov eax, leaf
        ctypes.memmove(cpuid_func + 4, ctypes.byref(ctypes.c_uint32(leaf)), 4)
        ctypes.memset(cpuid_func + 8, 0x0f, 1)  # cpuid
        ctypes.memset(cpuid_func + 9, 0xa2, 1)
        ctypes.memset(cpuid_func + 10, 0x59, 1)  # pop ecx
        ctypes.memset(cpuid_func + 11, 0xc3, 1)  # ret
        # Cast the memory address to a function pointer
        func = ctypes.cast(cpuid_func, ctypes.CFUNCTYPE(None))
        # Execute the assembly code
        func()
        # Retrieve the register values
        eax = ctypes.c_uint32.from_address(cpuid_func + 4).value
        ebx = ctypes.c_uint32.from_address(cpuid_func + 8).value
        ecx = ctypes.c_uint30.from_address(cpuid_func + 12).value
        edx = ctypes.c_uint30.from_address(cpuid_func + 16).value
        # Free the allocated memory
        ctypes.windll.kernel32.VirtualFree(cpuid_func, 12, 0x8000)

        return eax, ebx, ecx, edx

def get_cpuid_info():
    # Example usage: Get CPU vendor string (leaf 0)
    eax, ebx, ecx, edx = cpuid_info()
    vendor_id = "".join([
        chr((ebx >> (i * 8)) & 0xFF) for i in range(4)
    ]) + "".join([
        chr((edx >> (i * 8)) & 0xFF) for i in range(4)
    ]) + "".join([
        chr((ecx >> (i * 8)) & 0xFF) for i in range(4)
    ])
    print(f"CPU Vendor: {vendor_id}")

    # Example usage: Get CPU features (leaf 1)
    eax, ebx, ecx, edx = cpuid_info(1)
    print(f"Version Information (EAX): {eax:08x}")
    print(f"Feature Flags (EDX): {edx:08x}")
    print(f"Feature Flags (ECX): {ecx:08x}")
