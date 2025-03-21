import socket
import pygame

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Бактерия")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))
run = True

while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    sock.send("Пользователь Devloper отправил данные".encode())
pygame.quit()