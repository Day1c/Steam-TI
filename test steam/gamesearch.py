import tkinter as tk
from tkinter import ttk
import json
from info import show_game_details, show_game_image 
#from steam import WINDOW_SIZE, NAV_BAR_HEIGHT  # Import size constants if they are defined in Steam.py
from constants import WINDOW_SIZE, NAV_BAR_HEIGHT

with open("steam.json", "r") as file:
    games = json.load(file)

filtered_games = games


def filter_games(query):
    global filtered_games
    filtered_games = [game for game in games if query.lower() in game["name"].lower()]
    listbox.delete(0, tk.END)
    for game in filtered_games:
        listbox.insert(tk.END, game["name"])


def on_game_select(event, parent_frame):
    selected_game_name = listbox.get(listbox.curselection())
    selected_game = next(game for game in filtered_games if game["name"] == selected_game_name)
    
    details_frame = tk.Frame(parent_frame, width=WINDOW_SIZE[0] // 2, bg="#121D28")
    details_frame.place(x=0, y=NAV_BAR_HEIGHT, width=WINDOW_SIZE[0] // 2, height=WINDOW_SIZE[1] - NAV_BAR_HEIGHT)

    image_frame = tk.Frame(parent_frame, width=WINDOW_SIZE[0] // 2, bg="#121D28")
    image_frame.place(x=WINDOW_SIZE[0] // 2, y=NAV_BAR_HEIGHT, width=WINDOW_SIZE[0] // 2, height=WINDOW_SIZE[1] - NAV_BAR_HEIGHT)
    
    show_game_details(selected_game, details_frame)
    show_game_image(selected_game, image_frame)

def gui(parent_frame):
    global listbox
    frame = ttk.Frame(parent_frame, width=800, height=700)

    parent_width = parent_frame.winfo_width()
    parent_height = parent_frame.winfo_height()
    x_position = (parent_width - 800) // 2
    y_position = (parent_height - 700) // 2 + 175
    frame.place(x=x_position, y=y_position)

    search_entry = ttk.Entry(frame, font=("Arial", 14), width=40)
    search_entry.pack(fill=tk.X, pady=10)

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    listbox = tk.Listbox(
        frame, yscrollcommand=scrollbar.set, font=("Arial", 12),
        selectmode=tk.SINGLE, activestyle="none", bg="#121D28",
        fg="white", height=20, width=80
    )

    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    for game in games:
        listbox.insert(tk.END, game["name"])


    listbox.bind("<Double-1>", lambda event: on_game_select(event, parent_frame))

    def on_search_change(*args):
        query = search_entry.get()
        filter_games(query)

    search_entry.bind("<KeyRelease>", on_search_change)