"""Blah blah blah."""
import os.path
import schedule
import serial
import threading
import time
#import tkinter as tk   # python3
import Tkinter as tk   # python


TITLE_FONT = ("Helvetica", 18, "bold")
BUTTON_FONT = ("Helvetica", 14)
NOTIFICATION_FONT = ("Helvetica", 14)


class Interface(tk.Tk):
    """Interface GUI."""

    def __init__(self):
        """Blah blah blah."""
        tk.Tk.__init__(self)

        # Force fullscreen, uncomment on Raspberry Pi
        # self.overrideredirect(1)
        # Hide mouse pointer, uncomment on Raspberry Pi
        # self.config(cursor="none")
        self.wm_title("Interface")  # Set application title
        self.resizable(width=False, height=False)  # Disable window resizing
        self.geometry('{}x{}'.format(800, 480))  # Set window size

        # Create base frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Dictionary to find navigation button objects from page names
        self.buttons = {}
        # Create homeowner button
        self.homeownerButton = tk.Button(container, text="Homeowner",
                                         font=BUTTON_FONT, command=lambda:
                                         self.show_frame(Homeowner))
        # Add homeowner button navigation button dictionary
        self.buttons[Homeowner] = self.homeownerButton
        self.homeownerButton.place(x=0, y=430, width=400, height=50)
        # Create advanced user button
        self.advUsrButton = tk.Button(container, text="Advanced User",
                                      font=BUTTON_FONT, command=lambda:
                                      self.show_frame(AdvUser))
        # Add advanced usre button navigation button dictionary
        self.buttons[AdvUser] = self.advUsrButton
        self.advUsrButton.place(x=400, y=430, width=400, height=50)

        self.frames = {}  # Dictionary to find frame objects from page names

        # Create large frames (Homeowner AdvUser)
        for F in (AdvUser, Homeowner):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(x=0, y=0, width=800, height=430)

        # Create small frames (Option, PowerAndTemp, ...)
        for F in (Option, PowerAndTemp, FlowAndPressure,
                  WaterLevel, SystemStatus):
            frame = F(self.frames[AdvUser], self)
            self.frames[F] = frame
            frame.place(x=0, y=50, width=800, height=380)

        self.show_frame(Homeowner)  # Show default frame

    # Bring selected frame to the front and enable/disable relevant buttons
    def show_frame(self, page_name):
        """Blah blah blah."""
        self.frames[page_name].tkraise()  # Raise frame to top
        if page_name == Homeowner:
            # If Homeowner is selected reenable advUserButton
            self.buttons[AdvUser].config(state="normal")
        elif page_name == AdvUser:
            # If AdvUser is selected reenable homeownerButton
            self.buttons[Homeowner].config(state="normal")
        else:
            for F in (Option, PowerAndTemp, FlowAndPressure,
                      WaterLevel, SystemStatus):
                if page_name != F:
                    # Enable unselected AdvUser buttons
                    self.buttons[F].config(state="normal")
        # Disable selected button
        self.buttons[page_name].config(state="disabled")


class Homeowner(tk.Frame):
    """Homeowner frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="Homeowner Frame", font=TITLE_FONT)
        # label.pack(side="top", fill="x", pady=10)
        #find a way to make nowAsString retain value
        nowAsString = time.strftime('%H:%M %m/%d/%Y')
        washTank =  nowAsString+ ' NOTICE: add 1 gallon to Wash Tank'
        wasteTank = nowAsString + ' NOTICE: Waste Tank needs to be Emptied'
        renderer = Renderer(self, 800, 430)
        #logic to force into true values needed
        renderer.drawFlag(self, 10, 30, 15, 'blue', 'green', washTank)
        renderer.drawFlag(self, 10, 70, 15, 'yellow', 'green', wasteTank)
        renderer.drawFlag(self, 30, 150, 25, 'red', 'green', 'ERROR: Maintence Required')
        # display water levels on Homeowner page
        renderer.drawTank(self, 360, 195, 80, 0.3, "Wash")
        renderer.drawTank(self, 470, 195, 80, 0.5, "Grey")
        renderer.drawTank(self, 580, 195+80, 40, 0.1, "Waste")

class AdvUser(tk.Frame):
    """Advanced user frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        controller = controller

        # Create AdvUser navigation buttons
        optionButton = tk.Button(self, text="Options",
                                 font=BUTTON_FONT, command=lambda:
                                 controller.show_frame(Option))
        # Add to navigation button dictionary
        controller.buttons[Option] = optionButton
        optionButton.place(x=640, y=0, width=160, height=50)

        tempButton = tk.Button(self, text="Power and \n Temperature",
                               font=BUTTON_FONT, command=lambda:
                               controller.show_frame(PowerAndTemp))
        # Add to navigation button dictionary
        controller.buttons[PowerAndTemp] = tempButton
        tempButton.place(x=480, y=0, width=160, height=50)

        flowButton = tk.Button(self, text="Flow and \n Pressure",
                               font=BUTTON_FONT, command=lambda:
                               controller.show_frame(FlowAndPressure))
        # Add to navigation button dictionary
        controller.buttons[FlowAndPressure] = flowButton
        flowButton.place(x=320, y=0, width=160, height=50)

        waterButton = tk.Button(self, text="Water Level",
                                font=BUTTON_FONT, command=lambda:
                                controller.show_frame(WaterLevel))
        # Add to navigation button dictionary
        controller.buttons[WaterLevel] = waterButton
        waterButton.place(x=160, y=0, width=160, height=50)

        statusButton = tk.Button(self, text="System Status",
                                 font=BUTTON_FONT, command=lambda:
                                 controller.show_frame(SystemStatus))
        # statusButton is selected by default
        statusButton.config(state="disabled")
        # Add to navigation button dictionary
        controller.buttons[SystemStatus] = statusButton
        statusButton.place(x=0, y=0, width=160, height=50)


