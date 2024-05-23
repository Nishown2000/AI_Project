import socket
import threading

# Event to signal when a message has been received
message_received_event = threading.Event()

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
            message_received_event.set()  # Signal that a message has been received
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
    print("                 AI ChatBot                      ")
    print(f"Welcome {name}. You can send messages to anyone. If you want to talk to the AI chatbot, type 'bot'.")
    while True:
        message = input("Enter Sender name and message [SenderName: Message]: ")
        if message.lower() == "exit":
            client_socket.send(message.encode())
            break
        else:
            client_socket.send(message.encode())
            message_received_event.clear()  # Reset the event before waiting for the next message
            message_received_event.wait(50.0)   # Wait for the server's response before sending the next message
except KeyboardInterrupt:
    print("Closing the client.")
finally:
    # Close the client socket
    client_socket.close()
