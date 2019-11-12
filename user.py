
class User(object):

    def __init__(self, sock, ip='None', port='None', name="None"):
        self.sock = sock
        self.ip = ip
        self.port = port
        self.name = name    #no used

    def get_sock(self):
        return self.sock

    def set_sock(self, sock):
        self.sock = sock

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port