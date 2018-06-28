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

	key_help()
	
	close = False
	while not close:
		try:
			if keyboard.is_pressed('q'):
				close = not close
			elif keyboard.is_pressed('s'):		# Sector
				try:
					sector_in = int(input("Insert the sector index: "))
					sector_ = read_register_by_sector(client, sector_in)
					key_help()
					print('\nSector '+str(sector_in)+': ')
					for i in range(len(sector_)):
						print('\tSensor '+ str(i) + ': ' + str(sector_[i]))
					print()
				except:
					key_help()
					print('Input not valid, please retry: ')
			elif keyboard.is_pressed('t'):		# Type
				try:
					type_in = str(input("Insert the type of sensor letter: "))
					type_ = read_register_by_type(client, type_in)
					key_help()
					print('\nType '+'"'+str(type_in)+'"'+': ')
					for i in range(len(type_)):
						print('\tSensor '+ str(i) + ': ' + str(type_[i]))
					print()
				except:
					key_help()
					print('Input not valid, please retry: ')
			elif keyboard.is_pressed('r'):		# Address
				try:
					address_in = int(input("Insert the register index: "))
					count_in = input("Insert the number of registers you want to read (Press 'Enter' to read only one): ")
					if count_in	== "":
						address_ = read_register_by_address(client, address_in)
						key_help()
						print('\nAddress '+str(address_in)+': ')
						print('\tSensor: ' + str(address_[0]))
						print()
					else:
						address_ = read_register_by_address(client, address_in, int(count_in))
						key_help()
						print('\nAddress '+str(address_in)+': ')
						for i in range(len(address_)):
							print('\tSensor '+ str(i) + ': ' + str(address_[i]))
						print()
				except:
					key_help()
					print('Input not valid, please retry: ')
		except:
			pass

	client.close()


def read_register_by_address(client, address, count=1):
	"""Function that read one or more holding register by his address
	client: the istance of the client to use
	address: the starting address of the registers
	count: the number of register to read after the first one
	"""
	request = ReadHoldingRegistersRequest(address, count, unit=0x01)
	response = client.execute(request)
	
	return response.registers


def read_register_by_sector(client, sector, filename="C:/Users/rtc/Documents/GitHub/RaspberryPymodbus/registers_subdivision.txt"):
	"""Function that read one or more holding registers by a specific sector
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

	if value_list != []:
		return value_list
	else:
		return 'An error has occoured, please retry... '	


def read_register_by_type(client, type, filename="C:/Users/rtc/Documents/GitHub/RaspberryPymodbus/registers_subdivision.txt"):
	"""Function that read one or more holding registers by a specific sector
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

	if value_list != []:
		return value_list
	else:
		return 'An error has occoured, please retry... '


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


def key_help():
	"""Function that print the key help
	"""
	print('\n-------------------------------')
	print('| Press "q" to quit:          |')
	print('| Press "s" to read sector:   |')
	print('| Press "t" to read type:     |')
	print('| Press "r" to read register: |')
	print('-------------------------------\n')


if __name__ == "__main__":
	start_client('192.168.9.101', 502)
