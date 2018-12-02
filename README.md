## Python Curses Dialog

This is python curses dialog library.
This library provided the following dialogs

1. progressBarDialog
2. askFileSaveDialog
3. askYesCancelDialog
4. showMessageDialog

## Preview
<img src="https://raw.githubusercontent.com/jacklam718/cursesDialog/master/.github/curses-dialog.gif" width="600">

## Example
```python
from cursDialog import *

# use curses you need init the curses first
stdscr = curses.initscr( )

# progress bar dialog
maxValue = 100
progress = progressBarDialog(maxValue=maxValue, message='Progressbar for test', title='Progress test')
for i in range(maxValue+1):
    progress(i)

# progress bar dialog with colored, Note your terminal must support color
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, 0)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
COLOR_RED    = curses.color_pair(1)
COLOR_GREEN  = curses.color_pair(2)
progress = progressBarDialog(maxValue=maxValue, message='Progressbar for test', title='Progress test', clr1=COLOR_RED, clr2=COLOR_GREEN)

# ask filename/pathname dialog, will return the inputted string
filepath = askFileSaveDialog(message='Ask file save path\njust for test', title='Ask save file Dialog')

# ask yes or cancel dialog, will return boolean
result = askYesCancelDialog(message='Ask Yes Cancel \njust for test', title='Ask Yes Cancel Dialog', title_attr=curses.A_STANDOUT|curses.A_BOLD)

# show message dialog, only display message
showMessageDialog(message='Display message for test ', title='Display message ')
```


## Platform
- This library can only run on Unix like and Linux like OS, in Windows you need to install a curses alternative patch because the curses library not supported in Windows.

- Python3.x
