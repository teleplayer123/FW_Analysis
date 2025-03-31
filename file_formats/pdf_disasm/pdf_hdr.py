import ctypes as ct
import struct

from file_sigs import MagicValues


class PDFHeader:
    """
    - Boolean: true, false
    - Strings contain 8-bit chars between brackets:
        ASCII: (...)
        Hex: <...>
    - Names followed by forward slash /
    - Arrays: [...]
    - Dictionaries: <<...>>
    - Streams: optionally compressed binary data preceeded by dictionary between 'stream' and 'endstream' keywords
    - Comments: preceeded by '%'
    """
    MAGIC_VAL = MagicValues.PDF
    EOF_VAL = "%%EOF"

    def __init__(self, data):
        self.data = data
