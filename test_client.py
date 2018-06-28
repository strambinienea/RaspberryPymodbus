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

	read_hr_request(register_index(1, 'T', 1), client)

	client.close()

def read_hr_request(address, client, count=1):
	"""Function that read a holding register every 10 minutes
	address: the starting address of the registers
	count: the number of register to read after the first one
	client: the istance of the client to use
	"""
	first = True
	close = False
	delay = 5
	print('\n----------------------\n'+'| Press "q" to Quit: |\n'+'----------------------\n')

	# Loop start

	while not close:
		now = asctime() # Current local time

		if int(now.split(" ")[3].split(":")[1]) % delay == 0 and first:
			
			request = ReadHoldingRegistersRequest(address, count, unit=0x01)
			response = client.execute(request)
			print("\n[" + now + "] " + str(response.registers) + "\n")

			first = not first
			sleep(5)

		elif int(now.split(" ")[3].split(":")[1]) % delay != 0 and not first:
			first = True

		# Key pressed event check

		try:
			if keyboard.is_pressed('q'):
				close = not close
		except:
			pass

def register_index(sector, type, index):
	"""Function that return the register index of a specific sensor
	sector: The number of sector where the sensor is installed
	type: A string that identifies the type of sensor (es. Thermometer - "T")
	index: The index of the sensor (if there are moresensor of the same type)
	"""
	for line in open('C:/Users/rtc/Documents/GitHub/RaspberryPymodbus/registers_suddivision.txt'):
		elements = line.split(',')

		if eval(elements[0]) == sector and elements[1] == type and eval(elements[2]) == index:
			return eval(elements[3])

	return None

	
if __name__ == "__main__":
	start_client('192.168.9.113', 502)