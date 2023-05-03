import socket
from sys import argv
from random import choice

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 1500
wordsList = ["KUKURYDZA", "SAMOLOCIK", "OCZYSZCZALNIA"] # only one-word expressions supported 

def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((HOST, PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print(f"Connected by {addr}")
			initGame()
			conn.sendall(invitationMessage(addr))
			while True:
				data = conn.recv(1024)
				if not data:
					break
				conn.sendall(feedback(data))
			
def feedback(data):
	return data

def initGame():
	global WORD = choice(words)
	
def invitationMessage(addr)
	return r"""
				***********************************************
				** Hello {addr}! The game is on. Good luck!! **
				***********************************************
				
				The word: {WORD}
			"""