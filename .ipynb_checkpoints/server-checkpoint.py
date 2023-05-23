import socket
from sys import argv
from random import choice

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = socket.gethostname()
PORT = 1500
wordsList = ["KUKURYDZA", "SAMOLOCIK", "OCZYSZCZALNIA"] # only one-word expressions supported 
word = ""
guessed_word = ""
tried_letters = set([])
tries = 10

LETTER_REPEAT_MSG ="""
Już próbowałeś zgadnąć tą literę. Spróbuj inną!! 
Pozostało nadal {} prób.
"""

WIN_MSG = """
***************************
*  |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|  *
*  |     ZWYCIĘSTWO    |  *
*  |     w {} próbach  |  *
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
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print(f"Connected by {addr}")
			initGame()
			conn.sendall(invitationMessage(addr).encode())
			global tries
			while tries > 0:
				data = conn.recv(1024).decode().upper()
				if not data:
					break
				message = feedback(data, word)

				conn.sendall(message.format(tries).encode())
				conn.sendall(guessedWord2String().encode())
				if message == BAD_GUESS_MSG:
					tries += -1
			conn.sendall(LOSE_MSG.encode())
			
					
			
def feedback(data, word):
	if len(data) == 1:
		global tried_letters
		output = ""
		if data in tried_letters:
			output = LETTER_REPEAT_MSG
		elif data in word:
			output = GOOD_GUESS_MSG
		else:
			output = BAD_GUESS_MSG
			
		tried_letters.add(data)


	else:
		if data == WORD:
			output = WIN_MSG	
		else:
			output = BAD_GUESS_MSG	
	
	return output

def initGame():
	global word
	word = choice(wordsList)
	global guessed_word
	guessed_word = ['_'] * len(word)

	
def invitationMessage(addr):
	return f"""
*******************************************************************
** Hello {addr}! The game is on. Good luck!!                
*******************************************************************
				
The word: {guessedWord2String()}
"""

def guessedWord2String():
	string = ""
	for char in guessed_word:
		string += char
		string += ' '
	return string

main()