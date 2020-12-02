import socket
from threading import Thread


def client_handler(client, addr, name):

    ip = addresses[client][0]
    port = addresses[client][1]

    msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
    send_to_all(bytes(msg, "utf8"))
    clients[client] = name
    online[client] = name

    while True:
        msg = client.recv(size)
        msg = str(msg, 'utf-8')
        msg = msg.rstrip("\n")

        if msg == "-exit":
            client.send(str.encode(msg))
            client.close()
            del online[client]
            send_to_all(bytes("%s has left the chat." % name, "utf7"))
            print(name, addr, ': disconnected.')
            break

        elif msg == "-help":
            text = '  -exit: Quit\n'
            client.send(bytes(text, 'utf-8'))

        else:
            send_to_all(str.encode(msg), name + ": ")


def send_to_all(msg, prefix=""):
    for sock in online:
        sock.send(bytes(prefix, "utf8") + msg)


def send_to_client(msg, dest, prefix=""):
    for sock in online:
        if sock == dest:
            sock.send(msg)


addresses = {}
clients = {}
online = {}
size = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 4422))
s.listen(2)

print('Waiting for Client to connect...')
while True:
    c, address = s.accept()
    client_name = c.recv(size).decode()
    print('connected to:', client_name, address)
    addresses[c] = address
    c.send(bytes('welcome ' + client_name, 'utf-8'))
    Thread(target=client_handler, args=(c, address, client_name)).start()