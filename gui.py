import tkinter as tk
import json
import time
from tkinter import *

import copy
import threading

from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode, Controller

mouse = MouseController()
keyboard = Controller()

#colors
ascgreen = "#90bf38"
ascblue = "#71a2d2"
asclightblue = "#e5f4ff"
ascorange = "#e78319"
asctext = "#00315E"

#root element of gui
root = tk.Tk()
root.title("minimanumacro")
root.geometry("500x700")
root.configure(bg=ascblue)


#logic relevant variables
titletext = "minimanumacro"
combo = False
recording = False
combinations = []
newmakro = []
makros = []
hotkeys = {}
recordinghotkeys = False
drag = BooleanVar()
combination_to_id = {}
currentcombination = set()
recorded_hotkeys = set()
recorded_hotkeys_str = set()
hotkeyid = 0
default_combinations = {}
running = None
statusvar = StringVar()
statusvar.set("Status: ready")
cancel = False

#debugging fpr console outputs
debug = False


#filling combination_to_id
def get_combination():
    for makro in makros:
        if makro["combination"] != []:
            combination_to_id[frozenset(makro["combination"])] = makro["id"]
            
def is_combination_pressed(combination):
    return all(k in currentcombination for k in combination)

def format_combination(list):
    s = []
    try:
        for key in list:
            s.append(key.replace("Key.", ""))
        return " + ".join(s)
    except:
        return list

def save_combination(combination, id):
    for makro in makros:
        if makro["id"] == id:
            makro["combination"] = combination
            makro["combinationstr"] = recorded_hotkeys_str
            save_makros()
            break

def findmakro(id):
    for makro in makros:
        if makro["id"] == id:
            return makro
    return None

def runmakro(id):
    global currentcombination, running, cancel
    currentcombination = set()
    if recording:
        if debug: print("can't play a macro while recording")
    else:
        if debug: print("running macro {0}".format(id))
        statusvar.set("Status: running macro")
        running = id
        makro = copy.deepcopy(findmakro(id)["makro"])
        startingtime = time.time()
        makrostart = makro[0]["time"]
        t = threading.currentThread()
        while len(makro) > 0 and getattr(t, "do_run", True) and not cancel:
            step = makro[0]
            istdelay =  time.time() - startingtime
            solldelay = step["time"] - makrostart 
            #if debug: print(f"soll: {solldelay} ; ist: {istdelay}")
            if istdelay >= solldelay:
                #makroschritt
                try:
                    if step["mok"] == "m":
                        #all Mouse actions
                        mouse.position = (step["x"], step["y"])
                        if step['action'] == 'scroll' and step['key'] == "middle":
                            mouseaction = "mouse." + step['action'] + "(" + str(step['dx']) + "," + str(step['dy']) + ")"
                            if debug: print(mouseaction)
                            exec(mouseaction)
                        elif step["action"] != "move":
                            mouseaction="mouse." + step["action"] + "(" + step["key"] + ")"
                            exec(mouseaction)
                    elif step["mok"] == "k":
                        #all keyboard actions
                        keyboardaction = "keyboard." + step["action"] + "(" + step["key"] + ")"
                        exec(keyboardaction)
                    else:
                        if debug: print("neither mouse nor keyboard...?!")
                except Exception as e:
                    if debug: print(e)
                    if debug: print("something didn't work *surprisedpikachuface*")
                if debug: print("making step")
                makro.pop(0)
        running = None
        cancel=False
        statusvar.set("Status: ready")

def run(id):
    if running == None:
        t = threading.Thread(target=runmakro, args=(id,))
        t.start()
    else: 
        if debug: print("macro already running")

def toggledrag():
    global drag
    if drag.get():
        drag.set(False)
    else: 
        drag.set(True)


def reset_hotkeys(id):
    if debug: print(f"resetting hotkeys of macro with id {id}")
    for makro in makros:
        if makro["id"] == id:
            makro["combination"] = []
            makro["combinationstr"] = []
            global combination_to_id
            for key in combination_to_id:
                if combination_to_id[key] == id:
                    del combination_to_id[key]
                    break
            with open('makros.json', 'w') as f:
                json.dump({"makros": makros}, f, indent=2) 
            rendermakros()
    pass

def save_makros():
    with open('makros.json', 'w') as f:
        tempmakros = makros
        for makro in tempmakros:
            makro["combination"] = list(makro["combination"])
            makro["combinationstr"] = list(makro["combinationstr"])
        json.dump({"makros": tempmakros}, f, indent=2) 



def rendermakros():
    get_combination()
    for widget in makroframe.winfo_children():
        widget.destroy()
    for row, makro in enumerate(makros):
        label = tk.Label(
            makroframe, 
            font="Helvetica 15", 
            text=makro["name"], 
            bg=asclightblue, 
            fg=asctext, 
            width = 10
            )
        label.grid(
            row=row, 
            column=1, 
            padx=3, 
            pady=1
            )
        makrohotkeys = tk.Label(
            makroframe, 
            fg=asctext, 
            bg=asclightblue,
            text=format_combination(makro.get("combinationstr"))
            )
        if makro["combination"] == []:
            makrohotkeys = tk.Button(
                makroframe, 
                fg=asctext, 
                text="add Hotkeys", 
                bg=ascorange, 
                command=lambda makro=makro: addhotkeys(makro["id"])
                )
        else:
            reset_btn = tk.Button(
                makroframe,
                fg=asctext,
                bg=ascorange,
                text="reset hotkeys",
                command= lambda makro=makro: reset_hotkeys(makro["id"])
            )
            reset_btn.grid(
                row=row,
                column=4
            )
        makrohotkeys.grid(
            row=row, 
            column=3, 
            padx=3, 
            ipadx=5)
        playbtn = tk.Button(
            makroframe, 
            text="run", 
            command=lambda makro=makro: run(makro["id"]), 
            bg=ascgreen, 
            fg=asctext
            )
        playbtn.grid(
            row=row, 
            column=2, 
            padx=3,
            ipadx=10,
            )
        
        deleteBtn = tk.Button(
            makroframe, 
            text="delete",
            command=lambda makro=makro: deleteById(makro["id"]), 
            bg="lightgrey", 
            fg=asctext)
        deleteBtn.grid(
            row=row, 
            column=0, 
            padx=3)

