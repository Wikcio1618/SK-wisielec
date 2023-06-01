import socket
from sys import argv
from random import choice

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = socket.gethostname()
PORT = 1500
iter = 0

def client():
	print(HOST)
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		try:
			while True:
				info = s.recv(1024).decode() #Odczyt hasła 
				if info:
					print(info)
					if "P R Z E G R A N A" in info:
						break
					elif "ZWYCIĘSTWO" in info:
						break

					guess = input(" -> ")
					s.send(guess.upper().encode())
			s.close()

		except KeyboardInterrupt:
			print("Closing connection with server")
			s.close()
        
		
		
		
		
		
		
		
if __name__ == "__main__":
	client()            
        
    
