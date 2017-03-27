"""Blah blah blah."""
import os.path
import schedule
import serial
import threading
import time
import tkMessageBox
import Tkinter as tk
from functools import partial

TITLE_FONT = ("Helvetica", 17, "bold")
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

        self.show_frame(AdvUser)  # Show default frame

    # Bring selected frame to the front and enable/disable relevant buttons
    def show_frame(self, page_name):
        """Blah blah blah."""
        self.frames[page_name].tkraise()  # Raise frame to top
        if page_name == Homeowner:
            # If Homeowner is selected reenable advUserButton
            self.buttons[AdvUser].config(state="normal", bg='grey')
        elif page_name == AdvUser:
            # If AdvUser is selected reenable homeownerButton
            self.buttons[Homeowner].config(state="normal", bg='grey')
        else:
            for F in (Option, PowerAndTemp, FlowAndPressure,
                      WaterLevel, SystemStatus):
                if page_name != F:
                    # Enable unselected AdvUser buttons
                    self.buttons[F].config(state="normal", bg='grey')
        # Disable selected button
        self.buttons[page_name].config(state="disabled",
                                       disabledforeground='black', bg='grey95')


class Homeowner(tk.Frame):
    """Homeowner frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="Homeowner Frame", font=TITLE_FONT)
        # label.pack(side="top", fill="x", pady=10)
        # find a way to make nowAsString retain value
        nowAsString = time.strftime('%H:%M %m/%d/%Y')
        washTank = nowAsString + ' NOTICE: add 1 gallon to Wash Tank'
        wasteTank = nowAsString + ' NOTICE: Waste Tank needs to be Emptied'
        renderer = Renderer(self, 800, 420)
        # logic to force into true values needed
        renderer.drawFlag(self, 10, 30, 15, 'blue', 'green', washTank)

        renderer.drawFlag(self, 10, 80, 15, 'yellow', 'green', wasteTank)
        label = tk.Label(self, text='ERROR: Maintenance Required',
                         font=TITLE_FONT, fg='red')
        label.place(x=10, y=150, height=25)
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
                                 controller.show_frame(Option), bg='grey')
        # Add to navigation button dictionary
        controller.buttons[Option] = optionButton
        optionButton.place(x=640, y=0, width=160, height=50)

        tempButton = tk.Button(self, text="Power and \n Temperature",
                               font=BUTTON_FONT, command=lambda:
                               controller.show_frame(PowerAndTemp), bg='grey')
        # Add to navigation button dictionary
        controller.buttons[PowerAndTemp] = tempButton
        tempButton.place(x=480, y=0, width=160, height=50)

        flowButton = tk.Button(self, text="Flow and \n Pressure",
                               font=BUTTON_FONT, command=lambda:
                               controller.show_frame(FlowAndPressure),
                               bg='grey')
        # Add to navigation button dictionary
        controller.buttons[FlowAndPressure] = flowButton
        flowButton.place(x=320, y=0, width=160, height=50)

        waterButton = tk.Button(self, text="Water Level",
                                font=BUTTON_FONT, command=lambda:
                                controller.show_frame(WaterLevel), bg='grey')
        # Add to navigation button dictionary
        controller.buttons[WaterLevel] = waterButton
        waterButton.place(x=160, y=0, width=160, height=50)

        statusButton = tk.Button(self, text="System Status",
                                 font=BUTTON_FONT, command=lambda:
                                 controller.show_frame(SystemStatus),
                                 bg='grey')
        # statusButton is selected by default
        statusButton.config(state="disabled", disabledforeground='black',
                            bg='grey95')
        # Add to navigation button dictionary
        controller.buttons[SystemStatus] = statusButton
        statusButton.place(x=0, y=0, width=160, height=50)


class Option(tk.Frame):
    """Options frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        RegButton = (tk.Button(self, text='Regular Day',
                     command=lambda: partial(handler.manualCommand('D\n'))))
        RegButton.grid(row=0, column=4)
        RegButton.config(height=5, width=16)

        WasteButton = (tk.Button(self, text='Waste Day',
                       command=lambda: partial(handler.manualCommand('W\n'))))
        WasteButton.grid(row=1, column=4)
        WasteButton.config(height=5, width=16)

        QuitButton = (tk.Button(self, text='Quit',
                      command=lambda: self._exit()))
        QuitButton.grid(row=5, column=4)
        QuitButton.config(height=5, width=16)

        CFButton = (tk.Button(self, text='CF',
                    command=lambda: handler.manualCommand('V\n')))
        CFButton.grid(row=0, column=0)
        CFButton.config(height=5, width=16)

        CFWOButton = (tk.Button(self, text='CF wo R',
                      command=lambda: handler.manualCommand('C\n')))
        CFWOButton.grid(row=0, column=2)
        CFWOButton.config(height=5, width=16)

        NFButton = (tk.Button(self, text='NF',
                    command=lambda: handler.manualCommand('M\n')))
        NFButton.grid(row=1, column=0)
        NFButton.config(height=5, width=16)

        NFWOButton = (tk.Button(self, text='NF wo R',
                      command=lambda: handler.manualCommand('N\n')))
        NFWOButton.grid(row=1, column=2)
        NFWOButton.config(height=5, width=16)

        ROButton = (tk.Button(self, text='RO',
                    command=lambda: handler.manualCommand('T\n')))
        ROButton.grid(row=2, column=0)
        ROButton.config(height=5, width=16)

        ROWOButton = (tk.Button(self, text='RO wo R',
                      command=lambda: handler.manualCommand('R\n')))
        ROWOButton.grid(row=2, column=2)
        ROWOButton.config(height=5, width=16)

    def _exit(self):
        """Blah blah blah."""
        result = tkMessageBox.askquestion('Exit WWT Interface Confirmation', 'Are You Sure?', icon='warning')
        if result == 'yes':
            app.quit()
        else:
            print 'Exit Program Canceled'


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
                fullLine = 'Outside' + ':  ' + str(numberIn) + '  ' + 'C'
            elif x is 1:
                fullLine = 'AC Panel' + ':  ' + str(numberIn) + '  ' + 'C'
            else:
                fullLine = 'DC Panel' + ':  ' + str(numberIn) + '  ' + 'C'
            renderer.drawDataOutput(self, 20, x * 40 + 100, fullLine)
            numberIn = x * (2 + x) + 90
            if x < 2:
                fullLine = str(x) + ':  ' + str(numberIn) + '  ' + 'Amps'
            else:
                numberIn = (x-1 * (2 + x-1) + 90)+(x-1 * (2 + x-1) + 90)
                fullLine = ('Total Power' + ':  ' + str(numberIn)
                            + '  ' + 'Amps')
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
        fullLine = 'Pressure'
        renderer.drawDataOutput(self, 40, 50, fullLine)
        fullLine = 'Flow'
        renderer.drawDataOutput(self, 340, 50, fullLine)
        for x in range(0, 5):
            numberIn = x*(2+x)+20+0.532-(0.1*x)
            fullLine = str(x)+':  '+str("%.0f" % numberIn)+'  '+'psi'
            renderer.drawDataOutput(self, 20, x*40+100, fullLine)
            numberIn = x * (2 + x) + 50+0.932-(0.1*x)
            fullLine = (str(x) + ':  ' + str("%.2f" % numberIn)
                        + '  ' + 'gal/min')
            renderer.drawDataOutput(self, 320, x*40+100, fullLine)


