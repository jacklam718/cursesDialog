#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import curses
import sys

encoding = sys.getdefaultencoding( )

class CursBaseDialog:
    def __init__(self, **options):
        self.maxy, self.maxx = curses.LINES, curses.COLS
        self.win = curses.newwin(12, 56, int((self.maxy/2)-6) , int((self.maxx/2)-28))
        self.win.box( )
        self.y, self.x  = self.win.getmaxyx( )
        self.title_attr = options.get('title_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.msg_attr   = options.get('msg_attr',   curses.A_BOLD)
        self.opt_attr   = options.get('opt_attr',   curses.A_BOLD)
        self.focus_attr = options.get('focus_attr', curses.A_BOLD | curses.A_STANDOUT)
        self.title      = options.get('title',      curses.A_NORMAL)
        self.message    = options.get('message', '' )
        self.win.addstr(0, 0, ' '*56, self.title_attr)
        self.win.keypad(1)
        self.focus   = 0
        self.enterKey   = False
        self.win.keypad(1)
        curses.curs_set(0)
        curses.noecho( )
        curses.cbreak( )

    def left_right_key_event_handler(self, max):
        self.win.refresh( )
        key = self.win.getch( )
        if key == curses.KEY_LEFT and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_RIGHT and self.focus != max-1:
            self.focus += 1
        elif key == ord('\n'):
            self.enterKey = True

class AskYesCancelDialog(CursBaseDialog):
    def askYesOrCancel(self):
        if self.title: self.win.addstr(0, int(self.x/2 - len(self.title)/2), self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg,  self.msg_attr)
        option = ('Yes   ', 'Cancel')
        rectangle(self.win, 8, 13-1, 2, len(option[0])+1, self.opt_attr)
        rectangle(self.win, 8, 34-1, 2, len(option[1])+1, self.opt_attr)
        pos_x = [13, 34]
        while self.enterKey != True:
            if self.focus == 0:
                self.win.addstr(9, 13, ' Yes  ',    self.focus_attr    | self.opt_attr)
            else:
                self.win.addstr(9, 13, ' Yes  ',    self.opt_attr)

            if self.focus == 1:
                self.win.addstr(9, 34, 'Cancel', self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, 34, 'Cancel', self.opt_attr)
            for i in range(2):
                if i != self.focus: rectangle(self.win, 8, pos_x[i]-1, 2, len(option[i])+1, curses.A_NORMAL | self.opt_attr)
                else: rectangle(self.win, 8, pos_x[self.focus]-1, 2, len(option[self.focus])+1, self.focus_attr | self.opt_attr)
            self.left_right_key_event_handler(2)
        if self.focus==0: return True
        return False

class AskFileSaveDialog(CursBaseDialog):
    def fileSave(self):
        if self.title: self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, self.msg_attr)

        option = ('Save as', 'Save   ', 'Cancel ')
        space  = int(self.x/6)
        pos_x  = [ ]

        for i in option:
            pos_x.append(space)
            rectangle(self.win, 8, space-1, 2, len(i)+1, self.opt_attr)
            space = space + len(i) + 8

        while self.enterKey != True:
            if self.focus == 0:
                self.win.addstr(9, pos_x[0], 'Save as', self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, pos_x[0], 'Save as', self.opt_attr)

            if self.focus == 1:
                self.win.addstr(9, pos_x[1], ' save  ',   self.focus_attr | self.opt_attr)
            else:
                self.win.addstr(9, pos_x[1], ' Save  ',   self.opt_attr)

            if self.focus == 2:
                self.win.addstr(9, pos_x[2], 'Cancel ',  self.focus_attr | self.opt_attr)

            else:
                self.win.addstr(9, pos_x[2], 'Cancel ',  self.opt_attr)

            for i in range(len(option)):
                if i != self.focus: rectangle(self.win, 8, pos_x[i]-1, 2, len(option[i])+1, curses.A_NORMAL | self.opt_attr)
                else:  rectangle(self.win, 8, pos_x[self.focus]-1, 2, len(option[self.focus])+1, self.focus_attr | self.opt_attr)

            self.left_right_key_event_handler(len(option))

        if self.focus == 0:
            curses.echo()
            curses.cbreak( )
            curses.curs_set(1)
            self.win.keypad(False)
            self.win.addstr(4, 2, 'Please enter save path in the following:')
            self.win.addstr(6, 2, ' '*30, curses.A_UNDERLINE)
            filepath = self.win.getstr(6, 2, curses.A_BOLD).decode('latin1')

        elif self.focus == 1:
            filepath = '.'
        else:
            filepath = None
        return filepath

