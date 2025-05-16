import socket
import pygame
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

pygame.init()
WIDTH = 800
HEIGHT = 600
color = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown', 'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'Dark Turquoise', 'DeepSkyBlue', 'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue.']
def scroll(event):
    global color
    color = combo.get()
    style.configure("TCombobox", fieldbackground=color,background="white")
def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tkinter.messagebox.showerror("Ошибка: ", "ты не выбрал цвет или имя")
CC = (WIDTH//2, HEIGHT//2)
radius = 50
name = ""
color = ""
root = tkinter.Tk()
root.title("Login")
root.geometry("300x200")
style = ttk.Style()
style.theme_use("classic")
name_label = tk.Label(root, text="Введи свой никнейм:")
name_label.pack()
row = tk.Entry(root, width=30, justify="center")
row.pack()
color_label = tk.Label(root, text="Выбери цвет:")
color_label.pack()
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
        'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
        'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
        'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
        'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']
combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()
name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()
root.mainloop()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Бактерия")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))
sock.send(("color:<" + name + "," + color + ">").encode())
run = True
old = (0,0)
def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first+1:second]
            result = result.split(",")
            return result
    return ""
def draw_bacteries(data: list[str]):
    for num, buct in enumerate(data):
        data = buct.split(" ")
        x = CC[0]+int(data[0])
        y = CC[1]+int(data[1])
        size = int(data[2])
        color = int(data[3])
        pygame.draw.circle(screen,color,(x,y),size)
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0]-CC[0],pos[1]-CC[1]
        lenv = math.sqrt(vector[0]**2+vector[1]**2)
        vector = vector[0] / lenv, vector[1] / lenv
        if lenv <= radius:
            vector = 0,0
        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>"
            sock.send(msg.encode())
    data = sock.recv(1024).decode()
    data = find(data).split(",")
    screen.fill("gray")
    pygame.draw.circle(screen, color, CC, radius)
    if data != [""]:
        draw_bacteries(data)
    pygame.display.update()
pygame.quit()