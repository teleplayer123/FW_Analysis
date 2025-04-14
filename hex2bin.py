import re
import os
import sys


def parse_hex_dump_long(filename):
    with open(filename, "r") as fh:
        for line in fh:
            if line == "":
                continue
            line = line.split("  ", maxsplit=1)[0]
            addr, data = line.split(" ", maxsplit=1)
            data = "".join(data.split(" "))
            print(data)
            break

if __name__ == "__main__":
    fname = sys.argv[1]
    parse_hex_dump_long(fname)