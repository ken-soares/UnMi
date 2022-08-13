import socket
import threading

HOST = '127.0.0.1' #change with real IP adress
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
usernames = []

def broadcast(msg):
    for client in clients:
        client.send(msg)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]}: {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(username + " disconnected from server!\n".encode('utf-8'))
            usernames.remove(username)
            break
            

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}.")

        client.send("NICK".encode('utf-8'))
        username = client.recv(1024)
        usernames.append(username)
        clients.append(client)
        print(f"Client username: {username}")
        broadcast(username + " connected to server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is running")
receive()
