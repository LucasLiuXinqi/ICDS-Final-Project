#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import tkinter

from chat_utils import *
import json
import indexer
import pickle
import os
import random

# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        self.sonnet = indexer.PIndex("AllSonnets.txt")
        self.recv_msg= ''

    def login(self):
        # login window
        self.login_window = Toplevel()
        # set the title
        self.login_window.title("Login")
        self.login_window.resizable(width=False,
                                    height=False)
        self.login_window.configure(width=400,
                                    height=150,
                                    bg = "skyblue")

        # username label
        self.username_label = Label(self.login_window, text="Enter User Name: ", font="Helvetica 14", bg = "skyblue")
        self.username_label.place(relheight=0.2,
                                  relx=0.1,
                                  rely=0.125)

        # password label
        self.password_label = Label(self.login_window, text="Enter Password: ", font="Helvetica 14", bg = "skyblue")
        self.password_label.place(relheight=0.2,
                            relx=0.1,
                            rely=0.38)

        # username entry box
        self.username = StringVar()
        self.username_entry = Entry(self.login_window, textvariable=self.username, font="Helvetica 14", bg = "skyblue")
        self.username_entry.place(relwidth=0.4,
                             relheight=0.18,
                             relx=0.425,
                             rely=0.14)

        # password entry box
        self.password = StringVar()
        self.password_entry = Entry(self.login_window, textvariable=self.password, font="Helvetica 14", bg = "skyblue", show="*")
        self.password_entry.place(relwidth=0.4,
                             relheight=0.18,
                             relx=0.425,
                             rely=0.4)






        #signup button
        self.signup_button = Button(self.login_window, text="Sign Up", font="Helvetica 14", command=self.user_signup, highlightbackground='skyblue')
        self.signup_button.place(relx=0.2,
                      rely=0.65)

        #login button
        self.login_button = Button(self.login_window, text="Login", font="Helvetica 14", command=self.user_login, highlightbackground='skyblue')
        self.login_button.place(relx=0.5,
                      rely=0.65)


        self.Window.mainloop()


    def user_signup(self):
        def sign():
            password = self.password_new.get()
            confirm = self.confirm_new.get()
            username = self.username_new.get()
            with open('usrs_info.pickle', 'rb') as user_file:
                try:
                    exist_user_info = pickle.load(user_file)
                    if password != confirm:
                        messagebox.showerror(title='Error', message='Password and Confirm Password must be same!')

                    elif username in exist_user_info:
                        messagebox.showerror(title='Error', message='The user has already existed!')

                    else:
                        exist_user_info[username] = password
                        with open('usrs_info.pickle', 'wb') as user_file:
                            pickle.dump(exist_user_info, user_file)
                        messagebox.showinfo(title='Welcome', message='You have successfully signed up!')
                        self.signup_window.destroy()

                except:
                    exist_user_info = {}
                    if password != confirm:
                        messagebox.showerror('Error', 'Password and confirm password must be the same!')
                    elif username in exist_user_info:
                        messagebox.showerror('Error', 'The user has already signed up!')
                    else:
                        exist_user_info[username] = password
                        with open('usrs_info.pickle', 'wb') as usr_file:
                            pickle.dump(exist_user_info, usr_file)
                        messagebox.showinfo('Welcome', 'You have successfully signed up!')
                        self.signup_window.destroy()


        self.signup_window = Toplevel(self.login_window)
        self.signup_window.title('Sign Up')
        self.signup_window.geometry('350x165')
        self.signup_window.resizable(width=False, height=False)
        self.signup_window.configure(bg = "skyblue")


        self.username_new = StringVar()
        self.username_new.set('')
        Label(self.signup_window, text='User name: ', bg = "skyblue").place(x=10, y=10)
        self.entry_new_name = Entry(self.signup_window, textvariable=self.username_new, bg = "skyblue")
        self.entry_new_name.place(x=150, y=10)

        self.password_new = StringVar()
        Label(self.signup_window, text='Password: ', bg = 'skyblue').place(x=10, y=50)
        self.entry_usr_pwd = Entry(self.signup_window, textvariable=self.password_new, show='*', bg = 'skyblue')
        self.entry_usr_pwd.place(x=150, y=50)

        self.confirm_new = StringVar()
        Label(self.signup_window, text='Confirm password: ', bg = 'skyblue').place(x=10, y=90)
        self.entry_usr_pwd_confirm = Entry(self.signup_window, textvariable=self.confirm_new, show='*', bg = 'skyblue')
        self.entry_usr_pwd_confirm.place(x=150, y=90)

        self.confirm_button = Button(self.signup_window, text='Sign up', command=sign, highlightbackground = 'skyblue')
        self.confirm_button.place(x=150, y=130)



    def user_login(self):
        username = self.username.get()
        password = self.password.get()
        with open('usrs_info.pickle', 'rb') as user_file:
            try:
                exist_user_info = pickle.load(user_file)
            except EOFError:
                exist_user_info = {}
        if username in exist_user_info:
            if password == exist_user_info[username]:
                messagebox.showinfo(title='Welcome', message='Enjoy chatting! ' + username)
                self.login_window.destroy()
                self.goAhead(username)
                self.sendButton('who')
            else:
                messagebox.showerror(title='Error', message='Your password is wrong, try again.')
        else:
            is_sign_up = messagebox.askyesno('Welcome',
                                             'You have not signed up yet. Do you want to sign up now?')
            if is_sign_up:
                self.user_signup()
    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login_window.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    # The main layout of the chat
    def layout(self, name):
        global themecolor_1, themecolor_2, themecolor_3

        themecolor_1 = "skyblue"
        themecolor_2 = "navy"
        themecolor_3 = "gold"

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg=themecolor_1)


        self.labelHead = Label(self.Window,
                               bg=themecolor_2,
                               fg=themecolor_3,
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)


        self.textCons = Text(self.Window,
                             width=20,
                             height=5,
                             bg=themecolor_1,
                             fg="black",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.735,
                            relwidth=1,
                            rely=0.05)

        self.labelBottom = Label(self.Window,
                                 bg=themecolor_2,
                                 height=100)

        self.labelBottom.place(relwidth=1,
                               rely=0.785)


        self.entryMsg = Entry(self.labelBottom,
                              bg=themecolor_1,
                              fg="#000000",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.03,
                            rely=0.035,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg=themecolor_1,
                                highlightbackground=themecolor_2,
                                command=lambda: self.sendButton(self.entryMsg.get()), relief = FLAT)

        self.buttonMsg.place(relx=0.77,
                             rely=0.035,
                             relheight=0.03,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        self.line3 = Label(self.Window,
                           width=450,
                           bg="#e8e6e6")

        self.line3.place(relwidth=1,
                         rely=0.861,
                         height = 5)

        self.buttonTheme = Button(self.Window,
                                 text="Theme",
                                 font="Helvetica 10 bold",
                                 width=20,
                                 bg=themecolor_1,
                                    highlightbackground=themecolor_2,
                                 command=lambda: self.theme(), relief = FLAT)

        self.buttonTheme.place(relx=0.49,
                              rely=0.795,
                              relheight=0.05,
                              relwidth=0.12)


        scrollbar = Scrollbar(self.textCons)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.textCons.yview, troughcolor=themecolor_1, highlightbackground=themecolor_1, highlightcolor=themecolor_1)
        self.textCons.config(yscrollcommand=scrollbar.set)
        self.textCons.config(state=DISABLED)


        self.poembutton= Button(self.Window,
                                text= 'Poem',
                                font= "Helvetica 10 bold",
                                width= 20,
                                bg= themecolor_1,
                                highlightbackground=themecolor_2,
                                command=lambda: self.ask_Poem(), relief = FLAT)
        self.poembutton.place(relx=0.845,
                              rely=0.795,
                              relheight=0.05,
                              relwidth=0.12)


        self.search_button= Button(self.Window,
                                   text='Search',
                                   font='Helvetica 10 bold',
                                   width=20,
                                   bg= themecolor_1,
                                      highlightbackground=themecolor_2,
                                   command= lambda: self.search_history(), relief = FLAT)
        self.search_button.place(relx=0.33,
                                 rely=0.795,
                                 relheight=0.05,
                                 relwidth=0.12)


        self.Game_button= Button(self.Window,
                                      text='Game',
                                      font='Helvetica 10 bold',
                                      width=50,
                                      bg= themecolor_1,
                                        highlightbackground=themecolor_2,
                                      command= lambda: self.game(), relief = FLAT)
        self.Game_button.place(relx=0.65,
                                    rely=0.795,
                                    relheight=0.05,
                                    relwidth=0.14)


        self.connect_who= StringVar()

        self.connect_entry= Entry(self.Window,textvariable= self.connect_who,
                                  width=8, bg='white', highlightbackground=themecolor_2, fg='black', font='Helvetica 10 bold')

        self.connect_entry.place(relx=0.16,
                                 rely=0.8,
                                 relheight=0.05,
                                 relwidth=0.14)

        self.connect_button= Button(self.Window,
                                    text='Connect',
                                    font='Helvetica 10 bold',
                                    width=20,
                                    bg= themecolor_1,
                                        highlightbackground=themecolor_2,
                                    command= lambda: self.sendButton('c '+self.connect_who.get()), relief = FLAT)
        self.connect_button.place(relx=0.02,
                                  rely=0.795,
                                  relheight=0.05,
                                  relwidth=0.12)

        self.disconnect_button= Button(self.Window,
                                       text='Leave',
                                       font='Helvetica 10 bold',
                                       width=20,
                                       bg= themecolor_1,
                                        highlightbackground=themecolor_2,
                                       command= lambda: self.quit(), relief = FLAT)
        self.disconnect_button.place(relx=0,
                                     rely=0,
                                     relheight=0.05,
                                     relwidth=0.12)

    def theme(self):
        def get_color():
            color_1 = hex(random.randint(16, 255))
            color_2 = hex(random.randint(16, 255))
            color_3 = hex(random.randint(16, 255))
            color = '#' +   color_1[2:] + color_2[2:] + color_3[2:]
            return color

        global themecolor_1
        global themecolor_2
        themecolor_1 = get_color()
        themecolor_2 = get_color()


        self.Window.config(bg=themecolor_1)
        self.textCons.config(bg=themecolor_1)
        self.labelBottom.config(bg=themecolor_2)
        self.buttonMsg.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.buttonTheme.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.line3.config(bg=themecolor_1)
        self.poembutton.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.search_button.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.Game_button.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.connect_entry.config(highlightbackground=themecolor_2)
        self.connect_button.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.disconnect_button.config(bg=themecolor_1, highlightbackground=themecolor_2)
        self.entryMsg.config(highlightbackground=themecolor_2, bg=themecolor_1)
        self.labelHead.config(bg=themecolor_2)

    def ask_Poem(self):

        def getpoem(p):
            self.poem_text= self.sonnet.get_poem(p)
            self.poem_text = '\n'.join(self.poem_text).strip()
            self.get_window= Toplevel()
            self.get_window.geometry('335x500')
            self.get_window.title('Sonnet'+ str(p))
            self.text= Text(self.get_window,width=40,
                            height=40,
                            bg=themecolor_1,
                            fg='black',
                            font="Helvetica 14",
                            padx=5,
                            pady=5)
            self.text.place(x=0, y=0)
            if len(self.poem_text)>0:
                self.text.insert(INSERT, self.poem_text)
            else:
                self.text.insert(INSERT, 'No such Sonnet!')

            self.poem.destroy()


        self.poem= Toplevel()
        self.poem.geometry('300x150')
        self.poem.title('Shakespear')
        self.poem.config(bg=themecolor_1)
        self.poem_label= Label(self.poem,
                               text='Which sonnet do you want?', bg = themecolor_1, highlightbackground=themecolor_1).place(x=70, y=20)
        self.poemnumber= StringVar()
        self.poem_entry= Entry(self.poem,textvariable= self.poemnumber,
                               width=8, bg=themecolor_1, highlightbackground=themecolor_2).place(x=100, y=60)
        self.poem_button= Button(self.poem, text='Enter',
                                 command=lambda: getpoem(int(self.poemnumber.get())), bg=themecolor_2, highlightbackground=themecolor_1)
        self.poem_button.place(x=200, y=58)

    def search_history(self):
        if self.sm.state == S_CHATTING:
            self.sendButton('bye')
        self.search_window = Toplevel()
        self.search_window.geometry("400x100")
        self.search_window.title("search for chat history")
        self.search_window.config(bg=themecolor_1)
        # create a Label
        self.key_word = Label(self.search_window, text='Key word: ', bg = themecolor_1).place(x=40, y=33)
        self.var_key_word = StringVar()
        self.entry_key_word = Entry(self.search_window, textvariable=self.var_key_word, bg = themecolor_1, highlightbackground=themecolor_2)
        self.entry_key_word.place(x=110, y=30)

        self.var_result = StringVar()

        self.enter = Button(self.search_window, text="enter", font="Helvetica 10 bold", width=4, fg="black", command=lambda : self.sendButton("? "+self.var_key_word.get()), bg = themecolor_2, highlightbackground=themecolor_1)
        self.enter.place(x=310, y=33)



    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)




    def game(self):
        self.my_msg = "request_to_start_a_game"


    def game_layout(self):
        self.gameWindow = Toplevel(self.Window)
        self.gameWindow.title(f'GoBang for {self.name}')
        Label(self.gameWindow, text="player1 : X", font="times 15").grid(row=0, column=1)
        Label(self.gameWindow, text="player2 : O", font="times 15").grid(row=0, column=2)

        self.buttons = []
        for i in range(400):
            button = Button(self.gameWindow, width=1, height=1, font=('Times 16 bold'),
                            command=lambda i=i: self.checker(i))
            button.grid(row=1 + i // 20, column=1 + i % 20)
            self.buttons.append(button)

    def checker(self, index):
        self.my_msg = f"press_button_{index + 1}"

    def proc(self):
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []

            if self.socket in read:
                peer_msg = self.recv()

            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)

                if self.system_msg == "[Server]: Enjoy the game!":
                    self.game_layout()
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, self.system_msg + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)

