import os
import tkinter as tk
from PIL import Image, ImageTk
from gamesearch import gui as search_gui  
from info import show_game_details, show_game_image  
from constants import WINDOW_SIZE, NAV_BAR_HEIGHT
from statistics import main as stats_main  


BASE_DIR = os.path.dirname(__file__)
GUI_DIR = os.path.join(BASE_DIR, "GUI")
STEAM_LOGO_PATH = os.path.join(GUI_DIR, "/Users/dewan/School/test steam/steam.logo.png")
BACKGROUND_IMAGE_PATH = os.path.join(GUI_DIR, "/Users/dewan/School/test steam/steambg.png")
WINDOW_SIZE = (1440, 800)
LOGO_SIZE = (100, 50)
BACKGROUND_SIZE = (1440, 1080)
NAV_BAR_HEIGHT = 100
STEAM_BG_COLOR = "#121D28"

def load_image(path, size=None):
    image = Image.open(path).convert("RGBA")
    if size:
        image = image.resize(size)
    return ImageTk.PhotoImage(image)

class PaginationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Project")

        self.total_pages = 2 
        self.current_page = 1

        self.button_frame = tk.Frame(self.root, bg=STEAM_BG_COLOR)
        self.button_frame.place(x=0, y=0, width=WINDOW_SIZE[0], height=100)

        # self.prev_button = tk.Button(self.button_frame, text="←", command=self.previous_page, relief="flat",
        #                              bg=self.root.cget('bg'), width= 1, height=1)
        # self.next_button = tk.Button(self.button_frame, text="→", command=self.next_page, relief="flat",
        #                              bg=self.root.cget('bg'), width= 1, height=1)

        self.home_button = tk.Button(self.button_frame, text="Home", command=lambda: self.navigate_page("Home"),
                                     relief="flat", bg=self.root.cget('bg'), width= 5, height=2)
        self.stats_button = tk.Button(self.button_frame, text="Stats", command=lambda: self.navigate_page("Stats"),
                                      relief="flat", bg=self.root.cget('bg'), width= 5, height=2)

        # self.prev_button.place(x=10, y=60)
        # self.next_button.place(x=55, y=60)
        self.home_button.place(x=20, y=60)
        self.stats_button.place(x=100, y=60)

        self.page_label = tk.Label(self.root, text=f"Page {self.current_page} of {self.total_pages}", bg=STEAM_BG_COLOR,
                                   fg="white", font=('Helvetica', 12, 'bold'))
        self.page_label.place(x=(WINDOW_SIZE[0] - 150) / 2, y=WINDOW_SIZE[1] / 2 - 25, width=150, height=30)

        # self.update_buttons()
        self.update_underline("Home")

        self.add_logo()

    def add_logo(self):
        logo_image = load_image(STEAM_LOGO_PATH, LOGO_SIZE)
        logo_label = tk.Label(self.button_frame, image=logo_image, bg=STEAM_BG_COLOR)
        logo_label.image = logo_image
        logo_label.place(x=5, y=5)

    def navigate_page(self, page_name):
        for widget in self.root.winfo_children():
            if widget != self.button_frame:
                widget.destroy()

        if page_name == "Home":
            self.current_page = 1
            search_gui(self.root) 
        elif page_name == "Stats":
            self.current_page = 2
            self.show_statistics(self.root) 

        self.update_ui()
        self.update_underline(page_name)

    def show_statistics(self, parent):
        stats_frame = tk.Frame(parent, bg=STEAM_BG_COLOR)
        stats_frame.place(x=50, y=150, width=600, height=400) 
        stats_main()



    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_ui()
        if self.current_page == 1:
            self.update_underline("Home")
        elif self.current_page == 2:
            self.update_underline("Stats")

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_ui()
        if self.current_page == 2:
            self.update_underline("Stats")

    def update_ui(self):
        self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")
        # self.update_buttons()

    def update_buttons(self):
        if self.current_page == 1:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        if self.current_page == self.total_pages:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def update_underline(self, page_name):
        self.home_button.config(font=('Helvetica', 10))
        self.stats_button.config(font=('Helvetica', 10))

        if page_name == "Home":
            self.home_button.config(font=('Helvetica', 10, 'underline'))
        elif page_name == "Stats":
            self.stats_button.config(font=('Helvetica', 10, 'underline'))

def create_app():
    app = tk.Tk()
    app.title("Steam Project")
    app.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}") 
    app.config(bg=STEAM_BG_COLOR)
    return app

def add_background(app, image_path):
    background_image = load_image(image_path, BACKGROUND_SIZE)
    background_label = tk.Label(app, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0)
    return background_label

def main():
    app = create_app()
    add_background(app, BACKGROUND_IMAGE_PATH)
    pagination_app = PaginationApp(app)

    app.update_idletasks()  
    search_gui(pagination_app.root) 

    app.mainloop()

if __name__ == "__main__":
    main()