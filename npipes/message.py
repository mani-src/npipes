import struct


class Message(object):
    def __init__(self, data='', crc32=0, encoding='ascii', endian='big'):
        self.__data = data
        self.__crc32 = crc32
        self.__encoding = encoding
        self.__endian = endian
        self.__message = None

    @property
    def message(self):
        return self.__message

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_data):
        self.__data = new_data

    @property
    def crc32(self):
        return self.__crc32

    @crc32.setter
    def crc32(self, crc):
        self.__crc32 = crc

    def __get_endian(self):
        if self.__endian.upper() == 'BIG':
            return '>'
        elif self.__endian.upper() == 'LITTLE':
            return '<'
        elif self.__endian.upper() == 'NATIVE':
            return '='
        elif self.__endian.upper() == 'NETWORK':
            return '!'
        else:
            return ''

    def encode(self, size: int) -> bytes:
        return struct.pack(self.__get_endian() + 'I', size)

    def decode(self, size_bytes: bytes) -> int:
        return struct.unpack(self.__get_endian() + 'I', size_bytes)[0]

    def encapsulate_msg(self):
        data = self.__data.encode(self.__encoding)
        data_length = self.encode(len(data))
        crc32 = self.encode(self.__crc32)
        message_length = self.encode(len(data) + len(data_length) + len(crc32))
        message = message_length + data_length + data + crc32
        self.__message = message

    def read_msg(self, msg_bytes: bytes):
        msg_len = self.decode(msg_bytes[:4])
        data_len = self.decode(msg_bytes[4:8])
        data = (msg_bytes[8:data_len+8]).decode(self.__encoding)
        crc32 = self.decode(msg_bytes[(data_len+8):])
        self.__crc32 = crc32
        self.__data = data