class WaterLevel(tk.Frame):
    """Water levels frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        data = currentData['TANKD:']
        renderer = Renderer(self, 800, 380)
        renderer.drawTank(self, 50, 95, 85, data[0]/85, "Wash")
        renderer.drawTank(self, 200, 95, 85, data[1]/85, "Grey")
        renderer.drawTank(self, 350, 95, 85, data[2]/85, "NF Feed")
        renderer.drawTank(self, 500, 95, 85, data[3]/85, "RO Feed")
        renderer.drawTank(self, 650, 95+85, 45, data[4]/45, "Waste")


class SystemStatus(tk.Frame):
    """System status frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="System Status Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        renderer = Renderer(self, 800, 430)

        # two variable valves
        xposition = 10
        yposition = 300
        number = yposition / 30 + 13
        fullLine = '1: ' + str(int(number)) + '% OPEN'
        renderer.drawDataOutput(self, xposition, yposition, fullLine)
        yposition = yposition + 40
        number = yposition / 30 - 3
        fullLine = '2: ' + str(int(number)) + '% OPEN'
        renderer.drawDataOutput(self, xposition, yposition, fullLine)

        manualOn = False

        # initial valves and labels
        renderer.drawDataOutput(self, 10, 20, 'Valves')
        valvePosition = []
        for x in range(0, 8):
            if x < 4:
                valvePosition.append('OFF')
                yposition = 70 + 60*x
                renderer.drawDataOutput(self, -100, yposition, str(x+1))
            else:
                valvePosition.append('OFF')
                yposition = 70 + 60*(x-4)
                renderer.drawDataOutput(self, 100, yposition, str(x+1))
        # relay labels
        renderer.drawDataOutput(self, 350, 20, 'Relays')
        relay = []
        relay.append('Bubbler')
        relay.append('UV')
        relay.append('Ozone')
        relay.append('Ozone Pump')
        relay.append('High Pressure Pump')
        yposition = 70
        for x in range(0, 5):
            renderer.drawDataOutput(self, 250, yposition, relay[x])
            yposition = yposition+55

        # initial relays
        active = []
        active.append(False)
        active.append(False)
        active.append(False)
        active.append(False)
        active.append(False)
        # display relays and valves
        relayButtons = self.displayRelays(manualOn, active)
        valveButtons = self.displayValves(manualOn, valvePosition)
        self.displayGlobalManualButton(controller, manualOn,
                                       relayButtons, valveButtons)

    # set manual button for valves and relay
    def displayGlobalManualButton(self, controller,  manualOn,
                                  relayButton, valveButton):
        """Blah Blah Blah."""
        if manualOn:
            displayText = 'Exit\nManual'
        else:
            displayText = 'Enter\nManual'
        manualButton = tk.Button(self, text=displayText,
                                 font=NOTIFICATION_FONT, bg='grey',
                                 state="normal", command=lambda:
                                 self.changeGlobalManual(controller,
                                                         self.invert(manualOn),
                                                         relayButton,
                                                         valveButton))
        manualButton.place(x=675, y=40, width=100)

    def invert(self, manualIn):
        """Blah Blah Blah."""
        if manualIn:
            return False
        else:
            return True

    def changeGlobalManual(self, controller, manualIn,
                           relayButton, valveButton):
        """Blah Blah Blah."""
        self.changeRelayManual(manualIn, relayButton)
        self.changeValveManual(manualIn, valveButton)
        self.displayGlobalManualButton(controller, manualIn,
                                       relayButton, valveButton)

    def displayRelays(self, manualOn, active):
        """Blah Blah Blah."""
        relayButton = []
        for index in range(0, 5):
            if manualOn:
                    relayButton.append(
                        self.makeRelayButton("normal", active,
                                             index, relayButton))
            else:
                relayButton.append(
                    self.makeRelayButton("disabled", active,
                                         index, relayButton))
            relayButton[index].place(y=70+index*55, x=500, width=100)
        return relayButton

    # logic to interact with serial should go here
    def makeRelayButton(self, stateIn, active, index, relayButtonIn):
        """Blah Blah Blah."""
        if active[index]:
            color = 'green'
            textIn = 'ACTIVE'
        else:
            color = 'light grey'
            textIn = 'RUN'
        return tk.Button(self, text=textIn, font=NOTIFICATION_FONT, bg=color,
                         state=stateIn, fg='black',
                         disabledforeground='grey25',
                         command=lambda:
                         self.changeRelayButton(active, index, relayButtonIn))

    def changeRelayButton(self, array, index, relayButton):
        """Blah Blah Blah."""
        if array[index]:
            array[index] = False
            relayButton[index].config(bg='light grey', text='RUN')
        else:
            array[index] = True
            relayButton[index].config(bg='green', text='ACTIVE')
        return array

    def changeRelayManual(self, manualIn, relayButton):
        """Blah Blah Blah."""
        if manualIn:
            for index in range(0, 5):
                relayButton[index].config(state='normal')
        else:
            for index in range(0, 5):
                relayButton[index].config(state='disabled')

    def displayValves(self, manualOn, position):
        """Blah Blah Blah."""
        valveButton = []
        for index in range(0, 8):
            if manualOn:
                valveButton.append(
                        self.makeValveButton("normal", position,
                                             index, valveButton))
            else:
                valveButton.append(
                    self.makeValveButton("disabled", position,
                                         index, valveButton))
            if index < 4:
                valveButton[index].place(y=70+index*60, x=50, width=50)
            else:
                valveButton[index].place(y=70+(index-4)*60, x=150, width=50)
        return valveButton

    # logic to interact with serial should go here
    def makeValveButton(self, stateIn, position, index, valveButton):
        """Blah Blah Blah."""
        if position[index]:
            color = 'green'
            textIn = 'ON'
        else:
            color = 'orangered'
            textIn = 'OFF'
        return tk.Button(self, text=textIn, font=NOTIFICATION_FONT, bg=color,
                         state=stateIn, command=lambda:
                         self.changeValveButton(position, index, valveButton),
                         disabledforeground='grey25')

    def changeValveButton(self, array, index, valveButton):
        """Blah Blah Blah."""
        if array[index]:
            array[index] = False
            valveButton[index].config(text='OFF', bg='orangered')
        else:
            array[index] = True
            valveButton[index].config(text='ON', bg='green')
        return array

    def changeValveManual(self, manualIn, valveButton):
        """Blah Blah Blah."""
        if manualIn:
            for index in range(0, 8):
                valveButton[index].config(state='normal')
        else:
            for index in range(0, 8):
                valveButton[index].config(state='disabled')


