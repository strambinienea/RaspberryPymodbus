# Import
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.server.sync import StartTcpServer, ModbusBaseRequestHandler
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer, ModbusBinaryFramer
from random import randint
import logging
import keyboard
from time import sleep

# Log

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Defining server function



def start_server(address="0.0.0.0", port=502):
	"""A function that start the server
	address: the address of the server
	port: the port of the server
	"""
	
	# Context



	block1 = ModbusSequentialDataBlock(0, [0]*4)
	floor1 = ModbusSlaveContext(hr=block1)
	block2 = ModbusSequentialDataBlock(4, [0]*6)
	floor2 = ModbusSlaveContext(hr=block2)

	devices = {
	0X01 : floor1,
	0X02 : floor2
	}

	context = ModbusServerContext(devices, single=False)



	# Random values


	random_value(devices[0X01], 3, 0, 4)
	if devices[0X01].validate(3, 0, 4):
		print(devices[0X01].getValues(3, 0, 4))

	random_value(devices[0X02], 3, 4, 6)
	if devices[0X02].validate(3, 4, 6):
		print(devices[0X02].getValues(3, 4, 6))


	# Identity

	identity = ModbusDeviceIdentification()
	identity.VendorName = 'Raspberry'
	identity.ProductCode = 'RB'
	identity.ProductName = 'Raspberry TCP Server'
	identity.ModelName = 'Raspberry TCP Server'

	# Starting server

	server = StartTcpServer(context, identity, (address, port))


def random_value(device, function, address=0, count=0):
	"""A function that randomize the value of the given registers
	device: The istance of the slave to use
	function: The function to use es. 0 for the coil 
	address: The starting address of the registers
	count: The number of register to randomize after the first one
	"""
	if count == 0:
		device.setValues(function, address, [randint(10, 30)])

	else:
		for _ in range(count):
			device.setValues(function, address, [randint(10, 30)])
			address += 1


if __name__ == "__main__":
	start_server()
