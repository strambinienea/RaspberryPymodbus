# Import

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.factory import ClientDecoder
from pymodbus.bit_read_message import ReadCoilsRequest, ReadCoilsResponse

from time import localtime, asctime, sleep
import logging
import keyboard

# Log

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
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

	# Starting and connecting the client to the server
	
	client = ModbusTcpClient(address, port)
	client.connect()

	client.close()


def read_register_by_address(address, client, count=1):
	"""Function that read a holding register every 10 minutes
	address: the starting address of the registers
	client: the istance of the client to use
	count: the number of register to read after the first one
	"""
	request = ReadHoldingRegistersRequest(address, count, unit=0x01)
	response = client.execute(request)
	
	return response

def read_register_by_sector(client, sector, filename="C:/Users/rtc/Documents/GitHub/RaspberryPymodbus/registers_subdivision.txt"):
	"""Function that read the registers by a specific sector
	client: The istance of the client to use
	sector : The number of the sector where the sensor is located
	"""
	address_list = []
	value_list = []

	for row in open(filename):
		splitted_row = row.split(',')
		#print(splitted_row)
		if str(sector) in splitted_row[0]:
			address_list.append(eval(splitted_row[3]))

	for address in address_list:
		request = ReadHoldingRegistersRequest(address, 1, unit=0x01)
		response = client.execute(request)
		value_list.append(response.registers)

	return value_list	


def read_register_by_type(client, type, filename="C:/Users/rtc/Documents/GitHub/RaspberryPymodbus/registers_subdivision.txt"):
	"""Function that read the registers by a specific sector
	client: The istance of the client to use
	type: The type of the element, for example thermometer(T)
	"""
	address_list = []
	value_list = []

	for row in open(filename):
		splitted_row = row.split(',')
		#print(splitted_row)
		if type in splitted_row[1]:
			address_list.append(eval(splitted_row[3]))

	for address in address_list:
		request = ReadHoldingRegistersRequest(address, 1, unit=0x01)
		response = client.execute(request)
		value_list.append(response.registers)

	return value_list	
def register_index(sector, type, index):
	"""Function that return the register index of a specific sensor
	sector: The number of sector where the sensor is installed
	type: A string that identifies the type of sensor (es. Thermometer - "T")
	index: The index of the sensor (if there are moresensor of the same type)
	"""
	for line in open("C:/Users/rtc/Documents/GitHub/RaspberryPymodbus/registers_subdivision.txt"):
		elements = line.split(',')

		if eval(elements[0]) == sector and elements[1] == type and eval(elements[2]) == index:
			return eval(elements[3])

	return None
	
if __name__ == "__main__":
	start_client('192.168.9.101', 502)
