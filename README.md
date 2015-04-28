About
=====
This is python curses dialog library.
This dialogs library provided the following dialog

1. askFileSaveDialog
2. askYesCancelDialog
3. showMessageDialog
4. ~~progressBarDialog~~

> Note the **progressBarDialog** has some bugs, will fix it as soon as possible

#Example
```python
from cursDialog import *

# ask filename/pathname dialog, will return the inputted string
filepath = askFileSaveDialog(message='Ask file save path\njust for test', title='Ask save file Dialog')

# ask yes or cancel dialog, will return boolean
result = askYesCancelDialog(message='Ask Yes Cancel \njust for test', title='Ask Yes Cancel Dialog', title_attr=curses.A_STANDOUT|curses.A_BOLD)

# show message dialog, only display message
showMessageDialog(message='Display message for test ', title='Display message ')
```

#Platform
This library can only run on Unix like and Linux like OS, in Windows you need to install a curses alternative patch because the curses library not supported in Windows.

#Screenshots
####Show Message Dialog
<img src="https://raw.github.com/jacklam718/cursDialogs/master/screenshots/display-message-dialog.png" alt="Show Message Dialog">

####Ask Yes Or Cancel Dialog
<img src="https://raw.github.com/jacklam718/cursDialogs/master/screenshots/ask-yes-cancel-dialog.png" alt="Ask Yes Or Cancel Dialog">

####Ask Save File Dialog
<img src="https://raw.github.com/jacklam718/cursDialogs/master/screenshots/ask-save-dialog.png" alt="Ask Save File Dialog">
