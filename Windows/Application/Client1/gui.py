import tkinter as tk
from tkinter.filedialog import askopenfilename
from client import Client

class Application(Client):
    def __init__(self, root, server_ip, server_port, client_ip, client_port):
        self.root = root
        super().__init__(server_ip, server_port)
        self.client_ip = client_ip
        self.client_port = client_port
        self.mainframe1 = None
        self.mainframe2 = None
        self.mainframe3 = None
        self.mainframe4 = None
        self.id_object = None
        self.id = None
        self.password_object = None
        self.Password = None
        self.filename = None
        self.recvd_output = None

    @staticmethod
    def disableFrame(frame):
        for child in frame.winfo_children():
            child.configure(state='disable')

    def getFrame1Inputs(self):
        self.id = self.id_object.get()
        self.password = self.password_object.get()
        self.disableFrame(self.mainframe1)

        if(self.login(self.id, self.password) == True):       
            self.mainframe1.destroy()
            self.mainframe1 = None
            self.frame2()
        else:
            #destroy current frame
            self.mainframe1.destroy()
            self.mainframe1 = None
            self.frame1(True)

    #WELCOME MENU
    def frame1(self, login_fail=False):
        self.mainframe1 = tk.Frame(self.root)
        self.mainframe1.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.S, tk.E))
        self.mainframe1.grid_rowconfigure(0, weight=1)
        self.mainframe1.grid_columnconfigure(0, weight=1)

        tk.Label(self.mainframe1, text='IDLE', font=("Verdana", 64), fg='#%02x%02x%02x'%(0, 128, 128)).grid(column=0, row=0, sticky='nw')
        
        if (login_fail == True):
            tk.Label(self.mainframe1, text='Login Credentials Incorrect', font=("Verdana", 12), fg='red').grid(column=0, row=1, sticky=tk.W)
        else:
            tk.Label(self.mainframe1, text='Welcome', font=("Verdana", 24)).grid(column=0, row=1, sticky=tk.W)
            
        tk.Label(self.mainframe1, text='ID', font=("Verdana", 14)).grid(column=0, row=2, sticky=tk.W)
        
        self.id_object = tk.StringVar()
        id_entry = tk.Entry(self.mainframe1, width=35, textvariable=self.id_object)
        id_entry.grid(column=2, row=2, sticky=tk.E)
        id_entry.focus()

        tk.Label(self.mainframe1, text='Password', font=('Verdana', 14)).grid(column=0, row=3, sticky=tk.W)

        self.password_object=tk.StringVar()
        password_entry = tk.Entry(self.mainframe1, width=35, textvariable=self.password_object)
        password_entry.grid(column=2, row=3, sticky=tk.E)
        password_entry.focus()

        tk.Button(self.mainframe1, text='Login', command=self.getFrame1Inputs, bg='grey', width=15).grid(column=2, row=4, sticky='nsew')
        tk.Button(self.mainframe1, text='Exit', command=lambda: self.root.destroy(), bg='#%02x%02x%02x'%(0, 170, 0), width=12).grid(column=1, row=4, sticky='nsew')

        for child in self.mainframe1.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def manageFrame2Inputs(self, choice):
        self.disableFrame(self.mainframe2)
        if choice == 'Run Scripts':
            self.mainframe2.destroy()
            self.mainframe2 = None    
            self.frame3()
            print("Chosen Run Scripts")
        elif choice == 'Become IDLEr':
            self.mainframe2.destroy()
            self.mainframe2 = None    
            self.frame4()
            print("Chosen Become IDLEr")
        elif choice == 'Logout':
            self.logout()
            self.mainframe2.destroy()
            self.mainframe2 = None    
            self.frame1()

    #CHOOSING ROLE 
    def frame2(self):
        self.mainframe2 = tk.Frame(self.root)
        self.mainframe2.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.S, tk.E))
        self.mainframe2.rowconfigure(0, weight=1)
        self.mainframe2.grid_columnconfigure(0, weight=1)

        tk.Label(self.mainframe2, text='IDLE', font=("Verdana", 64), fg='#%02x%02x%02x'%(0, 128, 128)).grid(column=0, row=0, sticky='nw')

        tk.Button(self.mainframe2, text='Run Scripts', font=("Verdana", 14), command=lambda: self.manageFrame2Inputs('Run Scripts')).grid(column=0, row=1, sticky='w')

        tk.Button(self.mainframe2, text='Become IDLEr', font=("Verdana", 14), command=lambda: self.manageFrame2Inputs("Become IDLEr")).grid(column=2, row=1, sticky='e')

        tk.Button(self.mainframe2, text='Logout', font=("Verdana", 14), command=lambda: self.manageFrame2Inputs("Logout")).grid(column=1, row=1, sticky='ns')

        for child in self.mainframe2.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def manageFrame3Inputs(self, output):
        self.disableFrame(self.mainframe3)
        if output == 0: #0 for first output of frame i.e after getting filename
            print(self.filename)
            self.recvd_output = self.runScript(self.filename)
            self.mainframe3.destroy()
            self.mainframe3 = None
            self.frame3(True)
        elif output == 1: #1 for showing output
            self.mainframe3.destroy()
            self.mainframe3 = None
            self.frame3()
        elif output == 2: #2 to go t0 frame 2
            self.mainframe3.destroy()
            self.mainframe3 = None
            self.frame2()

    def askforfile(self):
        self.filename = askopenfilename()
        self.manageFrame3Inputs(0)

    #RUNNING SCRIPTS
    def frame3(self, output=False):
        self.mainframe3=tk.Frame(self.root)
        self.mainframe3.grid(column=0, row=0)
        self.mainframe3.rowconfigure(0, weight=1)
        self.mainframe3.grid_columnconfigure(0, weight=1)

        tk.Label(self.mainframe2, text='IDLE', font=("Verdana", 64), fg='#%02x%02x%02x'%(0, 128, 128)).grid(column=0, row=0, sticky='nw')
        
        if output == False:       
            tk.Button(self.mainframe3, text="Go Back", font=("Verdana", 14), command=lambda: self.manageFrame3Inputs(2), bg='#%02x%02x%02x'%(0, 255, 128)).grid(column=0, row=1, stick='nsw')
            tk.Button(self.mainframe3, text="Choose File To Execute", font=("Verdana", 14), command=self.askforfile, bg='#%02x%02x%02x'%(255, 192, 88)).grid(column=0, row=0, stick='nws')

        elif output == True:
            tk.Label(self.mainframe3, text="OUTPUT:", font=("Verdana", 14)).grid(column=0, row=1)
            tk.Label(self.mainframe3, text=self.recvd_output, font=("Verdana", 14)).grid(column=1, row=2)

            tk.Button(self.mainframe3, text="Go Back", font=("Verdana", 14), command=lambda: self.manageFrame3Inputs(1), bg='#%02x%02x%02x'%(0, 255, 128)).grid(column=0, row=3, stick='nswe')

        for child in self.mainframe3.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def manageFrame4Inputs(self):
        self.disableFrame(self.mainframe4)
        self.withdrawBeingIdler()
        self.mainframe4.destroy()
        self.mainframe4=None
        self.frame2()

    #IDLEr, FOR LENDING COMPUTATION POWER
    def frame4(self):
        self.mainframe4=tk.Frame(self.root)
        self.mainframe4.grid(column=0, row=0)
        self.mainframe4.rowconfigure(0, weight=1)
        self.mainframe4.grid_columnconfigure(0, weight=1)
        self.becomeIdler(self.client_ip, self.client_port)
        tk.Label(self.mainframe4, text='Amazing! Now Enjoy While You Help Others :)', font=("Verdana", 14)).grid(column=1, row=0, sticky='we')
        tk.Button(self.mainframe4, text="Go Back", font=("Verdana", 14), command=self.manageFrame4Inputs, bg='#%02x%02x%02x'%(255, 192, 88)).grid(column=1, row=3, stick='sw')
        for child in self.mainframe4.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def run(self):
        self.frame1()

root = tk.Tk()
root.title('IDLE v1.0')
root.configure(bg='white')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.geometry('{}x{}'.format(1280, 720))
root.minsize(720, 480)
root.maxsize(720, 480)

Application(root, "127.0.0.1", 8001, "127.0.0.1", 9001).run()
root.mainloop()
