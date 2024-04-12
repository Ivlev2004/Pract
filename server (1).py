#!/usr/bin/python3

import socket
import threading
import json
import struct
from datetime import datetime
import os



# Функция для обработки подключения клиента
def handle_client(conn, addr):
    print(f"Подключение установлено с {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            print(f"Подключение с {addr} разорвано")
            break

        # Определение типа данных от клиента и их обработка
        if data.startswith(b"SET_ROOT:"):
            new_root = data[len(b"SET_ROOT:"):]
            # Здесь можно выполнить необходимые действия по установке новой корневой папки
            print(f"Установлена новая корневая папка: {new_root.decode()}")
            # Отправляем ответ клиенту, что операция выполнена успешно
            conn.sendall(b"New root folder set successfully.")
        elif data.strip().isdigit():
            # Обработка данных от клиента 3
            print(f"Получено число от клиента 3: {data.decode()}")
            # Здесь можно выполнить необходимые действия с числом
            # Например, можно преобразовать его в квадрат и отправить обратно клиенту
            squared_number = str(int(data.strip()) ** 2).encode()
            conn.sendall(squared_number)
        else:
            data = []
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data.extend(chunk.decode().split())
                if "end" in data:
                    data.remove("end")
                    break
            print("Received data:", data)
            save_tree(map(int, data))

    conn.close()

# Функция для запуска сервера
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        # Запускаем новый поток для обработки подключения
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

# Запускаем сервер на localhost и порту 9999
start_server('localhost', 9998)
