import socket
import threading
from colorama import Fore, Back, Style, init
init()

def receive_messages(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        print(response)
        print( Fore.WHITE + f"Введите сообщение (или 'exit' для выхода):")


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))
    print(Fore.YELLOW + "Соединение с сервером установлено." + Style.RESET_ALL)


    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Введите сообщение (или 'exit' для выхода): \n")
        client_socket.send(message.encode())
        if message == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()