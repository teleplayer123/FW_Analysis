import ctypes as ct
import re
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

    BOOL_REGX = re.compile(r"\b*(true|false)\b*")
    STR_ASCII_REGX = re.compile(r"\([\w\d\s]+\)")
    STR_HEX_REGX = re.compile(r"<[0-9A-Fa-f]+>")
    NAME_REGX = re.compile(r"/[a-zA-Z0-9#]+")
    ARRAY_REGX = re.compile(r"\[[^\]]+\]")
    DICT_REGX = re.compile(r"<<[^\>]+>>")
    STREAM_REGX = re.compile(r"stream")
    ENDSTREAM_REGX = re.compile(r"endstream")
    COMMENT_REGX = re.compile(r"%[^\n]*")

    def __init__(self, data):
        self.data = data
        
