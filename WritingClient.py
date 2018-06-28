# Import
import logging
import keyboard
from random import randint
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.register_write_message import WriteSingleRegisterRequest
from pymodbus.factory import ClientDecoder
from pymodbus.bit_read_message import ReadCoilsRequest, ReadCoilsResponse
from time import localtime, asctime, sleep

# Log

FORMAT = ('%(asctime)-15s %(threadName)-15s ''%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Defining server function

def start_client(address, port=502):
	"""Function that start a client
	address: the address to witch the client is going to connect
	port: the port of the server to witch the client is going to connect
	"""
	decoder = ClientDecoder()
	closed = False

	# Starting and connecting the client to the server
	
	client = ModbusTcpClient(address, port)
	client.connect()
		
	while not closed:
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
			
			
	client.close()


def write_hr_request(address, client, value):
	"""Function that read a holding register every 10 minutes
	address: the starting address of the registers
	value: the value to write on the register
	client: the istance of the client to use
	"""

	now = asctime() # Current local time
	request = WriteSingleRegisterRequest(address, value, unit=0x01)
	response = client.execute(request)
	
	return (str(response))


def register_index(sector, type, index):
	"""Function that return the register index of a specific sensor
	sector: The number of sector where the sensor is installed
	type: A string that identifies the type of sensor (es. Thermometer - "T")
	index: The index of the sensor (if there are moresensor of the same type)
	"""
	for line in open('./registers_subdivision.txt'):
		elements = line.split(',')

		if eval(elements[0]) == sector and elements[1] == type and eval(elements[2]) == index:
			return eval(elements[3])

	return None

	
if __name__ == "__main__":
	start_client('192.168.9.101', 502)
