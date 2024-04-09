import socket
import threading

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("Server closed the connection.")
            break

# Client configuration
host = '127.0.0.1'
port = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Register client's name
name = input("Enter your name: ")
client_socket.send(name.encode())

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Main loop to send messages to the server
try:
    while True:
        message = input("Enter Sender name and message [SenderName: Message]: ")
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        else:
            client_socket.send(message.encode())
except KeyboardInterrupt:
    print("Closing the client.")
finally:
    # Close the client socket
    client_socket.close()
