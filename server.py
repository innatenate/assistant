import socket
import threading
import keywordprocessor
import weatherhandler
import universal


header = 120
port = 6060
mainServer = "192.168.1.4"
addr = (mainServer, port)
form = "utf-8"
disconnect = "ERROR"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)

def clientHandler(conn, caddr):
    print("[SERV] New client joined")
    print(f"[SERV] {caddr[0]}")

    connectionStable = True

    while connectionStable:
        msg_length = conn.recv(header).decode(form)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(form)
            if disconnect in msg:
                connectionStable = False

            if "commandprocess" in msg:
                newmsg = msg.replace("commandprocess ", "")
                success = keywordprocessor.Process(newmsg)
                if success:
                    speech = open(f"speech{universal.speech}.mp3", "r")
                    conn.send(speech.encode(form))
                ## Process what next for client command process (play sound on client) (return sound?)
            elif "update" in msg:
                newmsg = msg.replace("update ", "")
                data = weatherhandler.valueUpdate(None, None, True)
                if data:
                    conn.send(speech.encode(form))
                ## Return weather data to client

def start():
    print("[SERV] Starting server")
    server.listen()

    while True:
        conn, caddr = server.accept()
        thread = threading.Thread(target=clientHandler, args=(conn, caddr))
        thread.start()


