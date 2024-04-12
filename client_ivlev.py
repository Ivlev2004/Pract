import socket
import json

def send_data_to_server(sock, data):
    """
    Отправка данных серверу с обработкой специфических команд.
    """
    if data.startswith("SET_ROOT:"):
        sock.send(data.encode())
    elif data.isdigit():
        sock.send(data.encode())  # Отправка данных как числовые значения (для команды клента 3)
    else:
        data += " end" # Добавляем маркер конца данных
        sock.send(data.encode())

def main():
    # Установка сетевого соединения с сервером
    host = 'localhost'
    port = 9998
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        print("Соединение с сервером установлено.")

        while True:
            data = input("Введите данные для отправки серверу (или 'exit' для выхода): ")
            if data.lower() == 'exit':
                break

            send_data_to_server(sock, data)
            response = sock.recv(1024)
            print("Ответ сервера:", response.decode())

    except ConnectionRefusedError:
        print("Невозможно подключиться к серверу")
    finally:
        sock.close()
        print("Подключение закрыто.")

if __name__ == "__main__":
    main()