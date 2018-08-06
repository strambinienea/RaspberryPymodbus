# An easy guide for the implementation of pymodbus TCP Server and Client

Before you start read this guide if you don't know the basic of the ModbusTCP protocol go and read them, they are exential to understand all of what is explained in the guide.

#### Requirements
- Python 3+
- pymodbus[(link)](https://github.com/riptideio/pymodbus "Pymodbus repository on Github")
- keyboard
- logging

*Some other library may be required by the one above, chek for dependecies.

#### Initialization
In first place you need to use the `pip` or `pip3` command to install all the libraries needed.

```bash
pip install --update pip
pip install pymodbus
pip install keyboard
pip install logging
```

#### Server
Open a new python file and start importing the necessary function and libraies.
A brief explanation:
- logging: Is used to make a log and help with the debug
- keyboard: Is used to receive input from the keyboard
- randint: Fuction that output a random integer
- sleep: It's a delay, mesured in seconds
- ModbusDeviceIdentification: Used for the identity of the Server(better explained later)
- StartTcpServer: Used to start the Server, a function contained in the Modbus library
- ModbusSequentialDataBock: Function that extablish a block made by contiguous registers
- ModbusSlaveContext and ModbusServerContext: Create a context-type object, better explained later
```python
import logging
import keyboard
from random import randint
from time import sleep
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
```
When you have imported all of these function we can start writing the code for the server, the first line will be the one for the log, this will help troughout the project understanding all the steps the server is doing, it will also help you with some problem you may encounter during the realization of the Server.

```python
# Log

FORMAT = ('%(asctime)-15s %(threadName)-15s ' '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
```
After the log we will write the function to start the server, this is called everytime you want to start the server.
```python
def start_server(address="0.0.0.0", port=502):
	"""A function that start the server
	address: the address of the server
	port: the port of the server
	"""
```
Inside this function we will create and allocate the various blocks of registers.
```python
block1 = ModbusSequentialDataBlock(0, [0]*10000)
floor1 = ModbusSlaveContext(hr=block1)

devices = {
0X01 : floor1		
}

context = ModbusServerContext(devices, single=False)
```
The `block1`  variable contains a `ModbusSequentialDataBlock` type of object, a block made of contiguous registers, this is used by the next function, `ModbusSlaveContext()` to create a Slave Context, a object that contains the information of the register, how much they are, their type and address, in this case there are 10000 registers that start from the address 0 and they are all Holding Register type. We will then make a dictionary that contains all of our `ModbusSlaveContext` object, everyone with his own ID defined, in this case we only needed one.
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
Then you need to call the function that you have just created in order to start the server, you will do that by simply writing it inside an `if` that allow you to start it by just typing the name of the file in your shell.
```python
server = StartTcpServer(context, identity, (address, port))
if __name__ == "__main__":
    start_server()
```

#### Client
The Client is used to write and read the registers, to start you will import some function and define the log, as you did with the Server. 
A brief explanation:
- ModbusTcpClient: Function that is used to start the connection between the Client and the provided Server
- WriteSingleRegistersRequest: Function that is used to write a value on a single register
- ReadHoldingRegistersRequest: Function that is used to read a value from a Holding Register 
```python
import logging
import keyboard
from random import randint
from time import sleep
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_write_message import WriteSingleRegisterRequest
from pymodbus.register_read_message import ReadHoldingRegistersRequest
```
```python
# Log

FORMAT = ('%(asctime)-15s %(threadName)-15s ''%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
```
We will then start writing down the functions needed by the Client, one of them is obviously the one that allow us to start it.
```python
def start_client(address, port=502):
	"""Function that start a client
	address: the address to witch the client is going to connect
	port: the port of the server to witch the client is going to connect
	"""
```
we will start by creating the Client himself with the function `ModbusTcpClient()`
```python
client = ModbusTcpClient(address, port)
```
this function require as parameters the address and the port of the Server you want to connect to, we will then call a `ModbusTcpClient` object function, `connect()`, that will finally connect the Client to the Server.
```python
client.connect()
```
The Client is now connected to the server and we can comunicate with it.
We needed a loop for continuously reading and writing down the registers so we used `while` to create a reiteration and calling a writing function, this is an example valid for our case but might not be usefull for yours. 
```python
while not True:
		values = []
		values.append(write_hr_request(0, client, randint(10, 30)))
		values.append(write_hr_request(1, client, randint(10, 30)))
		values.append(write_hr_request(2, client, randint(10, 30)))
		values.append(write_hr_request(3, client, randint(10, 30)))
		values.append(write_hr_request(4, client, randint(10, 30)))
		values.append(write_hr_request(5, client, randint(10, 30)))
		values.append(write_hr_request(6, client, randint(10, 30)))
		values.append(write_hr_request(7, client, randint(10, 30)))
		values.append(write_hr_request(8, client, randint(10, 30)))
		values.append(write_hr_request(9, client, randint(10, 30)))
		print(values)
		sleep(50)
```
You then need to close the comunication between the client and the server using the `close()` function,
```python
client.close()
```
We will now show you an example of a writing function.
The first thing is to define the function, so we named it `write_hr_register()` 
```python
def write_hr_request(address, client, value):
	"""Function that read a holding register every 10 minutes
	address: the starting address of the registers
	value: the value to write on the register
	client: the istance of the client to use
	"""
```
We need to send a request to the Server so we use the function `WriteSingleRegisterRequest()` function to create an object that is then used by the `execute()` function to request the writing action to the Server.
```python
request = WriteSingleRegisterRequest(address, value, unit=0x01)
response = client.execute(request)
```
The `WriteSingleRegisterRequest()` function require 3 parameteres to work, the address of the register to write on, the value that is going to be wrote on the register and the Unit ID of the slave that wil perform this task.
The last thing for this function is to return a confirm of the writing so it will return the response object as a string, this can be than printed if wanted for debugging purpose.
```python
return str(response)
```
In the end we will show you a function that read the values of a register so we'll have covered the basics of this library.
We will start as usually by defining the function
```python
def read_register_by_address(client, address, count=1):
	"""Function that read one or more holding register by his address
	client: the istance of the client to use
	address: the starting address of the registers
	count: the number of register to read after the first one
	"""
```
We will then do like we have done with the `write_hr_register()` function, we will create a request and then execute it.
```python
request = ReadHoldingRegistersRequest(address, count, unit=0x01)
response = client.execute(request)
```
The `ReadHoldingRegistersRequest` function require not only the address of the register and the UnitID if the slave but you can also read more than one register at the time, the parameter count is used to know how many register you want to read. You then return the `response.registers` that consist in a list of value.
```python
return response.registers
```
So this is the end of this quick basic introduction to pymodbus, this is not a perfect guide so if you find any error please send an issue on github and we will try to resolve it. We hope this guide has been usefull!

-Strambini Enea & Tezza Giacomo
