#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
#
#    The MIT License (MIT)
#
#    Copyright (c) 2013 Jack Lam <jacklam718@gmail.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

from curses.textpad import rectangle
import curses
#stdscr = curses.initscr( )

class Progressbar: 
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

if __name__ == '__main__': 
    from time import sleep
    stdscr = curses.initscr( ) ; curses.curs_set(0)
    y, x   = stdscr.getmaxyx( ); dst = 100
    pb = Progressbar(dst, 'Progressbar for test', 'Progress test', y, x) 
    for i in range(dst+1): 
        pb.progress(i) 
        sleep(0.1)

