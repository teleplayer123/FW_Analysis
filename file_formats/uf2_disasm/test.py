import sys
from headers.uf2_header import UF2


fn = sys.argv[1]
u = UF2(fn)

u.unpack_uf2_blocks()
print(repr(u))

with open("test.txt", "w") as fh:
    fh.write(repr(u))

