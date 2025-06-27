import serial
import sys
import os


class BPReadFlash:
    def __init__(self, port: str, baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port, baudrate, timeout=1)
        self._connect()

    def _connect(self):
        if not self.serial.is_open:
            self.serial.open()
        if not self.serial.is_open:
            print(f"Failed to open serial port {self.port}")
            sys.exit(1)
        res = self.serial.read_all()
        res = res.decode('utf-8', errors='ignore')
        print(res)
        # if res.endswith("(Y/n)> "):
        if res == "VT100 compatible color mode? (Y/n)> ":
            self.serial.write(b"n\r\n")
            res = self.serial.read_all()
            print(res.decode('utf-8', errors='ignore'))

    def interactive_mode(self):
        print("Entering interactive mode. Type 'exit' to quit.")
        while True:
            cmd = input("> ")
            if cmd.lower() == 'exit':
                break
            elif cmd.lower() == 'read all':
                self.read_flash_to_file()
            self.serial.write((cmd + "\r\n").encode())
            response = self.serial.read_all()
            print(response.decode('utf-8', errors='ignore'))
        print("Exiting interactive mode.")

    def send_cmd(self, cmd) -> bytes:
        self.serial.write(cmd.encode())
        res = self.serial.read_until(b"\r\n")
        return res
    
    def read_flash(self, read_cmd: int=0x03, addr: int = 0x00, flash_size: int = 16777216) -> list:
        data = []
        length = flash_size // 256
        for i in range(length):
            cmd = f"[{read_cmd} {int(addr, 16)} r:256]\r\n"
            self.serial.write(cmd.encode())
            res = self.serial.read(256)
            data.append(res)
            addr += 256
        return data
        
    def read_flash_to_file(self, data, filename: str="flash_dump.bin"):
        filename = os.path.join(os.getcwd(), filename)
        with open(filename, 'wb') as fh:
            for chunk in data:
                fh.write(chunk)
        print(f"Flash data written to {filename}")

    def close(self):
        self.serial.close()

    