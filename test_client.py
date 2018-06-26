# Import

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.factory import ClientDecoder

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

	read_hr_request(0, 5, client)

	client.close()

def read_hr_request(address, count, client):
	"""Function that read a holding register every 10 minutes
	
	address: the starting address of the registers
	count: the number of register to read after the first one
	client: the istance of the client to use
	"""
	first = True
	close = False
	print('Press "q" to Quit: ')

	# Loop start

	while not close:
		now = asctime(localtime()) # Current local time 

		if int(now.split(" ")[3].split(":")[1]) % 2 == 0 and first:
			request = ReadHoldingRegistersRequest(address, count)
			response = client.execute(request)
			print("[" + now + "] " + str(response.registers))
			first = not first
		
		elif int(now.split(" ")[3].split(":")[1]) % 10 == 0 and not first:
			first = True

		# Key pressed event check

		try:
			if keyboard.is_pressed('q'):
				close = not close
		except:
			pass

	
if __name__ == "__main__":
	start_client('192.168.9.113', 502)
