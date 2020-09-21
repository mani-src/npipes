# npipes
Python based Named Pipes Wrapper for Windows

## Introduction
This module provides an easy wrapper for the windows named pipes using pywin32, which can be integrated with any of your projects dealing with the named pipes. This also includes an optional CRC32 validation for the data sent/received.  

## Usage
The module exposes 2 important APIs from the class IPC
```Python 
send_message
receive_message
``` 
These 2 APIs provide a high level wrapper around the methods in the Pipes class which are a direct interface to the win32file APIs
```Python
win32file.Writefile 
win32file.Readfile
```
Sample code for sending data from the pipe
```Python
from npipes.ipc import IPC
ipc = IPC()
ipc.send_message('Hello')
```
The above code, first creates a PIPE using ```win32pipe.CreateNamedPipe``` with a ```win32pipe.PIPE_WAIT``` and ```win32pipe.PIPE_ACCESS_DUPLEX``` flags set to wait for the client to connect and also open the PIPE in a duplex mode. And then sends the encoded data (encoding will be explained further below) to the client. 
The ```send_message``` API also provides an option to generate and encode the 32-bit CRC code for the data being sent out, which can be used at the other end to validate. To enable CRC validation the call from the above code must be modified to
```Python
ipc.send_message('Hello', crc=True)
```
Sample code for receiving data from the pipe
```Python
from npipes.ipc import IPC
ipc = IPC()
ipc.receive_message()
```
The above code again creates a PIPE in a Duplex mode with the Wait flag set. Please note that this module doesn't use the ```win32file.CreateFile``` API for the client to connect to the server end of the PIPE. It instead relies on the Duplex communication mode of  ```win32pipe.CreateNamedPipe```. The above API returns a data string and also can be accessed using the property method ```message```. Similar to the ```send_message``` API call, one can also validate the 32-bit CRC code by enabling it from the call
```Python
ipc.receive_message(crc = True)
```

### Encoding and Message Format

Detailed samples will be committed to the repo shortly.

