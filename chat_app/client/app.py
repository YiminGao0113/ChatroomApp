import sys
import time
from client import Client
from threading import Thread
from tkinter import *

class GUI:
    def __init__(self):

        # chat window which is currently hidden
        self.run = 1
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the curser
        self.entryName.focus()
        self.entryName.bind('<Return>', self.login_enter)

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)

        self.Window.mainloop()

    def login_enter(self, event):
    	self.goAhead(self.entryName.get())

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        self.client = Client(name)

        # the thread to receive messages
        rcv = Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.64,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()
        self.entryMsg.bind('<Return>',self.press_enter)
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=5,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.67,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.15)

        self.buttonExit = Button(self.labelBottom,
                                 text="Exit",
                                 font="Helvetica 10 bold",
                                 width=5,
                                 bg="#ABB2B9",
                                 command=lambda: self.exitButton())

        self.buttonExit.place(relx=0.83,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.15)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def press_enter(self, event):
    	self.sendButton(self.entryMsg.get())

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        self.client.send_message(msg)

    def exitButton(self):
        self.client.send_message("quit")
        self.Window.destroy()
        self.run = 0

    # function to receive messages
    def receive(self):

        """
        update local list of messages
        """
        msgs = []
        while True:
            try:
                time.sleep(0.1)  # update every 0.1 second
                new_messages = self.client.get_messages()  # get any new messages from client
                msgs.extend(new_messages)  # add to local list of messages

                for msg in new_messages:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         msg + "\n\n")

                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)

                    if msg == self.client.name + ": " + "quit":
                        break
            except:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!")
                break


        # create a GUI class object


g = GUI()
while True:
    if g.run == 0:
        break
sys.exit(0)