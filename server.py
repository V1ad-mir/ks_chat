import socket
import threading
from colorama import Fore, Back, Style, init
init()

def handle_client(client_socket, client_address, clients):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "exit":
                break

            # Отправить сообщение от одного клиента всем остальным клиентам
            for client in clients:
                if client != client_socket:
                    client.send((Fore.BLUE + f"Пользователь {client_address}: {message}").encode())
        except ConnectionResetError:
            break

    client_socket.close()
    clients.remove(client_socket)

    print(Fore.RED + f"Пользователь {client_address} вышел из чата.")

    # Отправить сообщение о выходе клиента всем остальным клиентам
    for client in clients:
        client.send((Fore.RED + f"Пользователь {client_address} вышел из чата.").encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1234))
    server_socket.listen(5)
    print(Fore.YELLOW + "Сервер запущен. Ожидаеться подключение пользователей...")

    clients = []

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(Fore.GREEN + f"Пользователь {client_address} онлайн.")

        # Запустить поток для обработки клиента
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        client_thread.start()

if __name__ == "__main__":
    start_server()