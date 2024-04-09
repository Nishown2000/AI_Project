import socket
import threading

# Function to handle client connections
def handle_client(client, address):
    print(f"New connection from {address}")

    # Receive client's name
    name = client.recv(1024).decode()
    print(f"{address} registered as {name}")

    clients[name] = client

    while True:
        message = client.recv(1024).decode()
        if not message or message.lower() == "exit":
            print(f"Connection closed from {address}")
            del clients[name]
            client.close()
            break

        print(f"Received message from {name}: {message}")

        # Send message to the specified client
        try:
            recipient, message_body = message.split(':')
            recipient = recipient.strip()
            print(f"Recipient {recipient}")
            if recipient in clients:
                print(f"Recipient {recipient} Client {clients}")
                clients[recipient].send(f"{name}: {message_body}".encode())
            else:
                client.send("Error: Recipient not found.".encode())
        except ValueError:
            client.send("Error: Invalid message format.".encode())

# Server configuration
host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

print(f"Server listening on {host}:{port}")

clients = {}

while True:
    client, address = server.accept()

    # Start a thread for each client
    thread = threading.Thread(target=handle_client, args=(client, address))
    thread.start()
