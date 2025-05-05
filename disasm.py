from file_formats.hex_disasm.headers.srec_file import SREC_File
import sys

srec_file = sys.argv[1]
sr = SREC_File(srec_file)
