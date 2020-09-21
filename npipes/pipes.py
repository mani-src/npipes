import os
import time
import select
import win32pipe
import win32file
import pywintypes
# from win32security import CreateWellKnownSid, ACL, WinNetworkSid
from win32security import *

from npipes.consts import *
from npipes.message import Message


class Pipes(object):
    def __init__(self):
        self.__fifo = None
        self.__msg = None
        self.__pipe = IPC_FIFO_NAME

    @property
    def fifo(self):
        return self.__fifo

    @property
    def pipe(self):
        return self.__pipe

    @pipe.setter
    def pipe(self, pipe_name):
        self.__pipe = pipe_name

    def open(self, mode='read', pipe_wait=True):
        wait = win32pipe.PIPE_WAIT
        if pipe_wait:
            wait = win32pipe.PIPE_WAIT
        else:
            wait = win32pipe.PIPE_NOWAIT
        create_file = False
        try:
            self.__fifo = win32pipe.CreateNamedPipe(rf'\\.\pipe\{self.__pipe}', win32pipe.PIPE_ACCESS_DUPLEX,
                                                    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE
                                                    | wait, 1, 65536, 65536, 0, None)
            print('Waiting for the client to connect')
            win32pipe.ConnectNamedPipe(self.__fifo, None)
            print('Client connected')
        except pywintypes.error as err:
            if mode == 'read':
                if err.args[0] == 231:
                    create_file = True
                else:
                    raise
            else:
                raise
        if mode == 'read' and create_file:
            self.__fifo = win32file.CreateFile(rf'\\.\pipe\{self.__pipe}',
                                               win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None,
                                               win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
            result = win32pipe.SetNamedPipeHandleState(self.__fifo, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if result == 0:
                raise Exception('Could not connect to any PIPE')
        return True

    def close(self):
        if self.__fifo:
            win32file.CloseHandle(self.__fifo)
            self.__fifo = None

    def write(self, msg):
        try:
            if not self.__fifo:
                self.open(mode='write')
            print(f'Sending message {msg} to the client')
            win32file.WriteFile(self.__fifo, msg)
            print(f'Message sent successfully')
        except Exception as exp:
            print(exp)
        finally:
            self.close()

    def read(self):
        try:
            if not self.__fifo:
                self.open()
            print(f'Reading message from the remote application')
            resp = win32file.ReadFile(self.__fifo, 65536)
            print(f'Message received: {resp}')
            return resp[1]
        except Exception as exp:
            print(exp)
        except pywintypes.error as err:
            if err.args[0] == 2:
                print('No PIPE available. Waiting for the PIPE to be created')
                time.sleep(1)
            elif err.args[0] == 109:
                print('Broken PIPE, exiting now')
            elif err.args[0] == 231:
                print('PIPE busy, check if the PIPE was opened successfully on the other end')
            print(err)
            return ''
        finally:
            self.close()

