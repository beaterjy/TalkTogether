import socket
import threading
from msg import Msg
from user import User
import tkinter as tk

# default port
default_port = 54123
# connected list
conns = []


class Server(object):
    """
    a simple server
    """

    def __init__(self, port=default_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
        self.sock.listen()
        self.start_server()

    def start_server(self):
        while True:
            try:
                sock, addr = self.sock.accept()
            except Exception as e:
                # some one want to connect, but fail
                print("some one want to connect, but fail")
            finally:
                # some one success connect
                print("[%s:%s] connect successfully." % (addr[0], addr[1]))
                # save in the conns
                conns.append(User(
                    sock=sock,
                    ip=addr[0],
                    port=addr[1],
                ))
                print("now has %s client." % (len(conns)))
                # tell to others and me
                msg = Msg(
                    data="Hello, [%s:%s] login." % (addr[0], addr[1]),
                    mode=Msg.TALK,
                    ip=addr[0],
                    port=addr[1]
                )

                for user in conns:
                    self.send_msg(user, msg)
                server_thread = threading.Thread(target=self.handle_sock, args=(sock, addr))
                server_thread.start()

    # handle for every client
    def handle_sock(self, sock, addr):
        # receive the msg and handle it
        while True:
            try:
                byte_arr = sock.recv(1024)
                # decode the socket bytes
                msg = Msg.decode(byte_arr)
                # (1.mode), (2,ip), (3,port), (4,data)
                # update the (2, ip) and (3, port)
                msg.set_ip(addr[0])
                msg.set_port(addr[1])
                # handle the msg
                if msg.mode == Msg.HELLO:
                    pass
                elif msg.mode == Msg.TALK:
                    # send the msg to everyone
                    # for user in conns:
                    #     self.send_msg(user, msg)
                    # just print in the server
                    print("[%s:%s] > %s" % (msg.ip, msg.port, msg.data))
                elif msg.mode == Msg.FINISH:
                    pass
            except Exception as e:
                # client logout
                # del the conns who logout
                for i in range(len(conns)):
                    if conns[i].ip == addr[0] and conns[i].port == addr[1]:
                        del conns[i]
                print('now has %s client.' % (len(conns)))
                # send the link out msg for everyone
                msg = Msg(
                    data='[%s:%s] logout' % (addr[0], addr[1]),
                    mode=Msg.TALK,
                    ip=addr[0],
                    port=addr[1],
                )
                for user in conns:
                    self.send_msg(user, msg)
                return

    # send the msg to user
    def send_msg(self, user, msg):
        try:
            user.sock.send(msg.encode())
        except Exception as e:
            print('Send Error.')


"""-----------------------------------------------------------------------------------"""


class Client(object):
    """
    a simple client
    """

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(('127.0.0.1', default_port))
            # GUI problem, just print in the server
            # receive_thread = threading.Thread(target=self.receive_msg())
            # receive_thread.start()
            # main input section
            # input_thread = threading.Thread(target=self.start_talking())
            # input_thread.start()
            # self.start_talking()

        except ConnectionError as e:
            print("Connect Fail.")
        finally:
            pass

    def start_talking(self):
        while True:
            try:
                text = input("> ")
                msg = Msg(
                    mode=Msg.TALK,
                    data=text,
                )
                self.sock.send(Msg.encode(msg))
            except Exception as e:
                print("some error happens")
            finally:
                pass
    
    # send the msg
    def send_msg(self, text):
        try:
            msg = Msg(
                    mode=Msg.TALK,
                    data=text,
                )
            self.sock.send(Msg.encode(msg))
        except Exception as e:
            print("send error happens")
            # other way to remind
    
    def receive_msg(self):
        while True:
            try:
                byte_arr = self.sock.recv(1024)
            except Exception as e:
                print("Receive Error.")
            finally:
                # unpack the bytes
                msg = Msg.decode(byte_arr)
                # handle the msg
                if msg.mode == Msg.HELLO:
                    pass
                elif msg.mode == Msg.TALK:
                    # print the msg
                    # print("[%s:%s] > %s" % (msg.ip, msg.port, msg.data))
                    # return the str(msg)
                    return ("[%s:%s] > %s" % (msg.ip, msg.port, msg.data))
                elif msg.mode == Msg.FINISH:
                    pass



