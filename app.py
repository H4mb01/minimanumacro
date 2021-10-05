import gui
import time
import json
from typing import Text
from pynput import mouse, keyboard
from pynput.mouse import Controller as MC
from pynput.keyboard import Controller as KC
from pynput.mouse import Button as Mousebutton
from pynput.keyboard import Key

maus = MC()


combo = gui.combo
gui.recording = False
gui.combinations = [set((Key.ctrl_l, Key.alt_l)),set((Key.ctrl_r, Key.shift))]
currentcombination = set()
gui.newmakro = []
gui.makros = []
gui.hotkeys = {}


#json
with open('makros.json') as f:
    data = json.load(f)
    gui.makros = data["makros"]


#own functions
def neuerEintrag(mok, key, action, *position):
    now = time.time()
    print(gui.newmakro)
    print("new entry: mok: {0}, key: {1}, action: {2}, position: {3}".format(mok, key, action, position))
    new = {
        "mok": mok,
        "key": str(key),
        "time": now,
        "action": action,
    }
    if mok == "m":
        (x,y) = position
        new['x'] = x
        new['y'] = y
        print(new)
    return new










#Mouse inputs
def on_move(x,y):
    pass

def on_click(x, y, button, pressed):
    print('{0} {1} at {2}'.format(
        'Pressed' if pressed else 'Released', button,
        (x, y)))
    print("mouse.postion = ", maus.position)
    if gui.recording:
        tx, ty = maus.position
        gui.newmakro.append(neuerEintrag("m", button, 'press' if pressed else 'release', tx, ty ))
    if gui.recordinghotkeys:
        pass

def on_scroll(x, y, dx, dy):
    pass


#keyboard inputs
def on_press(key):
    global combo
    
    for combination in gui.combinations:

        if key in combination:
            currentcombination.add(key)
            if all(k in currentcombination for k in combination):
                print("ALL ARE ACTIVE!")
                combo = True

    
    if gui.recording:
        gui.newmakro.append(neuerEintrag("k", key, "press"))


def on_release(key):
    try:
        currentcombination.remove(key)
    except KeyError:
        pass
    global combo
    if combo: 
        gui.record()
        combo = False
    else:
        if gui.recording:
            gui.newmakro.append(neuerEintrag("k", key, "release"))



#listening...
keyboardListener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboardListener.start()

mouseListener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
mouseListener.start()



#main Program
gui.rendermakros()
gui.root.mainloop()

keyboardListener.stop()
mouseListener.stop()