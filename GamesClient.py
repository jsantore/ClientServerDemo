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

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f" got message{self.message}", 200,200, color=(30,200, 30), font_size=20)


def communicate_with_server(client: GameClient):
     client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
     while True:
         message = str.encode("Client Says Hi")
         client_socket.sendto(message, (client.server_addr, Server.SERVER_PORT))
         data_packet = client_socket.recvfrom(1024)
         data = data_packet[0]
         print(f"data on client side {data}")
         client.message = data

if __name__ == '__main__':
    server_addr = input("What server:")
    window = GameClient(server_addr)
    client_thread = threading.Thread(target=communicate_with_server,
                                     args=(window,),daemon=True)
    client_thread.start()
    arcade.run()
