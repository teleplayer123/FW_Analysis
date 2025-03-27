from headers.elf32_header import ELF32

fn = r"C:\pico_asm\build\pico_usb\pico_usb.elf"
e = ELF32(fn)
print(e.elf_hdr.e_ident)