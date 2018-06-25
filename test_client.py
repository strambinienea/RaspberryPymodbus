from time import sleep
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.register_read_message import ReadRegistersRequestBase, ReadHoldingRegistersRequest, ReadHoldingRegistersResponse
from pymodbus.factory import ClientDecoder
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def start_client(address, port):
	"""Function that start a client

	address: the address to witch the client is going to connect
	port: the port of the server to witch the client is going to connect
	"""
	decoder = ClientDecoder()	

	# Starting and connecting the client to the server
	
	client = ModbusTcpClient(address, port)
	client.connect()
	
	#request = ReadHoldingRegistersRequest(32, 1)
	#response = client.execute(request)
	#print(response.registers)
	sleep(10)

	client.close()

	
if __name__ == "__main__":
	start_client('192.168.9.101', 502)
