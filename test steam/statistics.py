import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import psycopg2, json
from datetime import datetime

def get_median(lst):
    length = len(lst)
    lst = sorted(lst)
    if length %2 == 0:
        half = int(length/2-1)
        half2 = int(half+1)
        return (lst[half]+lst[half2])/2
    else:
        half = int(length/2)
        return float(lst[half])

def get_mean(lst):
    return sum(lst)/len(lst)

def get_gradient_descent(x, y, num_iterations=1000, learning_rate=0.0001):
    coefficients = [0, 0]
    for _ in range(num_iterations):
        for i,j in zip(x,y):
            error = (coefficients[0] + coefficients[1] * i) -j
            coefficients[0] = coefficients[0] - error * learning_rate
            coefficients[1] = coefficients[1] - i * error * learning_rate
    return coefficients

def get_time():
    format_time = datetime.now()
    return format_time.strftime('%Y-%m-%d'), format_time.strftime('%H:%M:%S')

def get_data():
    with open("steam.json", "r") as f:
        games = json.load(f)
    owner, price, playtime, ratings, release = [], [], [], [], []

    for game in games:
        if '-' in game['owners'] and game['price'] >= 0:
            people = int(game['owners'].split(' - ')[1])
            average_playtime = game['average_playtime']
            positive_rating = game['positive_ratings']
            try:
                release_date = int(game['release_date'].split(', ')[1])
            except IndexError:
                continue
            if 0 < people < 1000000 and 0 < average_playtime < 14000 and positive_rating > 0 and int(game['price']) < 250:
                owner.append(people)
                price.append(float(game['price']))
                playtime.append(int(average_playtime))
                ratings.append(int(positive_rating))
                release.append(int(release_date))
    return owner, price, playtime, ratings, release

def database(mean, median, interceptie, helling):
    try:
        connection_string = f"host = '4.158.114.13' dbname = 'steamdatabase' user = 'postgres' password = 'wachtwoord123'"
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
    except psycopg2.OperationalError:
        print("Er is een fout opgetreden. Kan niet verbinden met de database.")
    tijd = f"{get_time()[1]}"
    datum = f"{get_time()[0]}"
    query = """
        INSERT INTO statistiek (tijd, datum, gemiddelde, mediaan, interceptie, helling)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (tijd, datum, mean, median, interceptie, helling))
    conn.commit()
    cursor.close()
    conn.close()
    print("Data is successfully put in the database!")


def create_statistics_page(root, stats_frame):
    owner, price, playtime, ratings, release = get_data()

    ypoints = np.array(playtime)
    xpoints = np.array(price)
    median = get_median(ratings)
    mean = get_mean(ratings)
    interception, slope = get_gradient_descent(price, playtime)

    regression_line = interception + slope * xpoints
    # database(mean, median, interception,slope)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(xpoints, ypoints, color='blue', alpha=0.6, s=10, edgecolors='black', label='Games')
    ax.plot(xpoints, regression_line, color='red', linewidth=0.8, label=f'Regression (y={interception:.2f}+{slope:.2f}x)')

    ax.set_ylabel("Average Playtime (h)")
    ax.set_xlabel("Price ($)")
    ax.set_title("Average Playtime vs Price")

    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.axhline(y=mean, color='cyan', linestyle='-.', linewidth=0.8, label=f'Mean Playtime ({mean:.2f})')
    ax.axhline(y=median, color='magenta', linestyle='--', linewidth=0.8, label=f'Median Playtime ({median:.2f})')
    ax.legend()

    frame = tk.Frame(stats_frame)
    label = tk.Label(frame, text="Statistics")
    label.config(font=("Courier", 22))
    label.pack()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    frame.pack()


def stats_main():
    stats_frame = tk.Frame() 
    create_statistics_page(None, stats_frame)

def switch_to_statistics_page(stats_frame):

    for widget in stats_frame.winfo_children():
        widget.destroy()


    create_statistics_page(root=None, stats_frame=stats_frame)

def main():
    root = tk.Tk()
    root.geometry("800x600") 
    stats_frame = tk.Frame(root)

    stats_button = tk.Button(root, text="Stats", command=lambda: switch_to_statistics_page(stats_frame))
    stats_button.pack()

    stats_frame.pack()

    root.mainloop()

if __name__ == "__main__":
    main()