import socket
import threading
import json
import requests

# Define the model to be used for the chatbot
model = "phi3"  # Update this for the desired model

def chat(messages):
    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # The response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message

# Function to handle client connections
def handle_client(client, address):
    print(f"New connection from {address}")

    # Receive client's name
    name = client.recv(1024).decode()
    print(f"{address} registered as {name}")

    clients[name] = client
    messages = []

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
            if recipient.lower() == "bot":
                print("Chatbot is activated ...")
                messages.append({"role": "user", "content": message_body})
                response = chat(messages)
                messages.append(response)
                client.send(response["content"].encode())
            else:
                if recipient in clients:
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

try:
    while True:
        client, address = server.accept()

        # Start a thread for each client
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()
except KeyboardInterrupt:
    exit(0)