class Renderer(tk.Canvas):
    """Renderer used to draw GUI objects."""

    def __init__(self, parent, width, height):
        """."""
        tk.Canvas.__init__(self, parent)
        self.place(x=0, y=0, width=width, height=height)

    def drawFlag(self, parent, x, y, size, color0, color1, name):
        """Draw a circle flag object with a label to the right."""
        self.create_oval(x+4, y+4, x+size+4, y+size+4, width=2, fill=color0)
        label = tk.Label(parent, text=name, font=NOTIFICATION_FONT)
        label.place(x=x+size+5, y=y+4, height=size)

    def drawTank(self, parent, x, y, size, fill, name):
        """Draw a tank GUI object with a label below and # gallons above."""
        sizeLabel = size
        size = size*2
        self.create_rectangle(x, y, x+100, y+size, width=3, fill='grey')
        self.create_rectangle(x+2, y-fill*(size-3)+size-1, x+99, y+size-1,
                              width=0, fill='midnight blue')

        gals = tk.Label(parent,
                        text=str(int(sizeLabel*fill))+'/'+str(sizeLabel)
                        + 'gal', font=NOTIFICATION_FONT)
        gals.place(x=x, y=y-21, width=100, height=20)
        label = tk.Label(parent, text=name, font=TITLE_FONT)
        label.place(x=x, y=y+size+5, width=100, height=40)

    def drawDataOutput(self, parent, x, y, fullLine):
        """Draw label of something at a value with units."""
        label = tk.Label(parent, text=fullLine, font=NOTIFICATION_FONT)
        label.place(x=x, y=y, width=250, height=40)


