
class Msg(object):

    # Msg type
    TALK = 'TALK'
    HELLO = 'HELLO'
    FINISH = 'FINISH'

    def __init__(self, data, ip='None', port='None', mode=TALK):
        self.data = data
        self.mode = mode
        self.ip = ip
        self.port = port

    def __str__(self):
        # (1.mode), (2,ip), (3,port), (4,data)
        return "%s,%s,%s,%s" %(self.mode, self.ip, self.port, self.data)

    def get_type(self):
        return self.mode

    def get_data(self):
        return self.data

    def set_ip(self, ip):
        self.ip = ip

    def set_port(self, port):
        self.port = port

    def encode(self, mode='utf-8'):
        """return bytes"""
        return self.__str__().encode(mode)

    @classmethod
    def decode(cls, byte_arr, mode='utf-8'):
        """return the Msg class"""
        try:
            s = byte_arr.decode(mode)
            lst = s.split(',')
        except Exception as e:
            print("decode Error.")
        finally:
            return Msg(
                mode=lst[0],
                ip=lst[1],
                port=lst[2],
                data=','.join(lst[3:])
            )

