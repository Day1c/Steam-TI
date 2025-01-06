import tkinter as tk
from tkinter import ttk
import json
import requests
from PIL import Image, ImageTk
from io import BytesIO

# Load the JSON data
with open("/Users/dewan/School/steam.json", "r") as file:
    games = json.load(file)

def get_game_image(appid):
    image_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"
    try:
        response = requests.get(image_url)
        response.raise_for_status() 
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        image = image.resize((400, 300))  # maat
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image for appid {appid}: {e}")
        return None


def show_game_details(game, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy() 
    
    # format
    details_text = f"""
    Name: {game['name']}
    Release Date: {game['release_date']}
    Developer: {game['developer']}
    Publisher: {game['publisher']}
    Platforms: {game['platforms']}
    Categories: {game['categories']}
    Genres: {game['genres']}
    Price: ${game['price']}
    Positive Ratings: {game['positive_ratings']}
    Negative Ratings: {game['negative_ratings']}
    Average Playtime: {game['average_playtime']} minutes
    """

    label = tk.Label(parent_frame, text=details_text, justify=tk.LEFT, anchor="w", font=("Arial", 10), bg="#121D28", fg="white")
    label.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

def show_game_image(game, parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()  

    appid = game.get("appid")  # fetch the image
    if not appid:
        tk.Label(parent_frame, text="Image not available", fg="white", bg="#121D28").pack()
        return

    image = get_game_image(appid)
    if image:
        label = tk.Label(parent_frame, image=image, bg="#121D28")
        label.image = image  

        label.pack(side=tk.TOP, padx=10, pady=160)  #position of pictures
    else:
        tk.Label(parent_frame, text="Image not available", fg="white", bg="#121D28").pack()


def display_game_info(game, details_frame, image_frame):
    show_game_details(game, details_frame)
    show_game_image(game, image_frame)