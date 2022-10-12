import socket
from _thread import *
import pickle
from g import Game

server = '96.29.161.100'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print('Waiting for connection')

connected = set()
games = {}
id_count = 0

def threaded_client(conn, p, game_id):
    global id_count
    conn.send(str.encode(str(p)))

    reply = ''
    while True:
        try:
            data = conn.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset_went()
                    elif data != 'get':
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break
    print('Lost Connection', game_id)
    try:
        del games[game_id]
    except:
        pass
    id_count -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print('Connected to: ', addr)

    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print('Creating New Game')
    else:
        games[game_id].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, game_id))