class DataHandler():
    """Handles serial communications and data managment."""

    def __init__(self):
        """Blah blah blah."""
        self.mesHeadDict = (
         {'fileName':
          {'TANKD:': 'WWT-TankLevels',
           'PRESSD:': 'WWT-Pressure',
           'IFLOWD:': 'WWT-iFlow',
           'TFLOWD:': 'WWT-tFlow',
           'TandPD': 'WWT-TandPD',
           'RelayD': 'WWT-Relays',
           '1valveD': 'WWT-Valves1',
           '2valveD': 'WWT-Valves2'},
          'fileHeader':
          {'TANKD:': 'WW\tROF\tNFF\tGW\tWASTE\ttime\n',
           'PRESSD:': 'F\tC1\tC2\tNFR\tROR\ttime\n',
           'IFLOWD:': 'C\tNFP\tNFR\tROP\tROR\ttime\n',
           'TFLOWD:': 'C\tNFP\tNFR\tROP\tROR\ttime\n',
           'TandPD': 'UT\tAC\tDC\tPWRR\tPWRB\ttime\n',
           'RelayD': 'P\tBUB\tO3\tO3pump\tUV\ttime\n',
           '1valveD': 'NFPOT\tNFF\tNFFT\tGW\tCFF\ttime\n',
           '2valveD': 'ROPOT\tROF\tROFT\tWWT\tWASTE\ttime\n'}})

        self.commandDict = (
         {'startMessage':
          {'D\n': 'Regular Day',
           'W\n': 'Waste Day',
           'V\n': 'Cartridge Filter',
           'C\n': 'Cartridge Filter without Rinse',
           'M\n': 'Nanofilter',
           'N\n': 'Nanofilter without Rinse',
           'T\n': 'Reverse Osmosis',
           'R\n': 'Reverse Osmosis without Rinse'},
          'cancelMessage':
          {'D\n': 'Regular Day Treatment Canceled',
           'W\n': 'Waste Day Treatment Canceled',
           'V\n': 'Cartridge Filter Treatment Step Canceled',
           'C\n': 'Cartridge Filter without Rinse Treatment Step Canceled',
           'M\n': 'Nanofilter Treatment Step Canceled',
           'N\n': 'Nanofilter without Rinse Treatment Step Canceled',
           'T\n': 'Reverse Osmosis Treatment Step Canceled',
           'R\n': 'Reverse Osmosis without Rinse Treatment Step Canceled'},
          'confMessage':
          {'D\n': 'Regular Treatment Day Confirmation',
           'W\n': 'Waste Treatment Day Confirmation',
           'V\n': 'Cartridge Filter Step Confirmation',
           'C\n': 'Cartridge Filter w/o Step Confirmation',
           'M\n': 'Nanofilter Step Confirmation',
           'N\n': 'Nanofilter w/o Step Confirmation',
           'T\n': 'Reverse Osmosis Step Confirmation',
           'R\n': 'Reverse Osmosis w/o Step Confirmation'}})

        self.serialCom = serial.Serial('/dev/ttyACM0', 9600)

        schedule.every().monday.at("9:00").do(self.scheduledCommand, 'D\n')
        schedule.every().tuesday.at("9:00").do(self.scheduledCommand, 'D\n')
        schedule.every().wednesday.at("9:00").do(self.scheduledCommand, 'D\n')
        schedule.every().thursday.at("9:00").do(self.scheduledCommand, 'D\n')
        schedule.every().friday.at("09:00").do(self.scheduledCommand, 'D\n')
        schedule.every().saturday.at("9:00").do(self.scheduledCommand, 'D\n')
        schedule.every().sunday.at("9:00").do(self.scheduledCommand, 'D\n')

        self.serialListener = threading.Thread(target=self.runAndLog, args=())
        self.serialListenerEvent = threading.Event()
        self.serialListener.start()
        print 'Serial Listener Thread Started'

    def foo(self):
        print 'foo'

    def runAndLog(self):
        """Blah blah blah."""
        while not self.serialListenerEvent.isSet():
            # Get current time
            schedule.run_pending()
            message = self.serialCom.readline()
            parsedMessage = message.split('\t')
            if parsedMessage[0] in self.mesHeadDict:
                dictIndex = parsedMessage[0]
                del parsedMessage[0]
                global currentData
                currentData[dictIndex] = parsedMessage
                message = parsedMessage

                now = time.localtime(time.time())
                fileName = ('{0}_{1}_{2}_'.format(now.tm_year, now.tm_mon,
                                                  now.tm_mday)
                            + self.mesHeadDict['fileName'][dictIndex] + '.txt')

                if not (os.path.isfile(fileName)):
                    file = open(fileName, "w")
                    file.write(self.mesHeadDict['fileHeader'][dictIndex])
                    file.flush()
                    file.close()

                # Open file and save serial data from arduino
                file = open(fileName, "a")
                file.write('\t'.join(message))
                file.flush()
                file.close()

    def manualCommand(self, command):
        """Blah blah blah."""
        result = tk.MessageBox.askquestion(
                    self.commandDict['confMessage'][command],
                    'Are You Sure?', icon='warning')
        if result == 'yes':
            print 'MANUAL ACTIVATED: ' \
                  + self.commandDict['startMessage'][command]
            self.serialCom.write(command)
        else:
            print self.commandDict['cancelMessage'][command]

    def scheduledCommand(self, command):
        """Blah blah blah."""
        print 'It is 9:00AM, Scheduled Treatment: ' \
              + self.commandDict['startMessage'][command]
        self.serialCom.write(command)

    def exit(self):
        """Blah blah blah."""
        print 'Serial Listener Thread Closeing...'
        self.serialListenerEvent.set()
        self.serialListener.join()  # wait for the thread to finish
        print 'Closed'


if __name__ == "__main__":
    global currentData
    initialData = [0, 0, 0, 0, 0, 0]
    currentData = ({'TANKD:': initialData,
                    'PRESSD:': initialData,
                    'IFLOWD:': initialData,
                    'TFLOWD:': initialData,
                    'TandPD': initialData,
                    'RelayD': initialData,
                    '1valveD': initialData,
                    '2valveD': initialData})
    handler = DataHandler()
    app = Interface()  # Create application
    app.mainloop()
    print 'Exiting...'
    handler.exit()
    app.destroy()
