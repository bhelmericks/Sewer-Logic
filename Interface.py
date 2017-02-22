import tkinter as tk   # python3
#import Tkinter as tk   # python

TITLE_FONT = ("Helvetica", 18, "bold")

class Interface(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Create base frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.buttons = {} #Dictionary to find navigation button objects from page names

        #Create main navigation buttons
        self.homeownerButton = tk.Button(container, text="Homeowner", command=lambda: self.show_frame(Homeowner))
        self.buttons[Homeowner] = self.homeownerButton #Add to navigation button dictionary
        self.homeownerButton.place(x=0, y=440, width=400, height=40)
        self.advUsrButton = tk.Button(container, text="Advanced User", command=lambda: self.show_frame(AdvUser))
        self.buttons[AdvUser] = self.advUsrButton #Add to navigation button dictionary
        self.advUsrButton.place(x=400, y=440, width=400, height=40)

        self.frames = {} #Dictionary to find frame objects from page names

        #Create large frames (Homeowner AdvUser)
        for F in (AdvUser, Homeowner):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, width=800, height=440)

        #Create small frames (Option, PowerAndTemp, ...)
        for F in (Option, PowerAndTemp, FlowAndPressure, WaterLevel, SystemStatus):
            frame = F(self.frames[AdvUser], self)
            self.frames[F] = frame
            frame.place(x=0, y=40, width=800, height=400)

        self.show_frame(Homeowner) #Show default frame

    #Bring selected frame to the front and enable/disable relevant buttons
    def show_frame(self, page_name):
        self.frames[page_name].tkraise() #Raise frame to top
        if page_name == Homeowner:
            self.buttons[AdvUser].config(state="normal") #If Homeowner is selected reenable advUserButton
        elif page_name == AdvUser:
            self.buttons[Homeowner].config(state="normal") #If AdvUser is selected reenable homeownerButton
        else:
            for F in (Option, PowerAndTemp, FlowAndPressure, WaterLevel, SystemStatus):
                if page_name != F:
                    self.buttons[F].config(state="normal") #Enable unselected AdvUser buttons
        self.buttons[page_name].config(state="disabled") #Disable selected button

class Homeowner(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Homeowner Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

class AdvUser(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        controller = controller

        #Create AdvUser navigation buttons
        optionButton = tk.Button(self, text="Options", command=lambda: controller.show_frame(Option))
        controller.buttons[Option] = optionButton #Add to navigation button dictionary
        optionButton.place(x=640, y=0, width=160, height=40)

        tempButton = tk.Button(self, text="Power and Temperature", command=lambda: controller.show_frame(PowerAndTemp))
        controller.buttons[PowerAndTemp] = tempButton #Add to navigation button dictionary
        tempButton.place(x=480, y=0, width=160, height=40)

        flowButton = tk.Button(self, text="Flow and Pressure", command=lambda: controller.show_frame(FlowAndPressure))
        controller.buttons[FlowAndPressure] = flowButton #Add to navigation button dictionary
        flowButton.place(x=320, y=0, width=160, height=40)

        waterButton = tk.Button(self, text="Water Level", command=lambda: controller.show_frame(WaterLevel))
        controller.buttons[WaterLevel] = waterButton #Add to navigation button dictionary
        waterButton.place(x=160, y=0, width=160, height=40)

        statusButton = tk.Button(self, text="System Status", command=lambda: controller.show_frame(SystemStatus))
        statusButton.config(state="disabled") #statusButton is selected by default
        controller.buttons[SystemStatus] = statusButton #Add to navigation button dictionary
        statusButton.place(x=0, y=0, width=160, height=40)

class Option(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Options Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        #Button to quit application
        quitButton = tk.Button(self, text="Quit", command=lambda: app.quit())
        quitButton.pack()

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
    app = Interface() #Create application
    app.wm_title("Interface") #Set application title
    #app.overrideredirect(1) #Force fullscreen, uncomment line when running on Raspberry Pi
    app.resizable(width=False, height=False) #Disable application window resizing
    app.geometry('{}x{}'.format(800, 480)) #Set application window size
    app.mainloop()
