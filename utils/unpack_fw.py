import ctypes as ct
import os
import sys
import struct

filename = str(sys.argv[1])
save_dir = os.path.join(os.getcwd(), "UnpackedData")
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

class Chunk:

    def __init__(self, offset, size, desc):
        self.offset = offset
        self.size = size
        self.desc = desc

    def __str__(self):
        return \
        f"""
        Offset: {self.offset}
        Size: {self.size}
        Description: {self.desc}
        """
    
class Unpacker:

    def __init__(self, data):
        self._data = data

    def check_magic(self):
        """TODO: impllement dictionary with know magic numbers and test for magic number based on file extension"""
        pass

def unpack_chunks(chunks):
    file = open(filename, "rb")
    try:
        for chunk in chunks:
            file.seek(chunk.offset)
            with open(os.path.join(save_dir, f"{chunk.desc}.bin"), "wb") as fh:
                fh.write(file.read(chunk.size))
    finally:
        file.close()

chunks = [Chunk(540, int(707-540), "ucode0"),
          Chunk(707, int(807-707), "esp0"),
          Chunk(807, int(872-807), "esp1"),
          Chunk(1777, int(37517-1777), "Copyright_String"),
          Chunk(37517, int(165488-37517), "x86_64_uCode")]

unpack_chunks(chunks)