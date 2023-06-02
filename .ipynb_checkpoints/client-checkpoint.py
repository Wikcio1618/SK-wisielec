import socket
from sys import argv
from random import choice


def main():
	# adres serwera z argumentów
	HOST = argv[1]
	PORT = int(argv[2])
	
	# tworzenie gniazda
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		try:
			while True:
				# odbieranie danych
				info = s.recv(1024).decode() #Odczyt hasła
				
				# obsluga danych jesli istnieja z ewentualnym rozlaczeniem 				
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
	if len(argv) == 3:
		main()
	else:
		print("Give two arguments: ip and port")
        
    
