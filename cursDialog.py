#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import curses
import sys
encoding = sys.getdefaultencoding( )

class CommonDialog:
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

    def left_right(self, max):
        self.win.refresh( )
        key = self.win.getch( )
        if key == curses.KEY_LEFT and self.focus != 0:
            self.focus -= 1
        elif key == curses.KEY_RIGHT and self.focus != max-1:
            self.focus += 1
        elif key == ord('\n'):
            self.enterKey = True

class AskYesCancel(CommonDialog):
    def yescancel(self):
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
            self.left_right(2)
        if self.focus==0: return True
        return False

class AskFileSave(CommonDialog):
    def filesave(self):
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

            self.left_right(len(option))

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

class ShowMessage(CommonDialog):
    def showmessage(self):
        if self.title: self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, self.msg_attr)
        rectangle(self.win, 8, int(self.x/2-2), 2, 3, self.opt_attr | self.focus_attr)
        self.win.addstr(9, int(self.x/2-1), 'Ok',    self.opt_attr  | self.focus_attr)
        if self.win.getch( ) != ord('\n'):  self.showmessage( )

def showmessage(**option):
    return ShowMessage(**option).showmessage( )

def askfilesave(**option):
    return AskFileSave(**option).filesave( )

def askyescancel(**option):
    return AskYesCancel(**option).yescancel( )

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
    # test
    import traceback
    try:
        stdscr = curses.initscr( )
        rec = askfilesave(message='Ask file save path\njust for test', title='Ask save file Dialog')
        rec = askyescancel(message='Ask Yes Cancel \njust for test', title='Ask Yes Cancel Dialog', title_attr=curses.A_STANDOUT|curses.A_BOLD)
        rec = showmessage(message='Display message for test ', title='Display message ')
        curses.endwin( )
        print(rec)
        input('Press enter exit!')
    except:
        curses.endwin( )
        traceback.print_exc()
        input( )
