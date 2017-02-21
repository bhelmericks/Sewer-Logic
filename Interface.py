import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        advUsrFrame = tk.Frame(self, bg="grey")
        advUsrFrame.place(x=0, y=0, width=800, height=440)

        statusButton = tk.Button(advUsrFrame, text="System Status")
        statusButton.place(x=0, y=0, width=200, height=40)

        waterButton = tk.Button(advUsrFrame, text="Water Levels")
        waterButton.place(x=200, y=0, width=200, height=40)

        flowButton = tk.Button(advUsrFrame, text="Pressure and Flow")
        flowButton.place(x=400, y=0, width=200, height=40)

        tempButton = tk.Button(advUsrFrame, text="Power and Temperature")
        tempButton.place(x=600, y=0, width=200, height=40)

        homeOwnerFrame = tk.Frame(self, bg="grey")
        homeOwnerFrame.place(x=0, y=0, width=800, height=440)

        homeOwnerButton = tk.Button(self, text="Homeowner", command=lambda: homeOwnerFrame.tkraise())
        homeOwnerButton.place(x=0, y=440, width=400, height=40)

        advUsrButton = tk.Button(self, text="Advanced User", command=lambda: advUsrFrame.tkraise())
        advUsrButton.place(x=400, y=440, width=400, height=40)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.wm_title("Interface")
    root.resizable(width=False, height=False) #Disable window resizing
    root.geometry('{}x{}'.format(800, 480)) #Set window size
    root.mainloop()
