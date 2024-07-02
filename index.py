import curses
from random import randint
import os

# High score file
HIGHSCORE_FILE = "highscore.txt"

# Setup window
stdscr = curses.initscr()
sh, sw = stdscr.getmaxyx()
win = curses.newwin(sh, sw, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border()
win.nodelay(1)

def get_highscore():
    if not os.path.exists(HIGHSCORE_FILE):
        return 0
    with open(HIGHSCORE_FILE, 'r') as file:
        return int(file.read().strip())

def save_highscore(score):
    highscore = get_highscore()
    if score > highscore:
        with open(HIGHSCORE_FILE, 'w') as file:
            file.write(str(score))

def menu():
    win.clear()
    win.border()
    win.addstr(7, sw // 2 - 5, "1. Start Game")
    win.addstr(8, sw // 2 - 5, "2. Highscore")
    win.addstr(9, sw // 2 - 5, "3. Quit")
    win.refresh()

def display_highscore():
    highscore = get_highscore()
    win.clear()
    win.border()
    win.addstr(7, sw // 2 - 7, f"Highscore: {highscore}")
    win.addstr(9, sw // 2 - 13, "Press any key to go back")
    win.refresh()
    win.getch()

def start_game():
    global sh, sw
    sh, sw = win.getmaxyx()
    bird = [sh // 2, sw // 8]
    key = curses.KEY_RIGHT
    score = 0

    obstacles = []
    for i in range(2, sw, 20):
        obstacles.append([i, randint(1, sh - 2)])

    def draw_obstacles():
        for o in obstacles:
            win.addch(o[1], o[0], '#')
            win.addch(o[1]+1, o[0], '#')
            win.addch(o[1]-1, o[0], '#')

    def check_collision():
        if bird[0] in [0, sh-1] or bird[1] in [0, sw-1]:
            return True
        for o in obstacles:
            if o[0] == bird[1] and (bird[0] in [o[1], o[1]+1, o[1]-1]):
                return True
        return False

    while True:
        win.timeout(100)
        event = win.getch()
        if event in [curses.KEY_UP, curses.KEY_DOWN]:
            key = event

        win.clear()
        win.border()

        if key == curses.KEY_UP:
            bird[0] -= 1
        if key == curses.KEY_DOWN:
            bird[0] += 1

        win.addch(bird[0], bird[1], '*')

        for o in obstacles:
            o[0] -= 1
            if o[0] < 1:
                o[0] = sw - 2
                o[1] = randint(1, sh - 2)

        draw_obstacles()

        if check_collision():
            break

        score += 1
        win.addstr(0, 2, 'Score: ' + str(score))

    curses.endwin()
    save_highscore(score)
    print(f"Game over! Your score is {score}")
    input("Press any key to go back to menu...")
    curses.initscr()
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border()
    win.nodelay(1)

def main():
    global sh, sw
    while True:
        menu()
        choice = win.getch()
        if choice == ord('1'):
            start_game()
        elif choice == ord('2'):
            display_highscore()
        elif choice == ord('3'):
            break

    curses.endwin()

if __name__ == "__main__":
    main()
