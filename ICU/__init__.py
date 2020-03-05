#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import os
import atexit

from pprint import pprint

from . import constants
from . import event
from . import panel
from . import system_monitor
from . import main_panel
from . import tracking
from . import fuel_monitor
from . import keyhandler
from . import eyetracking
from . import component

__all__ = ('panel', 'system_monitor', 'constants', 'event', 'main_panel', 'tracking', 'fuel_monitor')

os.system('xset r off') #problem with key press/release otherwise

event.GLOBAL_EVENT_CALLBACK.add_event_callback(lambda *args: print("callback: ", *args))

def quit():
    global finish
    finish = True
    root.destroy()

class Fullscreen:

    def __init__(self, root, fullscreen=False):
        self.root = root
        self.fullscreen = fullscreen
        root.attributes("-fullscreen", self.fullscreen)
        print("full screen")
        self.root.bind("<Escape>", self.toggle)
        self.root.bind("<F11>", self.toggle)

    def toggle(self, event):
        self.fullscreen = not self.fullscreen
        root.attributes("-fullscreen", self.fullscreen)


root = tk.Tk()
full_screen = Fullscreen(root, False)

root.title("MATB-II")
root.protocol("WM_DELETE_WINDOW", quit)
root.geometry('%dx%d+%d+%d' % (1000, 1000, 1000, 500))

event.tk_event_schedular(root) #initial global event schedular

main = main_panel.MainPanel(root)

system_monitor_widget = system_monitor.SystemMonitorWidget(main.top, width=constants.SYSTEM_MONITOR_WIDTH, 
                                                                     height=constants.SYSTEM_MONITOR_HEIGHT)

system_monitor_widget.pack(side='left')

tracking_widget = tracking.TrackingWidget(main.top, size=400)
tracking_widget.pack(side='left')

fuel_monitor_widget = fuel_monitor.FuelWidget(main.bottom, width=constants.FUEL_MONITOR_WIDTH, 
                                                           height=constants.FUEL_MONITOR_HEIGHT)
fuel_monitor_widget.pack(side='left')

main.pack()

#event.event_scheduler.schedule(system_monitor.WarningLightEventGenerator(), sleep=1000, repeat=True)
#event.event_scheduler.schedule(system_monitor.ScaleEventGenerator(), sleep=1000)
#event.event_scheduler.schedule(tracking.TrackingEventGenerator(), sleep=100, repeat=True)

def highlight_event_generator():
    import random
    while True:
        name = random.choice(list(component.all_components().keys()))
        yield event.Event(name, 'highlight', 1)

#event.event_scheduler.schedule(highlight_event_generator(), sleep=1000, repeat=True)

print("ALL COMPONENTS: ")
pprint(component.all_components())



if constants.JOYSTICK:
    raise NotImplementedError("TODO are we using a joystick!?")
else:
    global_key_handler = keyhandler.KeyHandler(root)
    #event.event_scheduler.schedule(tracking.KeyEventGenerator(global_key_handler), sleep=50, repeat=True)


    #there is a delay, it needs an press/release handler to work smoothly and to handle simultanneous presses...
    #root.bind("<Left>",     lambda *args: keyhandler.left_callback(*args))
    #root.bind("<Right>",    lambda *args: keyhandler.right_callback(*args))
    #root.bind("<Up>",       lambda *args: keyhandler.up_callback(*args))
    #root.bind("<Down>",     lambda *args: keyhandler.down_callback(*args))

    #TODO record joystick data (send the event to somewhere else aswell!)
    #TODO record the target position at a given time interval, generate an event





# ================= EYE TRACKING ================= 

eyetracker = None
if constants.EYETRACKING:
    eyetracker = eyetracking.eyetracker(sample_rate=1, stub=True)
    eyetracker.start()

#ensure the program exits properly
def exit_handler():
    os.system('xset r on') #back to how it was before?
atexit.register(exit_handler) 

root.mainloop()

if eyetracker is not None:
    eyetracker.close()






