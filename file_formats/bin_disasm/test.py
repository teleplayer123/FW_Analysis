from headers.mpy_hdr import MPY

fn = r"C:\binanalysis\disasm\adafruit_ducky.mpy"
m = MPY(fn)
print(m.mpy_hdr.magic)