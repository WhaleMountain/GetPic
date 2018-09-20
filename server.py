import socket, ssl
import subprocess
import cv2
import base64

#サーバ側に送信する物をバイト型に変換
def conver():
    with open("snap.jpg","rb") as f:
        r = f.read()
        rc =base64.b64encode(r)
    delpic()
    return rc

#文字列を指定の数ずつに区切る
def split_str(s, n):
    "split string by its length"
    #sorce by http://yak-shaver.blogspot.jp/2013/08/blog-post.html
    length = len(s)
    return [s[i:i+n] for i in range(0, length, n)]

#写真を撮る
def getpic():
    camera_port = 0   # /dev/video0
    cap = cv2.VideoCapture(camera_port)
    print("Taking image...")
    ret, im = cap.read()
    if ret==True:
        file_name = "snap.jpg"
        cv2.imwrite(file_name, im)
    cap.release()

#写真を削除
def delpic():
    cmd = ["rm","snap.jpg"]
    subprocess.check_call(cmd)


if __name__ == "__main__":
    IP = "Your IP add"
    PORT = 1270

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="oreore.crt", keyfile="oreore.key")

    print("Whaiting for connection...")
    bindsocket = socket.socket()
    bindsocket.bind((IP,PORT))
    bindsocket.listen(5)

    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket,server_side=True)
    print("Conneted")

    while True:
        rmsg = connstream.recv(1024)
        if rmsg.decode() == "get":
            print("Ok.")
            getpic()
            conver_byte = conver()
            conver_byte_split = split_str(conver_byte,1000)
            msg = len(conver_byte_split)
            connstream.sendall(str(msg).encode())
            for i in conver_byte_split:
                connstream.sendall(i)
        elif rmsg.decode() == "end":
            break
        else:
            print("Re:"+rmsg.decode())
            continue


    connstream.shutdown(socket.SHUT_RDWR)
    connstream.close()