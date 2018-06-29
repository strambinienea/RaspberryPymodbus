# An easy guide for the implementation of pymodbus TCP Server and Client

#### Requirements
- Python 3+
- pymodbus()
- keyboard()
- logging()

*Some other library may be required by the one above, chek for dependecies.

#### Initialization
In first place you need to use the `pip` or `pip3` command to install all the libraries needed.

```bash
pip install --update pip
pip install pymodbus
pip install keyboard
pip install logging
```
##### Server
Open a new python file and start importing the necessary function
```python
import logging
import keyboard
from random import randint
from time import sleep
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer, ModbusBaseRequestHandler
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer, ModbusBinaryFramer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContextì
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
```
When you have imported all of these function we can start writing the code for the server, the firs line will be the line for the log, this will help troughout the project, understanding all the steps the server is doing this will also help you with some problem you may encounter during the realization of the Server.

```python
# Log

FORMAT = ('%(asctime)-15s %(threadName)-15s ' '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
```
After the log we will write the function to start the server
```python
def start_server(address="0.0.0.0", port=502):
	"""A function that start the server
	address: the address of the server
	port: the port of the server
	"""
```
Inside this function we will create and allocate the various block of registers, we will decide what type they are and what address they will have.
```python
block1 = ModbusSequentialDataBlock(0, [0]*10000)
floor1 = ModbusSlaveContext(hr=block1)

devices = {
0X01 : floor1		
}

context = ModbusServerContext(devices, single=False)
```
The block1 variable contains a `ModbusSequentialDataBlock` type of object, this is used by the next function, `ModbusSlaveContext()` to create a Slave Context, a object that contains the information of the register, how much they are, their type and address, in this case there are 10000 registers that start from the address 0 and they are all Holding Register type. We will the make a dictionary that contains all of our `ModbusSlaveContext` object, everyone with his own ID defined, in this case we only needed one.
Finally we have the context variable that contain a `ModbusServerContext` object, created by the homonym function, this uses the device dictionary we created before and create a Server Context, that is like a global Slave Context, with all the information of all the Slave Context like object in the server.
The Client will then use the ID found in the device dictionary to request to the slave to do something, like reading or writing on a register.
The next step is an optional aesthetic feature, so do as you like.
```python
# Identity

identity = ModbusDeviceIdentification()
identity.VendorName = 'Raspberry'
identity.ProductCode = 'RB'
identity.ProductName = 'Raspberry TCP Server'
identity.ModelName = 'Raspberry TCP Server'
```
The last step is to actually start the server, using the `StartTcpServer` function, this function require as parameters the context, the idendity(if you defined it) and a tuple containing the address and the port of the server.
Then you need to call the function that you have just created in order to start the server, you will to that by simply writing it inside an `if` that allow you to start it by just typing the name of the file in your shell.
```python
server = StartTcpServer(context, identity, (address, port))
if __name__ == "__main__":
    start_server()
```

