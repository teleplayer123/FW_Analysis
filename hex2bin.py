import sys
import re


def parse_hex_dump_long(filename):
    data_list = []
    outfile = filename.replace(".log", ".bin")
    with open(filename, "r") as fh:
        for line in fh:
            if line == "":
                continue
            line = line.split("  ", maxsplit=1)[0]
            addr, data = line.split(" ", maxsplit=1)
            data = "".join(data.split(" "))
            line_list = []
            for i in range(0, len(data), 2):
                b = "".join([data[i], data[i+1]])
                line_list.append(b)
            data_list.append(bytes.fromhex("".join(reversed(line_list))))
    with open(outfile, "w+b") as fh:
        for data_bytes in data_list:
            fh.write(data_bytes)

def parse_uboot_dump(filename):
    outfile = filename.replace(".log", ".bin")
    new_fh = open(outfile, "w+b")
    with open(filename, "r") as fh:
        for line in fh.readlines():
            line = line.split("  ", maxsplit=1)[0]
            line = line.split(":", maxsplit=1)
            if len(line) < 2:
                continue
            line = line[1].replace(" ", "")[:32]
            print(line)
            data = bytes.fromhex(line)
            new_fh.write(data)
    new_fh.close()


def main():
    fname = sys.argv[1]
    parse_uboot_dump(fname)

if __name__ == "__main__":
    main()