#                elif self.system_msg.startswith("systeminfo"):
#                    button_index = int(self.system_msg[10]) - 1
#                    button_text = self.system_msg[11:]
#                    self.buttons[button_index].config(text=button_text)

                elif self.system_msg.startswith("systeminfo"):
                    if self.system_msg[11] == "X" or self.system_msg[11] == "O":
                        button_index = int(self.system_msg[10]) - 1
                        button_text = self.system_msg[11:]
                        self.buttons[button_index].config(text=button_text)
                    elif self.system_msg[12] == "X" or self.system_msg[12] == "O":
                        button_index = int(self.system_msg[10]+self.system_msg[11]) - 1
                        button_text = self.system_msg[12:]
                        self.buttons[button_index].config(text=button_text)
                    elif self.system_msg[13] == "X" or self.system_msg[13] == "O":
                        button_index = int(self.system_msg[10]+self.system_msg[11]+self.system_msg[12]) - 1
                        button_text = self.system_msg[13:]
                        self.buttons[button_index].config(text=button_text)

                elif self.system_msg.startswith("serverinfo"):
                    result = self.system_msg[10:]
                    if result in ["Player 1", "Player 2"]:
                        messagebox.showinfo(title="Result", message=f"{result} wins!")
                    elif result == "draw":
                        messagebox.showinfo(title="Result", message="Draw!")
                    self.gameWindow.destroy()


                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END, self.system_msg + "\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)

                self.my_msg = ''


    def run(self):
        self.login()

    def quit(self):
        self.sendButton('q')
        self.socket.close()
        self.Window.destroy()





# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
