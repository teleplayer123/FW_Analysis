import struct
import ctypes as ct
from typing import NamedTuple


"""
-----------------------------------------------------
| S | Type | Byte Count | Address | Data | Checksum |
-----------------------------------------------------
An SREC format file consists of a series of ASCII text records. The records have the following structure from
left to right:

1. Record start - each record begins with an uppercase letter "S" character (ASCII
0x53) which stands for "Start-of-Record".

2. Record type - single numeric digit "0" to "9", defining the type of record.

3. Byte count - two hex digits, indicating the number of bytes (hex digit pairs) that
follow in the rest of the record (address + data + checksum). This field has a
minimum value of 3 for 16-bit address field plus 1 checksum byte, and a maximum
value of 255 (0xFF).

4. Address - four / six / eight hex digits as determined by the record type. The address
bytes are arranged in big-endian format.

5. Data - a sequence of 2n hex digits, for n bytes of the data. For S1/S2/S3 records, a
maximum of 32 bytes per record is typical since it will fit on an 80 character wide
terminal screen, though 16 bytes would be easier to visually decode each byte at a
specific address.

6. Checksum - two hex digits, the least significant byte of ones' complement of the
sum of the values represented by the two hex digit pairs for the byte count,
address and data fields. See example section for a detailed checksum example.
"""

hex_t = str

class SREC(NamedTuple):
    rec_start: str  #start record listeral 's'
    rec_type: int  #record type int 0-9
    byte_count: hex_t  #one hex byte value 0x03 - 0xff indicates number of bytes in rest of record
    addr: hex_t  #hex addr size specified hy rec_type in big endian
    data: hex_t  #sequence of bytes in hex; data size = byte_count - len(addr) - 1
    checksum: hex_t  #one byte in hex, the least significant byte of ones' complement of the
                     #sum of the values represented by the two hex digit pairs for the byte count, address and data fields.

class SREC_File:

    def __init__(self, data):
        self._data = data

