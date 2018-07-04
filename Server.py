# Import
import logging
import keyboard
from time import sleep
from random import randint
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server.sync import StartTcpServer, ModbusBaseRequestHandler
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer, ModbusBinaryFramer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse

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

	block1 = ModbusSequentialDataBlock(0, [0]*10000)
	floor1 = ModbusSlaveContext(hr=block1)

	devices = {
	0X01 : floor1		
	}

	context = ModbusServerContext(devices, single=False)

	# Identity

	identity = ModbusDeviceIdentification()
	identity.VendorName = 'Raspberry'
	identity.ProductCode = 'RB'
	identity.ProductName = 'Raspberry TCP Server'
	identity.ModelName = 'Raspberry TCP Server'

	# Starting server

	server = StartTcpServer(context, identity, (address, port))

if __name__ == "__main__":
	start_server()
		
