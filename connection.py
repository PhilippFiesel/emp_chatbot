import socket

class Connection(socket.socket):
    def __init__(self, ip: str, port: int) -> None:
        self.port = port
        self.ip = ip
        self.address = (self.ip, self.port)
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, msg: bytes) -> None:
        super().sendto(msg, self.address)

    def __del__(self) -> None:
        super().close()
