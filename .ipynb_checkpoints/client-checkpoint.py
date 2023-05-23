import socket
from sys import argv
from random import choice

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = socket.gethostname()
PORT = 1500
iter = 0

def client():
    print(HOST)
    client_socket = socket.socket() #Tworzenie socketa
    client_socket.connect((HOST, PORT))
    while True:
        info = client_socket.recv(1024).decode() #Odczyt hasła 
        print(info)
        if "Przegrales!" in info:
            break
        elif "Wygrales!" in info:
            break

        guess = input(" -> ")
        client_socket.send(guess.upper().encode())
    client_socket.close()

        

client()            
        
    
