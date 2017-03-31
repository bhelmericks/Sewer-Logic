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
        self.advUsrButton = tk.Button(container, text="Maintenance",
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
        self.displayHomeowner(parent, controller)

    # display function seperate for updating purposes
    def displayHomeowner(self, parent, controller):
        data = currentData['TANKD:']
        # label = tk.Label(self, text="Homeowner Frame", font=TITLE_FONT)
        # label.pack(side="top", fill="x", pady=10)
        renderer = Renderer(self, 800, 420)

        # TO DO: save nowAsString in event of restart restarted
        nowAsString = time.strftime('%H:%M %m/%d/%Y')
        # TO DO: if statement for tank needing refilling
        washTank = nowAsString + ' NOTICE: add 1 gallon to Wash Tank'
        renderer.drawFlag(self, 10, 30, 30, 'blue', 'green', washTank)
        # TO DO: if statement for tank needing to be emptied
        wasteTank = nowAsString + ' NOTICE: Waste Tank needs to be Emptied'
        renderer.drawFlag(self, 10, 80, 30, 'yellow', 'green', wasteTank)
        # TO DO: if statement for errors in system.
        # May want to activiate a "shut down" mode here
        label = tk.Label(self, text='ERROR: Maintenance Required',
                         font=TITLE_FONT, fg='red')
        label.place(x=10, y=150, height=25)

        # display water levels on Homeowner page
        # note: these are also under class WaterLevel
        renderer.drawTank(self, 360, 195, 85, data[0]/85, "Wash")
        renderer.drawTank(self, 470, 195, 85, data[1]/85, "Grey\nWater")
        renderer.drawTank(self, 580, 195+80, 45, data[4]/45, "Waste\nWater")



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

        waterButton = tk.Button(self, text="Tank Level",
                                font=BUTTON_FONT, command=lambda:
                                controller.show_frame(WaterLevel), bg='grey')
        # Add to navigation button dictionary
        controller.buttons[WaterLevel] = waterButton
        waterButton.place(x=160, y=0, width=160, height=50)

        statusButton = tk.Button(self, text="Valves and\nRelays",
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
        """These are from Dotson Labs code."""
        tk.Frame.__init__(self, parent)
        self.controller = controller

        RegButton = (tk.Button(self, text='Regular Day',
                     command=lambda:
                     partial(handler.manualCommand('RegularDay\n'))))
        RegButton.grid(row=0, column=4)
        RegButton.config(height=5, width=16)

        WasteButton = (tk.Button(self, text='Waste Day',
                       command=lambda:
                       partial(handler.manualCommand('FullWasteDay\n'))))
        WasteButton.grid(row=1, column=4)
        WasteButton.config(height=5, width=16)

        QuitButton = (tk.Button(self, text='Quit',
                      command=lambda: self.exit()))
        QuitButton.grid(row=5, column=4)
        QuitButton.config(height=5, width=16)

        CFButton = (tk.Button(self, text='CF',
                    command=lambda: handler.manualCommand('CFwithRinse\n')))
        CFButton.grid(row=0, column=0)
        CFButton.config(height=5, width=16)

        CFWOButton = (tk.Button(self, text='CF wo R',
                      command=lambda: handler.manualCommand('CFwoRinse\n')))
        CFWOButton.grid(row=0, column=2)
        CFWOButton.config(height=5, width=16)

        NFButton = (tk.Button(self, text='NF',
                    command=lambda: handler.manualCommand('NFwithRinse\n')))
        NFButton.grid(row=1, column=0)
        NFButton.config(height=5, width=16)

        NFWOButton = (tk.Button(self, text='NF wo R',
                      command=lambda: handler.manualCommand('NFwoRinse\n')))
        NFWOButton.grid(row=1, column=2)
        NFWOButton.config(height=5, width=16)

        ROButton = (tk.Button(self, text='RO',
                    command=lambda: handler.manualCommand('ROwithRinse\n')))
        ROButton.grid(row=2, column=0)
        ROButton.config(height=5, width=16)

        ROWOButton = (tk.Button(self, text='RO wo R',
                      command=lambda: handler.manualCommand('ROwoRinse\n')))
        ROWOButton.grid(row=2, column=2)
        ROWOButton.config(height=5, width=16)

    def exit(self):
        """Blah blah blah."""
        result = (tkMessageBox.askquestion('Exit WWT Interface Confirmation',
                                           'Are you sure you want to quit?',
                                           icon='warning'))
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
        self.displayPowerandTemp(parent, controller, renderer)

    def displayPowerandTemp(self, parent, controller, renderer):
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
                fullLine = str(x) + ':  ' + str("%.1f" %numberIn) + '  ' + 'Amps'
            else:
                numberIn = (x-1 * (2 + x-1) + 90)+(x-1 * (2 + x-1) + 90)
                fullLine = ('Total Power' + ':  ' + str("%.1f" %numberIn)
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
        self.displayFlowAndPressure(parent, controller, renderer)

    def displayFlowAndPressure(self, parent, controller, renderer):
        # labels for pressures and valves
        names = []
        names.append('Feed')
        names.append('CF2')
        names.append('CF3')
        names.append('NF')
        names.append('RO')

        fullLine = 'Pressure'
        renderer.drawDataOutput(self, 20, 50, fullLine)

        data = currentData['PRESSD:']
        for x in range(0, 5):
            fullLine = names[x]+':  '+str("%.0f" % data[x])+'  '+'psi'
            renderer.drawDataOutput(self, 20, x*40+100, fullLine)

        names.append('CF1')
        names.append('CF2')
        names.append('CF3')
        names.append('NFX')
        names.append('ROX')

        fullLine = 'Differential\nPressure'
        renderer.drawDataOutput(self, 200, 50, fullLine)
        for x in range(0, 5):
            fullLine = names[x+5]+':  '+str("%.0f" % data[x])+'  '+'psi'
            renderer.drawDataOutput(self, 200, x*40+100, fullLine)

        names.append('Feed')
        names.append('CF')
        names.append('NFP')
        names.append('ROP')
        names.append('NFR')
        names.append('ROR')

        fullLine = 'Flow'
        renderer.drawDataOutput(self, 400, 50, fullLine)
        data = currentData['IFLOWD:']
        for x in range(0, 6):

            fullLine = (names[x+10] + ':  ' + str("%.2f" % data[x])
                        + '  ' + 'gpm')
            renderer.drawDataOutput(self, 400, x*40+100, fullLine)


class WaterLevel(tk.Frame):
    """Water levels frame."""

    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.displayWaterLevel(parent, controller)

    def displayWaterLevel(self, parent, controller):
        data = currentData['TANKD:']
        renderer = Renderer(self, 800, 380)
        # note: 3 of these are also called under class Homeowner
        renderer.drawTank(self, 50, 95, 85, data[0]/85, "Wash")
        renderer.drawTank(self, 200, 95, 85, data[1]/85, "Grey\nWater")
        renderer.drawTank(self, 350, 95, 85, data[2]/85, "NF Feed")
        renderer.drawTank(self, 500, 95, 85, data[3]/85, "RO Feed")
        renderer.drawTank(self, 650, 95+85, 45, data[4]/45, "Waste\nWater")


class SystemStatus(tk.Frame):
    """System status frame."""


    def __init__(self, parent, controller):
        """Blah blah blah."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="System Status Frame", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        renderer = Renderer(self, 800, 430)

        manualOn = False

        # initial valves and labels
        renderer.drawDataOutput(self, 10, 20, 'Valves')
        self.valvePosition = []                             # this holds the valve on/off positions
        for x in range(0, 8):
            if x < 4:
                self.valvePosition.append('OFF')
                yposition = 70 + 60*x
                renderer.drawDataOutput(self, -100, yposition, str(x+1))
            else:
                self.valvePosition.append('OFF')
                yposition = 70 + 60*(x-4)
                renderer.drawDataOutput(self, 100, yposition, str(x+1))
        # relay labels
        renderer.drawDataOutput(self, 350, 20, 'Relays')
        relay = []
        relay.append('Soap Removal')
        relay.append('UV Disinfection')
        relay.append('Ozone Disinfection')
        relay.append('Ozone Pump')
        relay.append('High Pressure Pump')
        yposition = 70
        for x in range(0, 5):
            renderer.drawDataOutput(self, 250, yposition, relay[x])
            yposition = yposition+55

        # initial relays
        self.active = []                                # this holds the relay active/inactive status
        self.active.append(False)
        self.active.append(False)
        self.active.append(False)
        self.active.append(False)
        self.active.append(False)

        # display relays and valves
        relayButtons = self.displayRelays(manualOn, self.active)
        valveButtons = self.displayValves(manualOn, self.valvePosition)
        self.displayGlobalManualButton(controller, manualOn,
                                       relayButtons, valveButtons)
        self.displayValvesAndRelays(parent, controller, renderer, relayButtons, valveButtons)

    def displayValvesAndRelays(self, parent, controller, renderer, relayButtons, valveButtons):
        # two variable valves
        xposition = 10
        yposition = 300
        number = yposition / 30 + 13
        fullLine = 'NF Fev: ' + str(int(number)) + '% OPEN'
        renderer.drawDataOutput(self, xposition, yposition, fullLine)
        yposition = yposition + 40
        number = yposition / 30 - 3
        fullLine = 'RO Fev: ' + str(int(number)) + '% OPEN'
        renderer.drawDataOutput(self, xposition, yposition, fullLine)
        data = currentData['RelayD']
        for x in range(0, len(data)):
            self.changeRelayButton(data[x], relayButtons)
        data = currentData['1valveD']
        for x in range(0, len(data)):
            self.changeValveButton(data[x], valveButtons)


    # set manual button for valves and relay
    def displayGlobalManualButton(self, controller,  manualOn,
                                  relayButton, valveButton):
        """Blah Blah Blah."""
        if manualOn:
            displayText = 'Manual\nMode Off'
        else:
            displayText = 'Manual\nMode'
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
                         self.changeRelayButton(index, relayButtonIn))

    def changeRelayButton(self, index, relayButton):
        """Blah Blah Blah."""
        if self.active[index]:
            self.active[index] = False
            relayButton[index].config(bg='light grey', text='RUN')
        else:
            self.active[index] = True
            relayButton[index].config(bg='green', text='ACTIVE')
        return self.active

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
                         self.changeValveButton(index, valveButton),
                         disabledforeground='grey25')

    def changeValveButton(self, index, valveButton):
        """Blah Blah Blah."""
        if self.valvePosition[index]:
            self.valvePosition[index] = False
            valveButton[index].config(text='OFF', bg='orangered')
        else:
            self.valvePosition[index] = True
            valveButton[index].config(text='ON', bg='green')
        return self.valvePosition

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
        labelheight = 25
        self.create_rectangle(x, y, x+100, y+size, width=3, fill='grey')
        if fill < 1:
            self.create_rectangle(x+2, y-fill*(size-3)+size-1, x+99, y+size-1,
                              width=0, fill='midnight blue')
            gals = tk.Label(parent,
                            text=str(int(sizeLabel * fill)) + '/' + str(sizeLabel)
                                 + 'gal', font=NOTIFICATION_FONT)
        else:
            fill = 1
            self.create_rectangle(x + 2, y - fill * (size - 3) + size - 1, x + 99, y + size - 1,
                                  width=0, fill='red')
            gals = tk.Label(parent,
                            text='OVERFLOW\n'+str(int(sizeLabel * fill)) + '/' + str(sizeLabel)
                                 + 'gal', font=NOTIFICATION_FONT)

            labelheight = 45

        gals.place(x=x, y=y-labelheight-1, width=120, height=labelheight)
        label = tk.Label(parent, text=name, font=TITLE_FONT)
        label.place(x=x, y=y+size+5, width=100)

    def drawDataOutput(self, parent, x, y, fullLine):
        """Draw label of something at a value with units."""
        label = tk.Label(parent, text=fullLine, font=NOTIFICATION_FONT)
        label.place(x=x, y=y, width=250, height=40)


class DataHandler():
    """Handles serial communications and data managment."""

    def __init__(self):
        """Blah blah blah."""
        self.mesHeadDict = (
            {'TANKD:': {'fileName': 'WWT-TankLevels',
                        'fileHead': 'WW\tROF\tNFF\tGW\tWASTE\ttime\n'},
             'PRESSD:': {'fileName': 'WWT-Pressure',
                         'fileHead': 'F\tC1\tC2\tNFR\tROR\ttime\n'},
             'IFLOWD:': {'fileName': 'WWT-iFlow',
                         'fileHead': 'C\tNFP\tNFR\tROP\tROR\ttime\n'},
             'TFLOWD:': {'fileName': 'WWT-tFlow',
                         'fileHead': 'C\tNFP\tNFR\tROP\tROR\ttime\n'},
             'TandPD': {'fileName': 'WWT-TandPD',
                        'fileHead': 'UT\tAC\tDC\tPWRR\tPWRB\ttime\n'},
             'RelayD': {'fileName': 'WWT-Relays',
                        'fileHead': 'P\tBUB\tO3\tO3pump\tUV\ttime\n'},
             '1valveD': {'fileName': 'WWT-Valves1',
                         'fileHead': 'NFPOT\tNFF\tNFFT\tGW\tCFF\ttime\n'},
             '2valveD': {'fileName': 'WWT-Valves2',
                         'fileHead': 'ROPOT\tROF\tROFT\tWWT\tWASTE\ttime\n'}})

        self.commandDict = (
            {'RegularDay\n':
                {'startMessage': 'Regular Day',
                 'cancelMessage': 'Regular Day Treatment Canceled',
                 'confMessage': 'Regular Treatment Day Confirmation'},
             'FullWasteDay\n':
                {'startMessage': 'Waste Day',
                 'cancelMessage': 'Waste Day Treatment Canceled',
                 'confMessage': 'Waste Treatment Day Confirmation'},
             'HalfWasteDay\n':
                 {'startMessage': 'Half Waste Day',
                  'cancelMessage': '',
                  'confMessage': ''},
             'CFwithRinse\n':
                 {'startMessage': 'Cartridge Filter',
                  'cancelMessage': 'Cartridge Filter Treatment Step Canceled',
                  'confMessage': 'Cartridge Filter Step Confirmation'},
             'CFwoRinse\n':
                 {'startMessage': 'Cartridge Filter without Rinse',
                  'cancelMessage': 'Cartridge Filter without Rinse Treatment \
                                    Step Canceled',
                  'confMessage': 'Cartridge Filter w/o Step Confirmation'},
             'NFwithRinse\n':
                 {'startMessage': 'Nanofilter',
                  'cancelMessage': 'Nanofilter Treatment Step Canceled',
                  'confMessage': 'Nanofilter Step Confirmation'},
             'NFwoRinse\n':
                 {'startMessage': 'Nanofilter without Rinse',
                  'cancelMessage': 'Nanofilter without Rinse Treatment Step \
                                    Canceled',
                  'confMessage': 'Nanofilter w/o Step Confirmation'},
             'ROwithRinse\n':
                 {'startMessage': 'Reverse Osmosis',
                  'cancelMessage': 'Reverse Osmosis Treatment Step Canceled',
                  'confMessage': 'Reverse Osmosis Step Confirmation'},
             'ROwoRinse\n':
                 {'startMessage': 'Reverse Osmosis without Rinse',
                  'cancelMessage': 'Reverse Osmosis without Rinse Treatment \
                                    Step Canceled',
                  'confMessage': 'Reverse Osmosis w/o Step Confirmation'}})

        self.serialCom = serial.Serial('/dev/ttyACM0', 9600)

        schedule.every().monday.at("9:00").do(
            self.scheduledCommand, 'RegularDay\n')
        schedule.every().tuesday.at("9:00").do(
            self.scheduledCommand, 'HalfWasteDay\n')
        schedule.every().wednesday.at("9:00").do(
            self.scheduledCommand, 'RegularDay\n')
        schedule.every().thursday.at("9:00").do(
            self.scheduledCommand, 'RegularDay\n')
        schedule.every().friday.at("09:00").do(
            self.scheduledCommand, 'FullWasteDay\n')
        schedule.every().saturday.at("9:00").do(
            self.scheduledCommand, 'RegularDay\n')
        schedule.every().sunday.at("9:00").do(
            self.scheduledCommand, 'RegularDay\n')

        self.serialListener = threading.Thread(target=self.runAndLog, args=())
        self.serialListenerEvent = threading.Event()
        self.serialListener.start()
        print 'Serial Com Thread Started'

    def runAndLog(self):
        """Blah blah blah."""
        while not self.serialListenerEvent.isSet():
            #schedule.run_pending()
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
                            + self.mesHeadDict[dictIndex]['fileName'] + '.txt')
                # If file is not yet present create then add headers to file
                if not (os.path.isfile(fileName)):
                    file = open(fileName, "w")
                    file.write(self.mesHeadDict[dictIndex]['fileHead'])
                    file.flush()
                    file.close()

                # Open file and save serial data from arduino
                file = open(fileName, "a")
                file.write('\t'.join(message))
                file.flush()
                file.close()
                print 'Data saved!'

    def manualCommand(self, command):
        """Blah blah blah."""
        result = tk.MessageBox.askquestion(
                    self.commandDict[command]['confMessage'],
                    'Are you sure?', icon='warning')
        if result == 'yes':
            print 'MANUAL ACTIVATED: ' \
                  + self.commandDict[command]['startMessage']
            self.serialCom.write(command)
        else:
            print self.commandDict[command]['cancelMessage']

    def scheduledCommand(self, command):
        """Blah blah blah."""
        print 'It is 9:00AM, Scheduled Treatment: ' \
              + self.commandDict[command]['startMessage']
        self.serialCom.write(command)

    def exit(self):
        """Blah blah blah."""
        print 'Serial Com Thread Closing...'
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
