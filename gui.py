import tkinter as tk
import json
import time


from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
from pynput.keyboard import Key, Controller

mouse = MouseController()
keyboard = Controller()

#colors
ascgreen = "#90bf38"
ascblue = "#71a2d2"
asclightblue = "#e5f4ff"
ascorange = "#e78319"
asctext = "#00315E"

root = tk.Tk()
root.title("minimanumacro")
root.geometry("500x700")
root.configure(bg=ascblue)



titletext = "minimanumacro"
combo = False
recording = False
combinations = []
newmakro = []
makros = []
hotkeys = {}
recordinghotkeys = False
drag = False



def findmakro(id):
    for makro in makros:
        if makro["id"] == id:
            return makro
    return None

def runmakro(id):
    if recording:
        print("can't play a macro while recording")
    else:
        if drag:
            #etwas neues, ich tue es beim drag
            pass
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



def addhotkeys():
    global recordinghotkeys
    recordinghotkeys = True
    #hier fehlt noch was

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
            text=makro["combination"]
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
    print("adding new Makro:")
    global newmakro
    newmakro = []
    global recording
    recording = True

def abort():
    print("recording aborted.")
    global recording, newmakro
    recording = False
    newmakro = []
    
def confirm():
    print("recording finished.")
    global recording
    if recording == True:
        recording = False
        while newmakro[0]["action"] == "released":
            del newmakro[0] #entfernt überschüssige button releases vom Anfang
        #for step in newmakro:
            #step["delay"] = (lambda a, b: a-b)()   #soll den zukünftigen delay berechnen

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
            "combination": [], 
            "makro": newmakro,
            "description": "",
            "name": "macro {0}".format(id+1),
            "id": id+1
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

waypathcheckbutton = tk.Checkbutton(buttoncontainer, text="drag", variable=drag, bg=ascblue).place(relx=.2, rely=.925, relheight=.05)

abortButton = tk.Button(buttoncontainer, bg="lightgrey", text="abort", padx=10, pady=5, fg="black", command=abort)
abortButton.place(relx=0.425, rely= .9, relheight=.1)

confirmButton = tk.Button(buttoncontainer, bg=ascgreen, text="confirm", padx=10, pady=5, fg="black", command=confirm)
confirmButton.place(relx=.85, rely=.9, relheight=.1)

