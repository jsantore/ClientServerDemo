import arcade
import socket
import Server
import threading
import asyncio

class GameClient(arcade.Window):
    def __init__(self, addr):
        super().__init__(1000,1000, "Client")
        self.message = ""
        self.server_addr = addr
        self.keys:str = ""
        self.player = arcade.Sprite('archer.png', center_x=500, center_y=100)

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f" got message{self.message}", 200,200, color=(30,200, 30), font_size=20)
        ###########new
        self.player.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.keys = f"LEFT{self.keys}"
        elif symbol == arcade.key.RIGHT:
            self.keys = f"RIGHT{self.keys}"

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.keys = self.keys.replace("LEFT", '')
        elif symbol ==arcade.key.RIGHT:
            self.keys = self.keys.replace("RIGHT", '')


def communicate_with_server(client: GameClient):
     client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
     while True:
         message = str.encode(client.keys)
         client_socket.sendto(message, (client.server_addr, Server.SERVER_PORT))
         data_packet = client_socket.recvfrom(1024)
         data = data_packet[0]
         print(f"data on client side {data}")
         playerLoc = str(data, 'UTF-8')
         loc = playerLoc.split(',')
         client.player.center_x = float(loc[0])
         client.player.center_y = float(loc[1])

if __name__ == '__main__':
    server_addr = input("What server:")
    window = GameClient(server_addr)
    client_thread = threading.Thread(target=communicate_with_server,
                                     args=(window,),daemon=True)
    client_thread.start()
    arcade.run()
