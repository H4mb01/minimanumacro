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
gui.combinations = [set((Key.ctrl_l, Key.alt_l, Key.space)),set((Key.ctrl_r, Key.shift))]
gui.newmakro = []
gui.makros = []
gui.hotkeys = {}


#json
with open('makros.json') as f:
    data = json.load(f)
    gui.makros = data["makros"]


#own functions
def neuerEintrag(mok, key, action, *position, scroll=(0,0)):
    now = time.time()
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
        if key == "middle":
            dx, dy = scroll
            new['dx'] = dx
            new['dy'] = dy
        print(new)

    return new










#Mouse inputs
def on_move(x,y):
    if gui.recording:
        if gui.drag.get():
            tx, ty = maus.position
            gui.newmakro.append(neuerEintrag("m", "position", "move", tx, ty))

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
    if gui.recording:
        tx, ty = maus.position
        gui.newmakro.append(neuerEintrag("m", "middle", "scroll", tx, ty, scroll=(dx, dy)))



#keyboard inputs
def on_press(key):
    print(key)
    #vk=gui.get_vk(key)
    #gui.pressed_vks.add(vk)
    if len(gui.currentcombination) >3:
        gui.currentcombination = set()
    gui.currentcombination.add(str(key))
    print("currentcombination: {0}".format(gui.currentcombination))
    for combination in gui.combination_to_id:

        print("is_combination_pressed: {0}".format(gui.is_combination_pressed(combination)))
        if gui.is_combination_pressed(combination):
            gui.runmakro(gui.combination_to_id[combination])

        #with vks
        '''if gui.is_vkcombination_pressed(combination):
            gui.runmakro(gui.combination_to_id[combination])'''
    
    if gui.recording:
        gui.newmakro.append(neuerEintrag("k", key, "press"))

    if gui.recordinghotkeys:
        gui.recorded_hotkeys.add(str(key))

def on_release(key):
    '''vk=gui.get_vk(key)
    gui.pressed_vks.remove(vk)'''
    try:
        gui.currentcombination.remove(str(key))
    except KeyError:
        pass
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
gui.get_combination()
gui.rendermakros()
gui.root.mainloop()

keyboardListener.stop()
mouseListener.stop()