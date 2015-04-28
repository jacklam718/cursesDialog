#!/usr/bin/env python3
# --*-- coding: utf-8 --*--

import curses

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
