About
=====
This is python curses dialogs library.
This dialogs library provided the following dialogs

1. askFileSaveDialog
2. askYesCancelDialog
3. showMessageDialog
4. ~~progressBarDialog~~

> Note the **progressBarDialog** has some bugs, will fix it as soon

#Usage
```python
# input filepath dialog, will return the inputted string
filepath = askFileSaveDialog(message='Ask file save path\njust for test', title='Ask save file Dialog')

# ask yes or cancel dialog, will return boolean
result = askYesCancelDialog(message='Ask Yes Cancel \njust for test', title='Ask Yes Cancel Dialog', title_attr=curses.A_STANDOUT|curses.A_BOLD)

# show message dialog, only display message
showMessageDialog(message='Display message for test ', title='Display message ')
```
