import socket

SERVER_PORT = 25001

def find_server_address():
    server_address = ""
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.connect(('10.255.255.255', 1))
        server_address = conn.getsockname()[0]
    except IOError:
        server_address = '127.0.0.1'
    finally:
        conn.close()
    return server_address

def process_movement(keys:str, player_pos):
    new_player_pos = player_pos
    if keys.find("LEFT") >=0:
        new_player_pos = (player_pos[0]-.1, player_pos[1])
    elif keys.find("RIGHT")>=0:
        new_player_pos = (player_pos[0]+.1, player_pos[1])
    return new_player_pos

def run_server():
    player_pos = (500, 700)
    server_address = find_server_address()
    print(f"Server listening on {server_address} Port: {SERVER_PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_address, SERVER_PORT))
    while True:
        data_packet = server_socket.recvfrom(1024)
        data = data_packet[0]
        data = str(data, 'utf-8')
        client_address = data_packet[1]
        player_pos = process_movement(data, player_pos)
        print(f" got {data} from {client_address}")
        server_socket.sendto(str.encode(f"{player_pos[0]},{player_pos[1]}"),client_address)

if __name__ == '__main__':
    run_server()