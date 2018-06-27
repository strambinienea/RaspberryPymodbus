# Import

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.factory import ClientDecoder
from pymodbus.bit_read_message import ReadCoilsRequest, ReadCoilsResponse

from time import localtime, asctime
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

	read_hr_request(register_index(1, 'T', 2), client)

	client.close()

def read_hr_request(address, client, count=0):
	"""Function that read a holding register every 10 minutes

	address: the starting address of the registers
	count: the number of register to read after the first one
	client: the istance of the client to use
	"""
	first = True
	close = False
	delay = 2
	print('Press "q" to Quit: ')

	# Loop start

	while not close:
		now = asctime(localtime()) # Current local time 
		#time = localtime()
		#now = str(time()[0]) + "-" + str(time()[1]) + "-" + str(time()[2]) + " " + str(time()[3]) +

		if int(now.split(" ")[3].split(":")[1]) % delay == 0 and first or keyboard.is_pressed('a'):			#debug

			if count == 0:
				request = ReadHoldingRegistersRequest(address, count)
				#request = ReadCoilsRequest(address, 0)														#debug
				response = client.execute(request)
				print("[" + now + "] " + str(response))

			else:
				for _ in range(count):
					request = ReadHoldingRegistersRequest(address, count)
					#request = ReadCoilsRequest(address, 0)													#debug
					response = client.execute(request)
					print("[" + now + "] " + str(response))
					address += 1

			first = not first

		elif int(now.split(" ")[3].split(":")[1]) % delay == 0 and not first:
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

		if int(elements[0]) == sector and elements[1] == type and int(elements[2]) == index:
			return int(elements[3])

	return None

	
if __name__ == "__main__":
	start_client('192.168.9.113', 502)
