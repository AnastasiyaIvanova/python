import asyncio
from asyncio import transports


class ServerProtocol(asyncio.Protocol):
    login: str = None
    server: 'Server'
    transport: transports.Transport
    names: list = []
    all_msg: list = []

    def __init__(self, server: 'Server'):
        self.server = server

    def data_received(self, data: bytes):
        print(data)

        decoded = data.decode().strip()

        if self.login is not None:
            self.send_message(decoded)
        else:
            if decoded.startswith("login:"):
                self.login = decoded.replace("login:", "").replace("\r\n", "")

                if self.login in self.names:
                    self.transport.write(f"Логин {self.login} занят, попробуйте другой".encode())
                    asyncio.sleep(2)
                    self.transport.close()
                self.transport.write(
                    f"Привет, {self.login}!\r\n".encode()
                )
                self.names.append(self.login)
                self.send_history(decoded)
            else:
                self.transport.write("Неправильный логин\r\n".encode())

    def connection_made(self, transport: transports.Transport):
        self.server.clients.append(self)
        self.transport = transport
        print("Пришел новый клиент")

    def connection_lost(self, exception):
        self.server.clients.remove(self)
        print("Клиент вышел")

    def send_message(self, content: str):
        message = f"{self.login}: {content}\r\n"
        self.all_msg.append(f"{self.login}: {content}")
        for user in self.server.clients:
            user.transport.write(message.encode())

    def send_history(self, content: str):
        sl = self.all_msg
        if len(self.all_msg) > 9:
            sl = self.all_msg[-11:-1]
        for msg in sl:
            self.transport.write(f"{msg}\r\n".encode())


class Server:
    clients: list

    def __init__(self):
        self.clients = []

    def build_protocol(self):
        return ServerProtocol(self)

    async def start(self):
        loop = asyncio.get_running_loop()

        coroutine = await loop.create_server(
            self.build_protocol,
            '127.0.0.1',
            8888
        )

        print("Сервер запущен ...")

        await coroutine.serve_forever()


process = Server()

try:
    asyncio.run(process.start())
except KeyboardInterrupt:
    print("Сервер остановлен вручную")
