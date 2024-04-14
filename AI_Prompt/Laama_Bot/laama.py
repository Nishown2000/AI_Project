import threading
import subprocess
import queue
import os

class ChatRunnerThread(threading.Thread):
    def __init__(self, output_queue):
        super(ChatRunnerThread, self).__init__()
        self.output_queue = output_queue

    def run(self):
        # Get the present working directory
        pwd = os.getcwd()

        # Construct the full path to the 'chat' executable
        executable_path = os.path.join(pwd, "chat")

        process = subprocess.Popen([executable_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        for line in process.stdout:
            self.output_queue.put(line.strip())

    def send_input(self, user_input):
        self.output_queue.put(user_input)

class InputProcessingThread(threading.Thread):
    def __init__(self, output_queue, chat_runner):
        super(InputProcessingThread, self).__init__()
        self.output_queue = output_queue
        self.chat_runner = chat_runner

    def run(self):
        while True:
            user_input = input("You: ")

            if user_input.lower() == "exit":
                break

            # Pass the input to the chat executable using the ChatRunnerThread instance
            self.chat_runner.send_input(user_input)

            # Wait for the response from the chat executable
            response = self.output_queue.get()
            print("Bot:", response)

def main():
    output_queue = queue.Queue()

    # Start the thread responsible for running the 'chat' executable
    chat_runner = ChatRunnerThread(output_queue)
    chat_runner.start()

    # Start the thread responsible for taking user input and processing output
    input_processor = InputProcessingThread(output_queue, chat_runner)
    input_processor.start()

    # Wait for both threads to finish
    chat_runner.join()
    input_processor.join()

if __name__ == "__main__":
    main()
