import tkinter as tk
import pyautogui as pg
from pynput import keyboard
from pynput.keyboard import Key, Listener
import time
import random
import json
import keyboard

def toggle_cell(row, col):
    global start_row, start_col, end_row, end_col

    if shift_pressed:
        if start_row is None or start_col is None:
            start_row = row
            start_col = col
        else:
            end_row = row
            end_col = col
            select_area()
    else:
        if grid[row][col] == 1:
            grid[row][col] = 0
            canvas.itemconfig(cells[row][col], fill='white')
        else:
            grid[row][col] = 1
            canvas.itemconfig(cells[row][col], fill='black')


def select_area():
    min_row = min(start_row, end_row)
    max_row = max(start_row, end_row)
    min_col = min(start_col, end_col)
    max_col = max(start_col, end_col)

    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if grid[i][j] == 0:
                grid[i][j] = 1
                canvas.itemconfig(cells[i][j], fill='black')


def on_shift_press(event):
    global shift_pressed
    shift_pressed = True


def on_shift_release(event):
    global shift_pressed, start_row, start_col, end_row, end_col
    shift_pressed = False
    start_row = None
    start_col = None
    end_row = None
    end_col = None


def create_grid(rows, cols, cell_size):
    for i in range(rows):
        for j in range(cols):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            cell = canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='gray', width=1)
            cells[i][j] = cell
            canvas.tag_bind(cell, '<Button-1>', lambda event, r=i, c=j: toggle_cell(r, c))


def depot():
    y = 588
    x = 1272
    pg.keyDown('ctrl')
    for yy in range(rows):
        for xx in range(cols):
            if grid[yy][xx] == 1:
                clicker = random.randint(50, 55)
                pg.moveTo((x + 26 + (xx * clicker)), (y + 26 + (yy * clicker)))
                pg.click((x + 26 + (xx * clicker)), (y + 26 + (yy * clicker)))
                sleeper = random.randint(5, 10) / 100
                # time.sleep(sleeper)
    pg.keyUp('ctrl')

    pass


def dump():
    pg.keyDown('shift')
    depot()
    pg.keyUp('shift')


def clear():
    for i in range(rows):
        for l in range(cols):
            grid[i][l] = 0
            canvas.itemconfig(cells[i][l], fill='white')


def save_preset():
    save_grid = grid
    with open("data.txt") as f:
        data = f.read()
    data = json.loads(data)
    data["preset1"] = save_grid
    with open("data.txt", "w") as txt_file:
        json.dump(data, txt_file)


def load_preset():
    with open("data.txt") as f:
        data = f.read()
    data = json.loads(data)
    loaded_data = data["preset1"]
    for row in range(rows):
        for col in range(cols):
            if loaded_data[row][col] == 1:
                grid[row][col] = 1
                canvas.itemconfig(cells[row][col], fill='black')

def on_press(key):
    print(key)

rows = 5
cols = 12
cell_size = 53

root = tk.Tk()
root.title("ID")
root.geometry("+1260+270")
canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg='white')
canvas.config(bg="#000000")
canvas.pack()

cells = [[None for _ in range(cols)] for _ in range(rows)]
grid = [[0 for _ in range(cols)] for _ in range(rows)]

start_row = None
start_col = None
end_row = None
end_col = None
shift_pressed = False

create_grid(rows, cols, cell_size)

root.bind('<Shift_L>', on_shift_press)
root.bind('<KeyRelease-Shift_L>', on_shift_release)
keyboard.add_hotkey("F4",depot)

# buttons
ok_button = tk.Button(root, text="OK", command=depot)
ok_button.pack(side="left", anchor="n", expand=True, fill="x")

clear_button = tk.Button(root, text="CLEAR", command=clear)
clear_button.pack(side="left", anchor="n", expand=True, fill="x")

dump_onetab_button = tk.Button(root, text="DUMP", command=dump)
dump_onetab_button.pack(side="left", anchor="n", expand=True, fill="x")

save_preset_button = tk.Button(root, text="SAVE PRESET", command=save_preset)
save_preset_button.pack(side="left", anchor="n", expand=True, fill="x")

load_preset_button = tk.Button(root, text="LOAD PRESET", command=load_preset)
load_preset_button.pack(side="left", anchor="n", expand=True, fill="x")


root.mainloop()
