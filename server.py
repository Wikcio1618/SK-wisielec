import socket
from random import choice
import threading

# adres serwera
HOST = "127.0.0.1"
PORT = 1500
wordsList = ["KUKURYDZA", "SAMOLOCIK", "OCZYSZCZALNIA"] # only one-word expressions supported 
word = ""
tried_letters = set([]) # zbior liter ktore juz byly próbowanie
tries = 10

LETTER_REPEAT_MSG ="""
Już próbowałeś zgadnąć tą literę. Spróbuj inną!! 
Pozostało nadal {} prób.
"""

WIN_MSG = """
***************************
*  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|  *
*  |     ZWYCIĘSTWO    |  *
*  |      wynik: {}     |  *
*  |___________________|  *
***************************
"""

BAD_GUESS_MSG ="""
BŁĄD!! Pozostało prób: {}
"""

GOOD_GUESS_MSG = """
ZGADŁEŚ LITERĘ!! DOBRZE CI IDZIE!
Pozostało {} prób.
"""

LOSE_MSG = """
*********************************
*       P R Z E G R A N A       *
*     _____________________     *
*    |  _________________  |    *
*    | |                 | |    *
*    | |                 | |    *
*    | |_________________| |    *
*    |_____________________|    *
*********************************
"""


def main():
	print(HOST)
	message = ""
	
	# tworzenie gniazda
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# bindowanie adresu	
	s.bind((HOST, PORT))
	# nasłuchiwanie
	s.listen()
	print("Server is running. Waiting for connections...")

	# Create a shutdown event to signal the server to stop
	global shutdown_event
	shutdown_event = threading.Event()

	# Start accepting connections in a separate thread
	connection_thread = threading.Thread(target=accept_connections, args=(s,))
	connection_thread.start()

	try:
		# Wait for the user to interrupt the server with Ctrl+C
		while True:
			pass

	except KeyboardInterrupt:
        # Set the shutdown event to signal the server to stop
		shutdown_event.set()

        # Wait for the connection thread to exit
		connection_thread.join()

# funkcja do czekania na połączenia
def accept_connections(s):
	while not shutdown_event.is_set():
		global addr
		# oczekiwanie na przyjecie połączenia
		conn, addr = s.accept()
		try:
			handleClient(conn)
			
		except KeyboardInterrupt:
			# Handle Keyboard Interrupt (Ctrl+C) from the client
			print("Client disconnected.")
			s.close()

		except ConnectionResetError:
			# Handle connection reset by the client
			print("Client connection reset.")
			s.close()

		except ConnectionAbortedError:
			# Handle connection aborted by the client
			print("Client connection aborted.")
			s.close()

		except Exception as e:
			# Handle other exceptions
			print("Exception occurred:", str(e))
			s.close()

# funkcja do obsługiwania połączonego clienta	
def handleClient(conn):
	with conn:
		print(f"Connected by {addr}")
		initGame()
		# sendall wysyła dane. klient musi je odebrac
		conn.sendall(invitationMessage(addr).encode())

		global tries
		while tries > 0:
			data = conn.recv(1024).decode().upper()
			if not data:
				break
			message = feedback(data, word)

			if message == BAD_GUESS_MSG:
				tries += -1

			if tries == 0:
				break
			else:
				conn.sendall((message.format(tries) + guessedWord2String() + '\n').encode())
		conn.sendall(LOSE_MSG.encode())

# funckja do zwracania odpowiedzi na podstawie inputu clienta
def feedback(data, word):
	output = ""
	
	if len(data) == 1:
		global tried_letters
		if data in tried_letters:
			output = LETTER_REPEAT_MSG
		elif data in word:
			output = GOOD_GUESS_MSG
		else:
			output = BAD_GUESS_MSG
			
		tried_letters.add(data)


	else:
		if data == word:
			output = WIN_MSG
		else:
			output = BAD_GUESS_MSG
	
	return output


# inicjuje zmienne
def initGame():
	global word
	word = choice(wordsList)
	
	global tried_letters
	tried_letters = set([])
	
	global tries
	tries = 10

	
def invitationMessage(addr):
	return f"""
*******************************************************************
** Hello {addr}! The game is on. Good luck!!                
*******************************************************************
				
The word: {guessedWord2String()}
"""


def guessedWord2String():
	string = ""
	for char in word:
		if char in tried_letters:
			string += char
		else:
			string += '_'
		string += ' '
	return string



if __name__ == "__main__":
	main()