class Option(tk.Frame):
    """Options frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Options Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        # Button to quit application
        quitButton = tk.Button(self, text="Quit", command=lambda: app.quit())
        quitButton.pack()


class PowerAndTemp(tk.Frame):
    """Power and temperatures frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Power and Temperatures Frame",
                         font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        renderer = Renderer(self, 800, 380)
        fullLine = 'Temperature'
        renderer.drawDataOutput(self, 40, 50, fullLine)
        fullLine = 'Power'
        renderer.drawDataOutput(self, 340, 50, fullLine)
        for x in range(0, 3):
            numberIn = x * (2 + x) + 20 + 0.5 - (0.2 * x)
            if x is 0:
                fullLine = 'Outside' + ':  ' + str(numberIn) + '  ' + 'F'
            elif x is 1:
                fullLine = 'AC Panel' + ':  ' + str(numberIn) + '  ' + 'F'
            else:
                fullLine = 'DC Panel' + ':  ' + str(numberIn) + '  ' + 'F'
            renderer.drawDataOutput(self, 20, x * 40 + 100, fullLine)
            numberIn = x * (2 + x) + 90
            if x < 2:
                fullLine = str(x) + ':  ' + str(numberIn) + '  ' + 'Watts'
            else:
                fullLine = 'Total Power' + ':  ' + str(numberIn) + '  ' + 'Watts'
                numberIn = (x-1 * (2 + x-1) + 90)+(x-1 * (2 + x-1) + 90)
            renderer.drawDataOutput(self, 320, x * 40 + 100, fullLine)

class FlowAndPressure(tk.Frame):
    """Flows and pressures frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Flow and Pressure Frame",
                         font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        renderer = Renderer(self, 800, 380)
        fullLine='Pressure'
        renderer.drawDataOutput(self, 40, 50,fullLine)
        fullLine='Flow'
        renderer.drawDataOutput(self, 340, 50, fullLine)
        for x in range (0,5):
            numberIn=x*(2+x)+20+0.532-(0.1*x)
            fullLine=str(x)+':  '+str(numberIn)+'  '+'psi'
            renderer.drawDataOutput(self, 20, x*40+100, fullLine)
            numberIn = x * (2 + x) + 50+0.932-(0.1*x)
            fullLine = str(x) + ':  ' + str(numberIn) + '  ' + 'm^3/sec'
            renderer.drawDataOutput(self, 320, x*40+100, fullLine)

class WaterLevel(tk.Frame):
    """Water levels frame."""
    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        renderer = Renderer(self, 800, 380)
        renderer.drawTank(self, 50, 95, 80, 0.3, "Wash")
        renderer.drawTank(self, 200, 95, 80, 0.5, "Grey")
        renderer.drawTank(self, 350, 95, 80, 1, "NF Feed")
        renderer.drawTank(self, 500, 95, 80, 1, "RO Feed")
        renderer.drawTank(self, 650, 95+80, 40, 0.1, "Waste")


class SystemStatus(tk.Frame):
    """System status frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="System Status Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        renderer = Renderer(self, 800, 430)
        # logic to force into true values needed
        valvePosition = []
        valveLabel = []
        for x in range (0, 8):
            # correct valve on/off logic
            if x > 3:
                xposition = 170
                yposition = yposition = 30+40*(x-4)
            else:
                xposition = 10
                yposition = 30 + 40 * x
            if x is 4 or x is 7 or x is 2:
                valvePosition.append('ON')
            else:
                valvePosition.append('OFF')
            valveLabel.append(' ')
            valveLabel[x] = ' ' + str(x + 1) + ' ' + valvePosition [x]
            if valvePosition[x] is'ON':
                renderer.drawFlag(self, xposition, yposition, 15, 'green', 'green', valveLabel[x])
            else:
                renderer.drawFlag(self, xposition, yposition, 15, 'red', 'green', valveLabel[x])
        #insert two variable valves
        yposition = 30
        color = 'green'
        relay = []
        relay.append('Bubbler')
        relay.append('UV')
        relay.append('Ozone')
        relay.append('Ozone Pump')
        relay.append('High Pressure Pump')
        for x in range (0,5):
            renderer.drawRelay(self, 600, yposition, 50, color, relay[x])
            yposition = yposition+60

