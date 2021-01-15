import socket
import threading


class Server:
    def __init__(self, IP, port, **kwargs):
        super().__init__(**kwargs)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, port))
        self.client = None
        self.running = True

    def start(self):
        self.server.listen()
        self.client = self.server.accept()
        threading.Thread(target=self.handle_client, args=(self.client,)).start()

    def handle_client(self, client):
        conn: socket.socket
        conn, addr = client

    def send(self, conn, msg):
        pass
