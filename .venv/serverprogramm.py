import socket
import time
import psycopg2
import pygame
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
pygame.init()
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(("localhost", 10000))
main_socket.setblocking(False)
main_socket.listen(5)
engine = create_engine("postgresql+psycopg2://postgres:2222@localhost/postgres",connect_args={"client_encoding":"utf8","options":"-c lc_messages=en_US.UTF-8"})
Session = sessionmaker(bind=engine)
Base = declarative_base()
s = Session()
WIDTH_ROOM, HEIGHT_ROOM = 4000,4000
WIDTH_SERVER, HEIGHT_SERVER = 300,300
screen = pygame.display.set_mode((WIDTH_SERVER,HEIGHT_SERVER))
pygame.display.set_caption("Maintaince")
clock = pygame.time.Clock()
FPS = 100
color = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown', 'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'Dark Turquoise', 'DeepSkyBlue', 'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue.']
def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first+1:second]
            result = result.split(",")
            result = map(float, result)
            return result
    return ""
def find_color(info: str):
    first = None
    for num, sign in enumerate(info):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = info[first+1:second]
            result = result.split(",")
            return result
    return ""

class Player(Base):
    __tablename__ = "gamers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    address = Column(String)
    x = Column(Integer, default=500)
    y = Column(Integer, default=500)
    size = Column(Integer, default=50)
    errors = Column(Integer, default=0)
    abs_speed = Column(Integer, default=2)
    speed_x = Column(Integer, default=2)
    speed_y = Column(Integer, default=2)
    color = Column(String(250),default="red")
    w_vision = Column(Integer,default=800)
    h_vision = Column(Integer,default=600)

    def __init__(self, name, address):
        self.name = name
        self.address = address

Base.metadata.create_all(engine)
class LocalPlayer:
    def __init__(self, id, name, sock, addr):
        self.id = id
        self.db: Player = s.get(Player, self.id)
        self.sock = sock
        self.name = name
        self.address = addr
        self.x = 500
        self.y = 500
        self.size = 50
        self.errors = 0
        self.abs_speed = 1
        self.speed_x = 0
        self.speed_y = 0
        self.color = "red"
        self.w_vision = 800
        self.h_vision = 600
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
    def change_speed(self, vector):
        vector = find(vector)
        if vector[0] == 0 and vector[1] == 0:
            self.speed_x = self.speed_y = 0
        else:
            vector = vector[0] * self.abs_speed, vector[1] * self.abs_speed
            self.speed_x = vector[0]
            self.speed_y = vector[1]



Base.metadata.create_all(engine)

print("Сокет создался")

players = {}

run = True
while run:
    clock.tick(FPS)
    try:
        new_socket, addr = main_socket.accept()
        new_socket.setblocking(False)
        print("Подключился", addr)
        login = new_socket.recv(1024).decode()
        player = Player("name", addr)
        if login.startswith("color"):
            data = find_color(login[6:])
            player.name,player.color = data
        s.merge(player)
        s.commit()
        addr = f"({addr[0]},{addr[1]})"
        data = s.query(Player).filter(Player.address == addr)
        for user in data:
            player = LocalPlayer(user.id, "name", new_socket, addr)
            players[user.id] = player
    except BlockingIOError:
        pass
    for id in list(players):
        try:
            data = players[id].sock.recv(1024).decode
            print(f"Получил {data}")
            players[id].change_speed(data)
        except:
            pass
    visible_bacteries = {}
    for id in list(players):
        visible_bacteries[id] = []
        pairs = list(players.items())
        for i in range(0, len(pairs)):
            for j in range(i + 1, len(pairs)):
                hero_1: Player = pairs[i][1]
                hero_2: Player = pairs[j][1]
                dist_x = hero_2.x - hero_1.x
                dist_y = hero_2.y - hero_1.y
                if abs(dist_x) <= hero_1.w_vision // 2 + hero_2.size and abs(dist_y) <= hero_1.h_vision // 2 + hero_2.size:
                    x_ = str(round(dist_x))
                    y_ = str(round(dist_y))
                    size_ = str(round(hero_2.size))
                    color_ = hero_2.color
                    data = x_ + " " + y_ + " " + size_ + " " + color_
                    visible_bacteries[hero_1.id].append(data)
                if abs(dist_x) <= hero_2.w_vision // 2 + hero_1.size and abs(dist_y) <= hero_2.h_vision // 2 + hero_1.size:
                    x_ = str(round(dist_x))
                    y_ = str(round(dist_y))
                    size_ = str(round(hero_1.size))
                    color_ = hero_1.color
                    data = x_ + " " + y_ + " " + size_ + " " + color_
                    visible_bacteries[hero_2.id].append(data)
        for id in list(players):
            visible_bacteries[id] = "<"+",".join(visible_bacteries[id])+">"
        try:
            players[id].sock.send(visible_bacteries[id].encode())
        except:
            players[id].sock.close()
            del players[id]
            s.query(Player).filter(Player.id==id).delete()
            s.commit()
            print("Сокет закрыт")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill("black")
    for id in  players:
        player = players[id]
        x = player.x*WIDTH_SERVER//WIDTH_ROOM
        y = player.y*HEIGHT_SERVER//HEIGHT_ROOM
        size = player.size*WIDTH_SERVER//WIDTH_ROOM
        pygame.draw.circle(screen,player.color,(x,y),size)
        players[id].update()
        pygame.display.update()


pygame.quit()
main_socket.close()
s.query(Player).delete()
s.commit()

