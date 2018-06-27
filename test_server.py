# Import
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.server.sync import StartTcpServer, ModbusBaseRequestHandler
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer, ModbusBinaryFramer
from random import randint
import logging
import keyboard

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

    thermometer1 = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*1))
    thermometer2 = ModbusSlaveContext(hr=ModbusSequentialDataBlock(1, [0]*1))
    barometer = ModbusSlaveContext(hr=ModbusSequentialDataBlock(2, [0]*1))
    context = ModbusServerContext([thermometer1, thermometer2, barometer], single=True)

	
    therm1_slave = context[0][0]  #Slave context used in for writing a reading reg
    therm2_slave = context[0][1]
    bar_slave = context[0][2]

    # Random values

    random_value(therm1_slave, 0)
    print(therm1_slave.getValues(3, 0))
	
    # Identity

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Raspberry'
    identity.ProductCode = 'RB'
    identity.ProductName = 'Raspberry TCP Server'
    identity.ModelName = 'Raspberry TCP Server'

    # Starting server

    server = StartTcpServer(context, identity, (address, port))
	


def random_value(slave, address=0, count=0):
	"""A function that randomize the value of the given registers
	server: the istance of the server to use
	address: the starting address of the registers
	count: the number of register to randomize after the firs one
	"""
	if count == 0:
		slave.setValues(3, address, [randint(10, 30)])

	else:
		for _ in range(count):
			slave.setValues(3, address, [randint(10, 30)])
			address += 1


if __name__ == "__main__":
	start_server()
