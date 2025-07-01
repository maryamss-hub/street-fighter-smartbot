import socket
import json
from game_state import GameState
import sys
from bot import Bot

def connect(port):
    import time
    time.sleep(2)  # Delay 2 seconds
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print("Connected to game!")
    return client_socket

def send(client_socket, command):
    """Send the command to BizHawk."""
    command_dict = command.object_to_dict()
    payload = json.dumps(command_dict).encode()
    client_socket.sendall(payload)

def receive(client_socket):
    """Receive and parse the game state from BizHawk."""
    payload = client_socket.recv(4096)
    input_dict = json.loads(payload.decode())
    game_state = GameState(input_dict)
    return game_state

def main():
    if sys.argv[1] == '1':
        client_socket = connect(9999)
    elif sys.argv[1] == '2':
        client_socket = connect(10000)
    else:
        print("Invalid player ID. Use '1' or '2'.")
        return

    current_game_state = None
    bot = Bot()
    while (current_game_state is None) or (not current_game_state.is_round_over):
        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state, sys.argv[1])
        send(client_socket, bot_command)

if __name__ == '__main__':
    main()