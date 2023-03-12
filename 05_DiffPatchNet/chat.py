import asyncio
import cowsay

clients = {}
cows = cowsay.list_cows()

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    exit, is_login = False, False

    while not reader.at_eof() and not exit:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())

                msg = q.result().decode().split()
                if len(msg) == 0:
                    writer.write("Пользователь {} отправил пустой запрос".format(me))
                    continue

                match msg[0]:
                    case "exit":
                        exit = True
                        break
                    case "cows":
                        writer.write("Список доступных коров: {}\n".format(cows).encode())
                        await writer.drain()
                    case "who":
                        writer.write("Список участников чата: {}\n".format(clients.keys()).encode())
                        await writer.drain()
                    case "say":
                        if is_login:
                            if len(msg) < 2:
                                writer.write("Пустое сообщение от {}\n".format(me).encode())
                                continue
                            client = msg[1]
                            if (client in clients.keys()):
                                await clients[client].put("От {}: {}".format(me, msg[2:]))
                                await writer.drain()
                            else:
                                writer.write("Нет пользователя с таким именем\n".encode())
                                await writer.drain()
                        else:
                            writer.write("Вы не зарегистрированы в чате\n".encode())
                            await writer.drain()
                            continue
                    case "login":
                        if is_login:
                            writer.write("Пользователь {} уже зарегистрирован\n".format(me).encode())
                            continue
                        else:
                            if len(msg) < 2:
                                writer.write("Не введено имя\n".encode())
                                continue
                            cow = msg[1]
                            if cow not in cows:
                                writer.write("Такой коровы ({}) нет\n".format(cow).encode())
                                continue
                            me = cow
                            clients[me] = asyncio.Queue()
                            cows.remove(cow)
                            writer.write("Регистрирую {}\n".format(me).encode())
                            await writer.drain()
                            is_login = True
                            receive.cancel()
                            receive = asyncio.create_task(clients[me].get())
                    case _:
                        writer.write("Неизвестная комманда\n".encode())
                        continue

                for out in clients.values():
                    if out is not clients[me]:
                        await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print("Пользователь {} покинул чат".format(me))
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1234)
    async with server:
        await server.serve_forever()

asyncio.run(main())