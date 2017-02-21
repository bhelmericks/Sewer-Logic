import tkinter as tk   # python3
#import Tkinter as tk   # python

TITLE_FONT = ("Helvetica", 18, "bold")

class Interface(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Create base frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        #
        homeOwnerButton = tk.Button(container, text="Homeowner", command=lambda: self.show_frame(Homeowner))
        homeOwnerButton.place(x=0, y=440, width=400, height=40)
        advUsrButton = tk.Button(container, text="Advanced User", command=lambda: self.show_frame(AdvUser))
        advUsrButton.place(x=400, y=440, width=400, height=40)

        #Create large frames
        self.frames = {}
        for F in (AdvUser, HomeOwner):
            frame = F(frames[AdvUser], self)
            self.frames[F] = frame
            frame.place(x=0, y=40, width=800, height=440)

        #Create small frames
        for F in (Option, PowerAndTemp, FlowAndPressure, WaterLevel, SystemStatus):
            frame = F(frames[AdvUser], self)
            self.frames[F] = frame
            frame.place(x=0, y=40, width=800, height=400)

        self.show_frame(Homeowner) #Show default frame

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Homeowner(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Homeowner Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

class AdvUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        optionButton = tk.Button(self, text="Options", command=lambda: controller.show_frame(Option))
        optionButton.place(x=640, y=0, width=160, height=40)

        tempButton = tk.Button(self, text="Power and Temperature", command=lambda: controller.show_frame(PowerAndTemp))
        tempButton.place(x=480, y=0, width=160, height=40)

        flowButton = tk.Button(self, text="Flow and Pressure", command=lambda: controller.show_frame(FlowAndPressure))
        flowButton.place(x=320, y=0, width=160, height=40)

        waterButton = tk.Button(self, text="Water Level", command=lambda: controller.show_frame(WaterLevel))
        waterButton.place(x=160, y=0, width=160, height=40)

        statusButton = tk.Button(self, text="System Status", command=lambda: controller.show_frame(SystemStatus))
        statusButton.place(x=0, y=0, width=160, height=40)

class Option(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Options Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

class PowerAndTemp(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Power and Temperatures Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

class FlowAndPressure(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Flow and Pressure Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

class WaterLevel(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Water Levels Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

class SystemStatus(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="System Status Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

if __name__ == "__main__":
    app = Interface()
    app.wm_title("Interface")
    #app.overrideredirect(1) #Force fullscreen
    app.resizable(width=False, height=False) #Disable window resizing
    app.geometry('{}x{}'.format(800, 480)) #Set window size
    app.mainloop()