class ShowMessageDialog(CursBaseDialog):
    def showMessage(self):
        if self.title: self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, self.msg_attr)
        rectangle(self.win, 8, int(self.x/2-2), 2, 3, self.opt_attr | self.focus_attr)
        self.win.addstr(9, int(self.x/2-1), 'Ok',    self.opt_attr  | self.focus_attr)
        if self.win.getch( ) != ord('\n'):  self.showMessage( )

class ProgressBarDialog(CursBaseDialog):
    def __init__(self, **options):
        super(self.__class__, self).__init__(**options)
        self.clr1 = options.get("clr1", curses.A_NORMAL)
        self.clr2 = options.get("clr2", curses.A_NORMAL)
        self.maxValue = options.get("maxValue")
        self.blockValue = 0
        self.win.addstr(0, 0, ' '*self.x, curses.A_STANDOUT)

        # Display message
        self.displayMessage( )

        # Draw the ProgressBar Box
        self.drawProgressBarBox ( )

        self.win.refresh( )

    def drawProgressBarBox(self):
        from curses.textpad import rectangle as rect
        self.win.attrset(self.clr1 | curses.A_BOLD)
        hight, width = 2, 50
        y, x = 7, 3
        rect(self.win, y-1, x-1, hight+y, width+x)

    def displayMessage(self):
        if self.title:
            self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, curses.A_BOLD | curses.A_STANDOUT)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, curses.A_BOLD)

    def progress(self, currentValue):
        percentcomplete = int((100 * currentValue / self.maxValue))
        blockValue      = int(percentcomplete/2)
        maxValue     = str(self.maxValue)
        currentValue = str(currentValue)

        self.win.addstr(9, int(self.x/2-len(maxValue))-2, "%s of %s" % (currentValue, maxValue))

        for i in range(self.blockValue, blockValue):
            self.win.addstr(7, i+3, '▋', self.clr2 | curses.A_BOLD)
            self.win.addstr(8, i+3, '▋', self.clr2 | curses.A_NORMAL)

        if percentcomplete == 100:
            self.win.addstr(10, int(self.x/2)-3,  'Finish', curses.A_STANDOUT)
            self.win.getch( )
        self.blockValue = blockValue
        self.win.refresh( )

def showMessageDialog(**options):
    return ShowMessageDialog(**options).showMessage( )

def askFileSaveDialog(**options):
    return AskFileSaveDialog(**options).fileSave( )

def askYesCancelDialog(**options):
    return AskYesCancelDialog(**options).askYesOrCancel( )

def progressBarDialog(**options):
    return ProgressBarDialog(**options).progress

def rectangle(win, begin_y, begin_x, height, width, attr):
    win.vline(begin_y,    begin_x,       curses.ACS_VLINE, height, attr)
    win.hline(begin_y,        begin_x,   curses.ACS_HLINE, width , attr)
    win.hline(height+begin_y, begin_x,   curses.ACS_HLINE, width , attr)
    win.vline(begin_y,    begin_x+width, curses.ACS_VLINE, height, attr)
    win.addch(begin_y,        begin_x,       curses.ACS_ULCORNER,  attr)
    win.addch(begin_y,        begin_x+width, curses.ACS_URCORNER,  attr)
    win.addch(height+begin_y, begin_x,       curses.ACS_LLCORNER,  attr)
    win.addch(begin_y+height, begin_x+width, curses.ACS_LRCORNER,  attr)
    win.refresh( )

if __name__ == '__main__':
    from time import sleep

    # test
    import traceback
    try:
        # init curses screen
        stdscr = curses.initscr( )

        curses.start_color()
        # stdscr.use_default_colors()
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_RED, 0)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_BLUE,  0)

        COLOR_RED    = curses.color_pair(1)
        COLOR_GREEN  = curses.color_pair(2)
        COLOR_BLUE   = curses.color_pair(3)
        COLOR_NORMAL = curses.color_pair(4)

        askFileSaveDialog(message='Ask file save path\njust for test', title='Ask save file Dialog')
        askYesCancelDialog(message='Ask Yes Cancel \njust for test', title='Ask Yes Cancel Dialog', title_attr=curses.A_STANDOUT|curses.A_BOLD)
        showMessageDialog(message='Display message for test ', title='Display message ')

        maxValue = 100
        progress = progressBarDialog(maxValue=maxValue, message='Progressbar for test', title='Progress test', clr1=COLOR_RED, clr2=COLOR_GREEN)
        for i in range(maxValue+1):
            progress(i)
            sleep(0.01)

        curses.endwin( )
    except:
        curses.endwin( )
        traceback.print_exc()
