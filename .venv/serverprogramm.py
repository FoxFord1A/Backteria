import socket
import time

main_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)
main_socket.bind(("localhost",10000))
main_socket.setblocking(False)
main_socket.listen(5)

print("Сокет создался")

players = []


while True:
    try:
        new_socket, addr = main_socket.accept()
        new_socket.setblocking(False)
        print("Подключился", addr)
        players.append(new_socket)
    except BlockingIOError:
        pass
    for sock in players:
        try:
            data = sock.recv(1024).decode()
            print(f"Получил {data}")
        except:
            pass
    for sock in players:
        try:
            sock.send("Тест приёма".encode())
        except:
            players.remove(sock)
            sock.close()
            print("Сокет закрыт")
    time.sleep(1)
