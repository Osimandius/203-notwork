import socket
from threading import Thread
from tkinter import *

# nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        
        self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
        self.pls.place( relheight = 0.15,
                        relx = 0.2,
                        rely = 0.07)

        self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
        self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)

        self.entryName = Entry(self.login,
							font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
        self.entryName.focus()
        self.go=Button(self.login,text="BUTTON.",font="Helvetica 14 bold",command=lambda:self.goahead(self.entryName.get()))
        self.go.place(relx=0.4,rely=0.5)
        self.Window.mainloop()
    
    def goahead(self,name):
        self.login.destroy()
        #self.name=name
        self.layout(name)
        r=Thread(target=self.received)
        r.start()
    
    # personalised window for every user
    def layout(self,name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("SPEAK")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550 , bg="#702963")
        self.labelHead = Label(self.Window , bg= "#702963", 
        fg="#FFC300", text = self.name, font="Helvetica 14 bold" , pady = 5 )
        self.labelHead.place(relwidth= 1)
        self.line = Label(self.Window , width = 450 , bg="#5ddaff")
        self.line.place(relwidth=1, rely = 0.07 , relheight=0.012)
        self.textCons = Text(self.Window , width=20 , height =2 
                             ,bg="#17202A", fg="#EAECEE", font="Helvetica 14",
                             padx=5 , pady = 5)
        self.textCons.place(relheight= 0.745 , relwidth=1 , rely = 0.08)
        self.labelBott=Label(self.Window, bg="#9275EC",height=80)
        self.labelBott.place(relwidth=1,rely=0.825)
        self.entryMsg=Entry(self.labelBott,bg="#2c3e50",fg="#EEEEEE",font="Helvetica 15")
        self.entryMsg.place(relwidth=0.7,relheight=0.06,rely=0.008,relx=0.01)
        self.entryMsg.focus()
        self.buttonMsg=Button(self.labelBott,text="BUTTON.",font="ComicSansMS 10 bold",
                              width=20,bg="#AaAaAa",command=lambda:self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,rely=0.008,relheight=0.06,relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrolly=Scrollbar(self.textCons)
        scrolly.place(relheight=1,relx=0.974)
        scrolly.config(command=self.textCons.yview)
        self.textCons.config(status=DISABLED)
        #self.Window.mainloop()
        
    def sendButton(self,msg):
        self.textCons.config(status=DISABLED)
        self.msg=msg
        self.entryMsg.delete(0,END)
        s=Thread(target=self.write)
        s.start()

    def show_message(self,msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,msg+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def received(self):
     while True:
         try:
             message = client.recv(2048).decode('utf-8')
             if message == 'NICKNAME':
                 client.send(self.name.encode('utf-8'))
             else:
                 self.show_message(message)
         except:
             print("An error occured!")
             client.close()
             break
         
    def write(self): 
        self.textCons.config(state=DISABLED) 
        while True: 
            message = (f"{self.name}: {self.msg}") 
            client.send(message.encode('utf-8')) 
            self.show_message(message) 
            break
g = GUI()
