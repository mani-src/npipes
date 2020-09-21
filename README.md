# npipes
Python based Named Pipes Wrapper for Windows

## Introduction
This module provides an easy wrapper for the windows named pipes using ```pywin32```, which can be integrated with any of your projects dealing with the named pipes. This also includes an optional CRC32 validation for the data sent/received.  

## Usage
The module exposes 2 important APIs from the class IPC
```Python 
send_message
receive_message
``` 
These 2 APIs provide a high level wrapper around the methods in the ```Pipes``` class which are a direct interface to the ```win32file``` APIs
```Python
win32file.Writefile 
win32file.Readfile
```
Sample code for sending data
```Python
from npipes.ipc import IPC
ipc = IPC()
ipc.send_message('Hello')
```
The above code, first creates a ```PIPE``` using ```win32pipe.CreateNamedPipe``` with a ```win32pipe.PIPE_WAIT``` and ```win32pipe.PIPE_ACCESS_DUPLEX``` flags set to wait for the client to connect and also open the ```PIPE``` in a duplex mode. And then sends the encoded data (encoding will be explained further below) to the client. 
The ```send_message``` API also provides an option to generate and encode the 32-bit CRC code for the data being sent out, which can be used at the other end to validate. To enable CRC validation the call from the above code must be modified to
```Python
ipc.send_message('Hello', crc=True)
```
Sample code for receiving data
```Python
from npipes.ipc import IPC
ipc = IPC()
ipc.receive_message()
```
The above code again creates a ```PIPE``` in a Duplex mode with the Wait flag set. Please note that this module doesn't use the ```win32file.CreateFile``` API for the client to connect to the server end of the ```PIPE```. It instead relies on the Duplex communication mode of  ```win32pipe.CreateNamedPipe```. The above API returns a data string and the data can also be accessed using the property method ```message```. Similar to the ```send_message``` API call, one can also validate the 32-bit CRC code by enabling it from the below call
```Python
ipc.receive_message(crc = True)
```

## Message Format and Encoding
Packing and Encoding the data is done in the ```Message``` class.
The data supplied to the API ```send_message``` is first packed into the following fields

| Message Length | Data Length |      Data/Payload       |  CRC-32  |
|----------------|-------------|-------------------------|----------|

```Message Length``` is the size of the whole packet and is ```4 bytes``` long.  
```Data Length``` is the size of the data or payload and is also ```4 bytes``` long.  
```Data/Payload``` is the data supplied to the ```send_message``` API call.  
```CRC-32``` is the 32-bit CRC code for the data, and is ```4 bytes``` long.  

The message is sent out encoded in binary and the data field is encoded in ascii by default, but this is configurable, by passing the relevant encoding format to the constructor. The message is forced to be in little endian system by default, but this is configurable by the value set in constructor.

