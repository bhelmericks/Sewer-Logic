import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        homeOwnerButton = tk.Button(self, text="Homeowner", command=lambda: homeOwnerFrame.tkraise())
        homeOwnerButton.place(x=0, y=440, width=400, height=40)
        advUsrButton = tk.Button(self, text="Advanced User", command=lambda: advUsrFrame.tkraise())
        advUsrButton.place(x=400, y=440, width=400, height=40)

        advUsrFrame = tk.Frame(self)
        advUsrFrame.place(x=0, y=0, width=800, height=440)

        tempButton = tk.Button(advUsrFrame, text="Power and Temperature", command=lambda: advUsrTempFrame.tkraise())
        tempButton.place(x=600, y=0, width=200, height=40)
        advUsrTempFrame = tk.Frame(advUsrFrame, bg="yellow")
        advUsrTempFrame.place(x=0, y=40, width=800, height=400)

        flowButton = tk.Button(advUsrFrame, text="Pressure and Flow", command=lambda: advUsrFlowFrame.tkraise())
        flowButton.place(x=400, y=0, width=200, height=40)
        advUsrFlowFrame = tk.Frame(advUsrFrame, bg="red")
        advUsrFlowFrame.place(x=00, y=40, width=800, height=400)

        waterButton = tk.Button(advUsrFrame, text="Water Levels", command=lambda: advUsrWaterFrame.tkraise())
        waterButton.place(x=200, y=0, width=200, height=40)
        advUsrWaterFrame = tk.Frame(advUsrFrame, bg="green")
        advUsrWaterFrame.place(x=00, y=40, width=800, height=400)

        statusButton = tk.Button(advUsrFrame, text="System Status", command=lambda: advUsrStatusFrame.tkraise())
        statusButton.place(x=0, y=0, width=200, height=40)
        advUsrStatusFrame = tk.Frame(advUsrFrame, bg="blue")
        advUsrStatusFrame.place(x=00, y=40, width=800, height=400)

        homeOwnerFrame = tk.Frame(self)
        homeOwnerFrame.place(x=0, y=0, width=800, height=440)
        quitButton = tk.Button(homeOwnerFrame, text="Quit", command=lambda: root.destroy())
        quitButton.pack()

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.wm_title("Interface")
    #root.overrideredirect(1) #Force fullscreen
    root.resizable(width=False, height=False) #Disable window resizing
    root.geometry('{}x{}'.format(800, 480)) #Set window size
    root.mainloop()
