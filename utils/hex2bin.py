import sys


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
            data = bytes.fromhex(line)
            new_fh.write(data)
    new_fh.close()


def main():
    fname = sys.argv[1]
    parse_uboot_dump(fname)

if __name__ == "__main__":
    main()