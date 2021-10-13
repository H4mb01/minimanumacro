# minimanumacro
A program to record and play macros on your PC

## Warning
Work in progress.  
Usage at own risk!

## Default Keybindings
Start recording a new macro: Alt + R  
Abort recording of a new macro: Alt + A  
Confirm recorded macro: Alt + C  
Toggle drag option: Alt + D  
to cancel a running macro double-tap the ESC key

## Usage
1. Start recording a macro using the 'record' button or the hotkey (default Alt + R).  
2. Check the "drag" checkbox, if you want to be able to drag with the mouse. If checked all movements of the mouse will be recorded, allowing you to drag in Windows. If unchecked only mouseclicks will be recorded. 
2. Finish the recording by pressing the 'confirm' button or the hotkey (default Alt + C).  
(You can about the recording by pressing the 'abort' button or using the hotkey (default Alt + A))
3. set a Hotkey-combination für your new added macro if you want.  
Press the buttons one by one and confirm with 'Enter' or cancel with 'ESC'.
4. play the macro at any time using the 'run' button next to it or pressing your own set of hotkeys  

## Customize Default Hotkeys
For customizing the hotkeys for recording, abort, confirm and toggle drag you have to use settings.json.  
Please note that you have to know the virtual key number of any key you want to use and insert them in dezimal (not Hex).

## Additional Important Information
- Every keypress recorded as a macro will be stored in readable JSON Data on your device.
Please keep this in mind when using a macro to login with a password.
- No logging will be recorded
- Via GUI deleted macros will be deleted permanently and cannot be restored
- If you want to edit a macro after recording you can edit it in the JSON file directly, but to apply the changes you have to restart the application
- Please only edit the JSON files if you know what you are doing. You could potentially lose all your macros permanently if you do something wrong :)