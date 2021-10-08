import tkinter as tk
import json
import time
from tkinter import *


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
#vkcombination_to_id = {}
currentcombination = set()
#pressed_vks = set()
recorded_hotkeys = set()



#filling combination_to_id
def get_combination():
    for makro in makros:
        if makro["combination"] != []:
            combination_to_id[frozenset(makro["combination"])] = makro["id"]
            

def is_combination_pressed(combination):
    return all(k in currentcombination for k in combination)

'''def is_vkcombination_pressed(combination):
    return all([get_vk(Key) in pressed_vks for Key in combination])'''

def format_combination(list):
    s = []
    for key in list:
        s.append(key.replace("Key.", ""))
    return " + ".join(s)

'''def get_vk(key):
    return key.vk if hasattr(key, 'vk') else key.value.vk'''

def findmakro(id):
    for makro in makros:
        if makro["id"] == id:
            return makro
    return None

def runmakro(id):
    global currentcombination
    currentcombination = set()
    if recording:
        print("can't play a macro while recording")
    else:
        print("running macro {0}".format(id))
        m = findmakro(id)
        makro = m["makro"]
        index = 0
        for step in makro:
            try:
                if step["mok"] == "m":
                    #all Mouse actions
                    mouse.position = (step["x"], step["y"])
                    if step['action'] == 'scroll' and step['key'] == "middle":
                        mouseaction = "mouse." + step['action'] + "(" + str(step['dx']) + "," + str(step['dy']) + ")"
                        print(mouseaction)
                        exec(mouseaction)
                    elif step["action"] != "move":
                        mouseaction="mouse." + step["action"] + "(" + step["key"] + ")"
                        exec(mouseaction)
                elif step["mok"] == "k":
                    #all keyboard actions
                    keyboardaction = "keyboard." + step["action"] + "(" + step["key"] + ")"
                    exec(keyboardaction)
                else:
                    print("neither mouse nor keyboard...?!")
            except:
                print("something didn't work *surprisedpikachuface*")
            try:
                index += 1
                print("making step")
                time.sleep(makro[index]["time"]-step["time"])
            except:
                print("makro finished")





def rendermakros():
    for widget in makroframe.winfo_children():
        widget.destroy()
    for makro in makros:
        row=makros.index(makro)
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
            text=format_combination(makro["combination"])
            )
        if makro["combination"] == []:
            makrohotkeys = tk.Button(
                makroframe, 
                fg=asctext, 
                text="add Hotkeys", 
                bg=ascorange, 
                command=lambda makro=makro: addhotkeys()
                )
        makrohotkeys.grid(
            row=row, 
            column=2, 
            padx=3, 
            ipadx=50)
        playbtn = tk.Button(
            makroframe, 
            text="run", 
            command=lambda makro=makro: runmakro(makro["id"]), 
            bg=ascgreen, 
            fg=asctext
            )
        playbtn.grid(
            row=row, 
            column=3, 
            padx=3,
            ipadx=10,
            )
        deleteBtn = tk.Button(
            makroframe, 
            text="delete",
            command=lambda makro=makro: deleteByName(makro["name"]), 
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
        messagebox = tk.Frame(makroframe, bg=asclightblue).pack()
        message1 = "Please push up to 3 buttons as hotkeys for this macro"
        message2 = ""
        label1 = tk.Label(messagebox, bg=ascblue, fg=asctext, text=message1).pack()


def deleteByName(name):
    print("trying to delete macro '{0}'".format(name))
    for makro in makros:
        if makro["name"] == name:
            print("found macro '{0}'".format(name))
            index = makros.index(makro)
            del makros[index]
            with open('makros.json', 'w') as f:
                json.dump({"makros": makros}, f, indent=2) 
            rendermakros()
            print("deleted macro '{0}'".format(name))
            break

#button actions
def record():
    if not recordinghotkeys:
        print("adding new Makro:")
        global newmakro
        newmakro = []
        global recording
        recording = True

def abort():
    print("recording aborted.")
    global recording, newmakro, recordinghotkeys
    recording, recordinghotkeys = False, False
    newmakro = []
    
def confirm():
    print("recording finished.")
    global recording
    if recording == True:
        recording = False
        while newmakro[0]["action"] == "released":
            del newmakro[0] #entfernt überschüssige button releases vom Anfang
        #for step in newmakro:

        if newmakro[len(newmakro)-2]["mok"] == "m":
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
            "description": "",
            "makro": newmakro
            })
        with open('makros.json', 'w') as f:
            json.dump({"makros": makros}, f, indent=2) 

        print("recording hotkeys...")
        global recordinghotkeys
        recordinghotkeys = True

        #makros anzeigen
        rendermakros()
    else: 
        print("recording didn't get started")

def addhotkeys():
    global recordinghotkeys
    recordinghotkeys = True
    render_message_box()
    #hier fehlt noch was


#GUI
canvas = tk.Frame(root, height=700, width=1920, bg=ascblue)
canvas.pack()

title = tk.Label(canvas, text=titletext, bg=asctext, fg="white", font="Helvetica 20 bold underline")
title.place(relheight=0.1, relwidth=1)

frame = tk.Frame(canvas, bg=asclightblue)
frame.place( relwidth=1, relheight=0.8, relx= 0, rely=0.1)

makroframe = tk.Frame(frame, bg="white")
makroframe.place(relwidth=1, relheight=1, relx=0, rely=0)

buttoncontainer = tk.Frame(canvas).place()

recordButton = tk.Button(buttoncontainer, bg=ascorange, text="record", padx=10, pady=5, fg=asctext, command=record)
recordButton.place(relx=0, rely = .9, relheight=.1)

waypathcheckbutton = tk.Checkbutton(buttoncontainer, text="drag", variable=drag, offvalue=False, onvalue=True, bg=ascblue).place(relx=.2, rely=.925, relheight=.05)

abortButton = tk.Button(buttoncontainer, bg="lightgrey", text="abort", padx=10, pady=5, fg="black", command=abort)
abortButton.place(relx=0.425, rely= .9, relheight=.1)

confirmButton = tk.Button(buttoncontainer, bg=ascgreen, text="confirm", padx=10, pady=5, fg="black", command=confirm)
confirmButton.place(relx=.85, rely=.9, relheight=.1)

