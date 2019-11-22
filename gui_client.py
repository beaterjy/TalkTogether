import tkinter as tk
from socket_pack import Client

class ClientGui(object):

    def __init__(self):
        # start the client
        self.client = Client()

        self.window = tk.Tk()
        self.window.title('Client')
        # window size
        self.window.geometry("200x300")

        # label1
        l_rec = tk.Label(self.window
                        ,text="recive message"
                        ,bg="green"
                        ,font=("Arial", 12)
                        )
        l_rec.pack()

        # Text1
        text_rec = tk.Text(self.window, height=5, )
        text_rec.pack()

        # label2
        l_send = tk.Label(self.window
                            ,text="send message"
                            ,bg='green'
                            ,font=("Arial", 12)
                            )
        l_send.pack()

        # Text2
        self.text_send = tk.Text(self.window, height=2)
        self.text_send.pack()

        # button send
        bt = tk.Button(self.window,
                        text='send',
                        command=self.send_button
                        ).pack()

        # show the window
        self.window.mainloop()

    def send_button(self):
        var = self.text_send.get("0.0", "end")
        self.client.send_msg(var)
        # clear the text send section
        self.text_send.delete("0.0", "end")
        

if __name__ == "__main__":
    client_obj = ClientGui()