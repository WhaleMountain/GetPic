import socket, ssl
import base64

def copy(cp_str):
    with open("getpic.jpg","wb") as f:
        cp_file = base64.b64decode(cp_str)
        f.write(cp_file)

if __name__ == "__main__":

    IP = "Your IP add"
    PORT = 1270

    context = ssl.create_default_context()
    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    context.load_verify_locations("oreore.crt")

    print("Connecting")

    client = context.wrap_socket(socket.socket(socket.AF_INET),server_hostname=IP)
    client.connect((IP,PORT))

    print("Connected")

    while True:
        #メッセージ送信
        msg = input("message:")
        client.sendall(msg.encode())
        if msg == "get":
            piclen = client.recv(1024)
            piclen = int(piclen.decode())
            cp_str = "".encode()
            for i in range(piclen):
                cp_str += client.recv(1024)
            copy(cp_str)
        elif msg == "end":
            break

    client.close()