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
from pymodbus.register_read_message import ReadHoldingRegistersRequest

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
	count = 0
	while True:	
		write_reg_csv('/home/pi/Desktop/Tridium/Data/dati_Trento2', '/home/pi/Desktop/Tridium/Data/letture1.csv', client, count)
			
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
	

def write_reg_csv(start_file, log_file, client, count):
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
	energy_h = 131644850
	reactive_energy_h = 57175898
	
	for row in open(start_file):
		
		if first:
			first = False
			
		else:
			
			# 3 main value
			float_(round(eval(row.split(';')[3]), 3), 500, client)
			float_(round(round(eval(row.split(';')[4])) / 10000, 5), 502, client)
			float_(round(round(eval(row.split(';')[5])) / 10000, 5), 504, client)
			
			# the average 
			float_(round(round(hour_energy(energy_h, eval(row.split(';')[4]))) / 10000, 4), 550, client)
			float_(round(round(hour_energy(reactive_energy_h, eval(row.split(';')[4]))) / 10000, 4), 552, client)			
			
			# sensori
			write_hr_request(510, client, randint(0, 40))
			write_hr_request(511, client, randint(0, 40))
			write_hr_request(512, client, randint(0, 40))
						
			
			count += 1
			write_hr_request(507, client, count)	
			sleep(6)
	

def float_(number, reg, client):
	"""Function that write a float number (16bit) in 2 registers"""
	number = str(number)
	list_ = number.split('.')
	print(list_)
	write_hr_request(reg, client, int(list_[0]))
	write_hr_request(reg + 1, client, int(list_[1]))


def hour_energy(start, value):
	"""Function that calculate the energy used every quarter of an hour"""
	return start + value / 4


	
if __name__ == "__main__":
	start_client('192.168.9.121', 502)