class Renderer(tk.Canvas):
    """Renderer used to draw GUI objects."""

    def __init__(self, parent, width, height):
        """."""
        tk.Canvas.__init__(self, parent)
        self.place(x=0, y=0, width=width, height=height)

    def drawFlag(self, controller, x, y, size, color0, color1, name):
        """Draw a circle flag object with a label to the right."""
        self.create_oval(x+4, y+4, x+size+4, y+size+4, width=2, fill=color0)
        label = tk.Label(controller, text=name, font=NOTIFICATION_FONT)
        label.place(x=x+size+5, y=y+4, height=size)

    def drawTank(self, controller, x, y, size, fill, name):
        """Draw a tank GUI object with a label below and # gallons above."""
        sizeLabel=size
        size=size*2
        self.create_rectangle(x, y, x+100, y+size, width=3, fill='grey')
        self.create_rectangle(x+2, y-fill*(size-3)+size-1, x+99, y+size-1,
                              width=0, fill='blue')
        gals = tk.Label(controller, text=str(int(sizeLabel*fill))+'/'+str(sizeLabel)
                        + 'gal', font=NOTIFICATION_FONT)
        gals.place(x=x, y=y-20, width=100, height=20)
        label = tk.Label(controller, text=name, font=TITLE_FONT)
        label.place(x=x, y=y+size+10, width=100, height=40)

    def drawRelay(self, controller, x, y, size, color, name):
        """Draw a button for relays with label to the left"""
        self.create_rectangle(x, y, x + 100, y + size, width=3, fill=color)
        relayLabel = tk.Label(controller, text=name, font=NOTIFICATION_FONT)
        relayLabel.place(x=x-230, y=y+3, width=220, height=40)
        if color is 'green':
            label = tk.Label(controller, text='ACTIVE', font=NOTIFICATION_FONT, bg='green')
        else:
            label = tk.Label(controller, text='RUN', font=NOTIFICATION_FONT, bg='grey')
        label.place(x=x+10, y=y+3, width=75, height=40)

    def drawDataOutput(self, controller, x, y, fullLine):
        """Draw label of something at a value with units"""
        label = tk.Label(controller, text=fullLine, font=NOTIFICATION_FONT)
        label.place(x=x, y=y, width=250, height=40)

class DataHandler():
    """Handles serial communications and data managment."""

    def __init__(self):
        """Blah blah blah."""
        self.mesHeadDict = (
         {'fileName': {'TANKD:': 'WWT-TankLevels',
                       'PRESSD:': 'WWT-Pressure',
                       'IFLOW:': 'WWT-iFlow',
                       'TFLOW:': 'WWT-tFlow',
                       'TandPD': 'WWT-TandPD',
                       'RelayD': 'WWT-Relays',
                       '1valveD': 'WWT-Valves1',
                       '2valveD': 'WWT-Valves2'},
          'fileHeader': {'TANKD:': 'WW\tROF\tNFF\tGW\tWASTE\ttime\n',
                         'PRESSD:': 'F\tC1\tC2\tNFR\tROR\ttime\n',
                         'IFLOW:': 'C\tNFP\tNFR\tROP\tROR\ttime\n',
                         'TFLOW:': 'C\tNFP\tNFR\tROP\tROR\ttime\n',
                         'TandPD': 'UT\tAC\tDC\tPWRR\tPWRB\ttime\n',
                         'RelayD': 'P\tBUB\tO3\tO3pump\tUV\ttime\n',
                         '1valveD': 'NFPOT\tNFF\tNFFT\tGW\tCFF\ttime\n',
                         '2valveD': 'ROPOT\tROF\tROFT\tWWT\tWASTE\ttime\n'}})
        self.serialCom = serial.Serial('/dev/ttyACM0', 9600)

    def RunAndLog(self):
        """Blah blah blah."""
        # Get current time
        message = self.serialCom.readline()
        parsedMessage = message.split('\t')
        dictIndex = parsedMessage[0]
        parsedMessage.remove(parsedMessage[0])
        message = parsedMessage

        now = time.localtime(time.time())
        fileName = "{0}_{1}_{2}_" + self.mesHeadDict['fileName'][dictIndex] \
                   + ".txt".format(now.tm_year, now.tm_mon, now.tm_mday)

        if not (os.path.isfile(fileName)):
            file = open(fileName, "w")
            file.write(self.mesHeadDict['fileHeader'][dictIndex])
            file.flush()
            file.close()

        # open file and save serial data from arduino
        file = open(fileName, "a")
        # message = serialCom.readline()
        # print('\t'.join(message))
        file.write('\t'.join(message))
        file.flush()
        file.close()


if __name__ == "__main__":
    # handler = DataHandler()
    # serialListener = threading.Thread(target=handler.RunAndLog, args=())
    # serialListenerEvent = threading.Event()
    # serialListener.start()
    app = Interface()  # Create application
    app.mainloop()
    # serialListener.join()
