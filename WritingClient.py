# Import
import logging
import keyboard
from random import randint
from collections import OrderedDict
from pymodbus.constants import Endian
from pymodbus.compat import iteritems
from pymodbus.factory import ClientDecoder
from time import localtime, asctime, sleep
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.register_write_message import WriteSingleRegisterRequest
from pymodbus.bit_read_message import ReadCoilsRequest, ReadCoilsResponse
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse

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
	# Starting and connecting the client to the server
	
	client = ModbusTcpClient(address, port)
	client.connect()
	file = open('/home/pi/Desktop/Tridium/Data/letture.csv', 'w')
	file.close()
	
	while True:
		write_reg_csv('/home/pi/Desktop/Tridium/Data/dati_Trento.csv', '/home/pi/Desktop/Tridium/Data/letture.csv', client)
				
	#file.close()
	client.close()


def write_hr_request(address, client, value):
	"""Function that write a holding register every 10 minutes
	address: the starting address of the registers
	value: the value to write on the register
	client: the istance of the client to use
	"""
	request = WriteSingleRegisterRequest(address, value, unit=0x01)
	response = client.execute(request)
	
	
	
	return (str(response))
	

def write_reg_csv(start_file, log_file, client):
	"""Functoin that, gathered all the data from the start_file,
	write a log in the log_file and write data on registers
	reg 0X00: Current value
	reg 0X100: Daily sum
	reg 0X101: Monthly sum
	reg 0X102: Grand total
	start_file: Path of the file from wich read the data
	log_file: Path of the file in wich write down the log(erase every time it's restated)
	client: The instance of the client that send the request
	"""
	
	first = True
	
	
	for row in open(start_file):
		
		if first:
			first = False
			
		else:
			float_(round(eval(row.split(';')[3]), 3), 0, client)
			float_(round(round(eval(row.split(';')[4])) / 10000, 5), 2, client)
			float_(round(round(eval(row.split(';')[5])) / 10000, 5), 4, client)
			number = round(eval(row.split(';')[3]), 3)

			sleep(60)
	

def float_(number, reg, client):
	number = str(number)
	list_ = number.split('.')
	print(list_)
	write_hr_request(reg, client, int(list_[0]))
	write_hr_request(reg + 1, client, int(list_[1]))



def daily_sum(filename, address, client):
	"""Function that sum all the values in the file, the sum is erased daily
	filename: Path of the file from wich read the data
	"""
	
	file = open(filename, 'r')

	total = 0
	old_total = 0
	data_split = asctime().split(' ')

	
	for row in file:
		if data_split[1] in row and data_split[3] in row:
			if total + eval(row.split(';')[-1]) >= 2 ** 16:
				total += eval(row.split(';')[-1])
				digits = total.split('.')
				write_hr_request(100, client, digits[0])
	
	file.close()
	
	return total * 1000
	
	
def monthly_sum(filename):
	"""Function that sum all the values in the file, the sum is erased monthly
	filename: Path of the file from wich read the data
	"""
	
	file = open(filename, 'r')
	total = 0
	data_split = asctime().split(' ')
	
	for row in file:
		if data_split[1] in row:
			total += eval(row.split(';')[-1])
			digits = str(total).split('.')
			
	
	file.close()
	



def total_sum(filename):
	"""Function that sum all the values in the file, the sum is erased at the reboot
	filename: Path of the file from wich read the data
	"""
	
	file = open(filename, 'r')
	total = 0
	
	for row in file:
		total += eval(row.split(';')[-1])
	
	file.close()
	
	return total * 1000

	
if __name__ == "__main__":
	start_client('192.168.9.116', 502)