def render_message_box():
    if recordinghotkeys:
        for widget in makroframe.winfo_children():
            widget.destroy()
        messagebox = tk.Frame(makroframe, bg=asclightblue).grid(row=0, column=0)
        message1 = "Please push up to 3 buttons as hotkeys for this macro"
        message2 = ""
        label1 = tk.Label(messagebox, bg=ascblue, fg=asctext, text=message1).pack()

def deleteById(id):
    if debug: print("trying to delete macro with id'{0}'".format(id))
    for index, makro in enumerate(makros):
        if makro["id"] == id:
            if debug: print("found macro with id '{0}'".format(id))
            del makros[index]
            global combination_to_id
            if debug: print("combination_to_id:", combination_to_id)
            for key in combination_to_id:
                if combination_to_id[key] == id:
                    del combination_to_id[key]
                    break
            with open('makros.json', 'w') as f:
                json.dump({"makros": makros}, f, indent=2) 
            rendermakros()
            if debug: print("deleted macro with id '{0}'".format(id))
            break



#button actions
def record():
    if not recordinghotkeys:
        if debug: print("adding new Makro:")
        global newmakro
        newmakro = []
        global recording
        recording = True
        statusvar.set("Status: recording macro")

def abort():
    if debug: print("recording aborted.")
    global recording, newmakro, recordinghotkeys, recorded_hotkeys, hotkeyid
    recording, recordinghotkeys = False, False
    newmakro = []
    recorded_hotkeys = set()
    hotkeyid = 0
    statusvar.set("Status: ready")
    
def confirm(button):
    if debug: print("recording finished.")
    global recording, recordinghotkeys
    if recording == True:
        recording = False
        if button == "hotkey" and newmakro[0].get("vk") in default_combinations["record"]:
            del newmakro[0]
        
        while button == "hotkey" and newmakro[len(newmakro)-1].get("vk") in default_combinations["record"]:
            del newmakro[len(newmakro)-1]
            

        while newmakro[0]["action"] == "release":
            del newmakro[0] #entfernt überschüssige button releases vom Anfang
        #for step in newmakro:

        if button == "button" and newmakro[len(newmakro)-2]["mok"] == "m":
            del newmakro[len(newmakro)-1]
            del newmakro[len(newmakro)-1]


        id=0
        for makro in makros:
            try:
                if makro["id"] > id:
                    id = makro["id"]
            except KeyError as e:
                id += 1

        makros.append({
            "id": id+1,
            "name": "macro {0}".format(id+1),
            "combination": [], 
            "combinationstr": [],
            "description": "",
            "makro": newmakro
            })
        save_makros()


        #makros anzeigen
        rendermakros()
    elif recordinghotkeys:
        global hotkeyid
        global recorded_hotkeys, recorded_hotkeys_str
        save_combination(recorded_hotkeys, hotkeyid)
        hotkeyid = 0
        recordinghotkeys = False
        recorded_hotkeys, recorded_hotkeys_str = set(), set()
        rendermakros()
    else: 
        if debug: print("recording didn't get started")
    statusvar.set("Status: ready")
        

def addhotkeys(id):
    global recordinghotkeys, hotkeyid
    recordinghotkeys = True
    hotkeyid = id
    statusvar.set("Status: recording hotkeys")



#GUI
canvas = tk.Frame(root, height=700, width=1920, bg=ascblue)
canvas.pack()

title = tk.Label(canvas, text=titletext, bg=asctext, fg="white", font="Helvetica 20 bold underline")
title.place(relheight=0.1, relwidth=1)

frame = tk.Frame(canvas, bg=asclightblue)
frame.place( relwidth=1, relheight=0.75, relx= 0, rely=0.1)

status = tk.Label(canvas, textvariable=statusvar, bg=asclightblue, fg=asctext)
status.place(relwidth=1, relheight=0.05, relx= 0, rely=0.85)

makroframe = tk.Frame(frame, bg="white")
makroframe.place(relwidth=1, relheight=1, relx=0, rely=0)

buttoncontainer = tk.Frame(canvas).place()

recordButton = tk.Button(buttoncontainer, bg=ascorange, text="record", padx=10, pady=5, fg=asctext, command=record)
recordButton.place(relx=0, rely = .9, relheight=.1)

waypathcheckbutton = tk.Checkbutton(buttoncontainer, text="drag", variable=drag, offvalue=False, onvalue=True, bg=ascblue).place(relx=.2, rely=.925, relheight=.05)

abortButton = tk.Button(buttoncontainer, bg="lightgrey", text="abort", padx=10, pady=5, fg="black", command=abort)
abortButton.place(relx=0.425, rely= .9, relheight=.1)

confirmButton = tk.Button(buttoncontainer, bg=ascgreen, text="confirm", padx=10, pady=5, fg="black", command=lambda: confirm("button"))
confirmButton.place(relx=.85, rely=.9, relheight=.1)
