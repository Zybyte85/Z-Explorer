import curses
import os
import startfile

def print_menu(stdscr, selected_row_idx, dir):
    global menu
    menu = os.listdir(dir)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    start_idx = max(0, selected_row_idx - (h // 2))
    end_idx = start_idx + h
    for idx, row in enumerate(menu[start_idx:end_idx]):
        y = idx
        x = 0
        if idx == selected_row_idx - start_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def main(stdscr):
    # Set initial menu
    cur_dir = "/"  #os.getcwd()

    stdscr.keypad(True)

    # Turn off cursor blinking
    curses.curs_set(0)

    # Color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Specify the current selected row
    current_row = 0

    # Print the initial menu
    print_menu(stdscr, current_row, cur_dir)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_BACKSPACE: #or curses.KEY_LEFT:
            cur_dir = os.path.dirname(cur_dir)
            # Update the menu
            print_menu(stdscr, current_row, cur_dir)
        elif key == curses.KEY_ENTER or curses.KEY_RIGHT:
            selected_item = menu[current_row]
            if os.path.isdir(os.path.join(cur_dir, selected_item)):
                cur_dir = os.path.join(cur_dir, selected_item)
                # Update the menu
                print_menu(stdscr, current_row, cur_dir)
            else:
                startfile(os.path.dirname(cur_dir))

        # Refresh the screen after each key press
        print_menu(stdscr, current_row, cur_dir)

curses.wrapper(main)
