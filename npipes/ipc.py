from array import array
from npipes.consts import *
from npipes.pipes import Pipes
from npipes.message import Message


class IPC(Pipes):
    def __init__(self, pipe_name=IPC_FIFO_NAME):
        super().__init__()
        self.__msg_parser = Message()
        self.__msg = ''
        self.pipe = pipe_name

    @property
    def message(self):
        return self.__msg

    @staticmethod
    def __calc_crc(msg, polynomial=0xEDB88320):
        # Ref: https://stackoverflow.com/questions/41564890/crc32-calculation-in-python-without-using-libraries
        table = array('L')
        for byte in range(256):
            crc = 0
            for bit in range(8):
                if (byte ^ crc) & 1:
                    crc = (crc >> 1) ^ polynomial
                else:
                    crc >>= 1
                byte >>= 1
            table.append(crc)
        value = 0xffffffff
        for ch in msg:
            value = table[(ord(ch) ^ value) & 0xff] ^ (value >> 8)
        return (-1 - value) & 0xffffffff

    def send_message(self, data: str, crc: bool = False) -> bool:
        try:
            crc32 = 0
            if crc:
                crc32 = IPC.__calc_crc(data)
            self.__msg_parser.data = data
            self.__msg_parser.crc32 = crc32
            self.__msg_parser.encapsulate_msg()
            self.__msg = self.__msg_parser.message
            self.write(self.__msg)
            return True
        except Exception as err:
            print(err)
            return False

    def receive_message(self, crc: bool = False) -> str:
        try:
            msg = self.read()
            self.__msg_parser.read_msg(msg)
            data = self.__msg_parser.data
            recv_crc32 = self.__msg_parser.crc32
            crc32 = IPC.__calc_crc(data)
            if crc:
                if recv_crc32 == crc32:
                    self.__msg = data
                    return data
                else:
                    print('Failed to validate the CRC')
                    print(f'Received CRC: {recv_crc32}')
                    print(f'Calculated CRC: {crc32}')
                    self.__msg = ''
                    return ''
            else:
                self.__msg = data
                return data
        except Exception as err:
            print(err)
            return ''



