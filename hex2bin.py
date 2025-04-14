import sys


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

if __name__ == "__main__":
    fname = sys.argv[1]
    parse_hex_dump_long(fname)