import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to TypeSpeed!")  #, curses.color_pair(1)
    stdscr.addstr("\nPress any key to start...")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")
    stdscr.addstr("\n-press esc to quit-", curses.COLOR_RED)


    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
       
        stdscr.addstr(0, i, char, color)


def load_text():
	with open("text.txt", "r") as f:  # r as read mode
		lines = f.readlines()
		return random.choice(lines).strip()


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)
    
    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh() # so that you see it

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)

            stdscr.addstr("\nYou are an -")
            if wpm < 35:
                stdscr.addstr("below average")
            elif 35 <= wpm <= 45:
                stdscr.addstr("average")
            else:
                stdscr.addstr("above average")
            stdscr.addstr("- typer")

            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:  # ASCII of 27
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()  #pop take away the last element
        elif len(current_text) < len (target_text):
            current_text.append(key)



        
 
def main(stdscr): #stands for std screen
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)

        stdscr.addstr(3, 0, "You completed the text! Press any key to continue...")
        stdscr.addstr(5, 0, "Author: Max Chung")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)