#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

# from curses.textpad import rectangle
import curses
import cursBaseDialog
import sys

encoding = sys.getdefaultencoding( )

class AskYesCancelDialog(cursBaseDialog.CursBaseDialog):
    def yesCancel(self):
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

class AskFileSaveDialog(cursBaseDialog.CursBaseDialog):
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

class ShowMessageDialog(cursBaseDialog.CursBaseDialog):
    def showMessage(self):
        if self.title: self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, self.title_attr)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, self.msg_attr)
        rectangle(self.win, 8, int(self.x/2-2), 2, 3, self.opt_attr | self.focus_attr)
        self.win.addstr(9, int(self.x/2-1), 'Ok',    self.opt_attr  | self.focus_attr)
        if self.win.getch( ) != ord('\n'):  self.showMessage( )

class ProgressBarDialog:
    def __init__(self, finalcount, message="", title=None, clr1=None, clr2=None, y=32, x=80):
        self.win = curses.newwin(12, 56, int(y/2)-6, int(x/2)-28)
        self.win.box( )
        self.clr1 = clr1 or curses.A_NORMAL
        self.clr2 = clr2 or curses.A_NORMAL
        self.y, self.x  = self.win.getmaxyx( )
        self.finalcount = finalcount
        self.blockcount = 0
        self.win.addstr(0, 0, ' '*self.x, curses.A_STANDOUT)
        # Display some message
        self.message = message
        self.title   = title
        self.display_message( )
        # Draw the interface
        self.draw_interface ( )
        self.win.refresh( )

    def draw_interface(self):
        self.win.attrset(self.clr1 | curses.A_BOLD)
        hight, width = 2, 50
        y, x = 7, 3
        rectangle(self.win, y-1, x-1, hight+y, width+x)

    def display_message(self):
        if self.title:
            self.win.addstr(0, int(self.x/2-len(self.title)/2), self.title, curses.A_BOLD | curses.A_STANDOUT)
        for (i, msg) in enumerate(self.message.split('\n')):
            self.win.addstr(i+1, 2, msg, curses.A_BOLD)

    def progress(self, count):
        percentcomplete = int((100*count/self.finalcount))
        blockcount      = int(percentcomplete/2)
        self.count_of_final(count)
        for i in range(self.blockcount, blockcount):
            self.win.addstr(7, i+3, '█', self.clr2 | curses.A_BOLD)
            self.win.addstr(8, i+3, '█', self.clr2 | curses.A_NORMAL)

        if percentcomplete == 100:
            self.win.addstr(10, int(self.x/2)-3,  'Finish', curses.A_STANDOUT)
            self.win.getch( )
        self.blockcount = blockcount
        self.win.refresh( )

    def count_of_final(self, count):
        final = str(self.finalcount)
        count = str(count)
        self.win.addstr(9, int(self.x/2-len(final))-2, "%s of %s" % (count, final))
        return


def showMessageDialog(**option):
    return ShowMessageDialog(**option).showMessage( )

def askFileSaveDialog(**option):
    return AskFileSaveDialog(**option).fileSave( )

def askYesCancelDialog(**option):
    return AskYesCancelDialog(**option).yesCancel( )

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
        rec = askFileSaveDialog(message='Ask file save path\njust for test', title='Ask save file Dialog')
        rec = askYesCancelDialog(message='Ask Yes Cancel \njust for test', title='Ask Yes Cancel Dialog', title_attr=curses.A_STANDOUT|curses.A_BOLD)
        rec = showMessageDialog(message='Display message for test ', title='Display message ')
        curses.endwin( )
        print(rec)
        input('Press enter exit!')
    except:
        curses.endwin( )
        traceback.print_exc()
        input( )


    # from time import sleep
    # stdscr = curses.initscr( ) ; curses.curs_set(0)
    # y, x   = stdscr.getmaxyx( ); dst = 100
    # pb = Progressbar(dst, 'Progressbar for test', 'Progress test', y, x)
    # for i in range(dst+1):
    #     pb.progress(i)
    #     sleep(0.1)
