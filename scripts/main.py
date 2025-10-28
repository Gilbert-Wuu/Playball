# Import Modules ---------------------------------------------------------------
import tkinter as tk
from tkinter import *

from data_places import get_places, to_place_df
from data_weather import get_weather, to_weather_df
from data_mlb import get_mlb, to_mlb_df
from data_stadium import get_stadium, to_stadium_df

# Cities Mapping: from team to city --------------------------------------------
CITIES = {
    'NYY': ('New York', 'Bronx'),
    'BOS': ('Boston', 'Boston'),
    'TOR': ('Toronto', 'Toronto'),
    'TB': ('Tampa Bay', 'St. Petersburg'),
    'BAL': ('Baltimore', 'Baltimore'),
    'CLE': ('Cleveland', 'Cleveland'),
    'MIN': ('Minneapolis', 'Minneapolis'),
    'CWS': ('Chicago', 'Chicago1'),
    'DET': ('Detroit', 'Detroit'),
    'KC': ('Kansas City', 'Kansas City'),
    'HOU': ('Houston', 'Houston'),
    'SEA': ('Seattle', 'Seattle'),
    'TEX': ('Arlington', 'Arlington'),
    'LAA': ('Anaheim', 'Anaheim'),
    'OAK': ('Oakland', 'West Sacramento'),
    'ATL': ('Atlanta', 'Cumberland'),
    'PHI': ('Philadelphia', 'Philadelphia'),
    'MIA': ('Miami', 'Miami'),
    'NYM': ('New York', 'Queens'),
    'WSH': ('Washington, D.C.', 'Washington, D.C.'),
    'MIL': ('Milwaukee', 'Milwaukee'),
    'CHC': ('Chicago', 'Chicago2'),
    'STL': ('Saint Louis', 'Saint Louis'),
    'PIT': ('Pittsburgh', 'Pittsburgh'),
    'CIN': ('Cincinnati', 'Cincinnati'),
    'LAD': ('Los Angeles', 'Los Angeles'),
    'ARI': ('Phoenix', 'Phoenix'),
    'SD': ('San Diego', 'San Diego'),
    'SF': ('San Francisco', 'San Francisco'),
    'COL': ('Denver', 'Denver')
}


# Interface Helping Functions --------------------------------------------------
def insert_label(root, i, j, text, isTitle=False):
    """
    Insert a label into the component
    :param root: tkinter component
    :param i: grid x position
    :param j: grid y position
    :param text: label text
    :param isTitle: if true, label is styled as a title
    :return:
    """
    kwargs = {"font": ("Arial", 16, "bold")} if isTitle else {}
    label = Label(root, text=text, **kwargs)
    label.grid(row=i, column=j, sticky="nsew", padx=2, pady=5)

    return label


def insert_button(root, i, j, text, func):
    """
    Insert a button into the component
    :param root: tkinter component
    :param i: grid x position
    :param j: grid y position
    :param text: button text
    :param func: trigger function when clicking
    :return:
    """
    button = Button(root, text=text, command=lambda x=text: func(x))
    button.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)


# Reading Basic Information ----------------------------------------------------
mlb_df = to_mlb_df(get_mlb())
mlb_df["CITY"] = mlb_df["Home"].apply(lambda x: CITIES[x][1])

stadium_df = to_stadium_df(get_stadium())
stadium_df["CITY"] = stadium_df["Location"].str.split(",",
                                                      expand=True).iloc[:, 0]
stadium_df.loc[12, "CITY"] = "Chicago1"
stadium_df.loc[28, "CITY"] = "Chicago2"

all_df = mlb_df.merge(stadium_df, on="CITY")


# Initiate Window --------------------------------------------------------------
root = Tk()
root.title("MLB Dashboard")
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)

canvas1 = tk.Canvas(root, width=500)
canvas1.grid(row=0, column=0, sticky="nsew")
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas1.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas1.configure(yscrollcommand=scrollbar.set)
canvas1.bind('<Configure>',
             lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
frame1 = tk.Frame(canvas1, width=500)
canvas1.create_window((0, 0), window=frame1, anchor="nw")

canvas2 = Canvas(root, width=500, height=600)
canvas2.grid(row=1, column=0, sticky="nsew")
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas2.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
canvas2.configure(yscrollcommand=scrollbar.set)
canvas2.bind('<Configure>',
             lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))
frame2 = Frame(canvas2, width=500)
canvas2.create_window((0, 0), window=frame2, anchor="nw")

frame3 = Frame(root, width=1000)
frame3.grid(row=0, column=2, sticky="nsew", rowspan=2)
frame3.grid_propagate(False)

frame2.columnconfigure(0, weight=1)
frame2.columnconfigure(1, weight=1)
frame2.columnconfigure(2, weight=1)
frame2.columnconfigure(3, weight=1)

frame3.columnconfigure(0, weight=1)
frame3.columnconfigure(1, weight=1)
frame3.columnconfigure(2, weight=1)
frame3.columnconfigure(3, weight=1)


# Data Updating Functions ------------------------------------------------------
def refresh_frame2(city):
    """
    Search by city and update the data in frame2
    :param city: city name
    """
    for widget in frame2.winfo_children():
        widget.destroy()

    df = to_weather_df(get_weather(city))

    label = Label(frame2, text="Weather", font=("Arial", 16, "bold"),
                  justify="center", relief=RAISED)
    label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=4)

    for i, idx in enumerate(list(df.index)):
        insert_label(frame2, i + 1, 0, idx, isTitle=True)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            insert_label(frame2, i + 1, j + 1, df.iloc[i, j])

    frame2.grid_size()


def refresh_frame3(city):
    """
    Search by city and update the data in frame3
    :param city: city name
    """
    for widget in frame3.winfo_children():
        widget.destroy()

    df = to_place_df(get_places(f"{city} Foods"))
    df = df.loc[:, ["displayName", 'formattedAddress',
                    'nationalPhoneNumber', 'rating']]
    df.columns = ["Name", "Address", "Phone", "Rating"]

    label = Label(frame3, text="Foods", font=("Arial", 16, "bold"),
                  justify="center", relief=RAISED)
    label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=4)

    for j, col in enumerate(list(df.columns)):
        insert_label(frame3, 1, j, col, isTitle=True)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            insert_label(frame3, i + 2, j, df.iloc[i, j])

    frame3.grid_size()
    frame3.grid_size()


def click(x):
    """
    callback function for button clicking in frame1
    :param x: city name on the button
    """
    refresh_frame2(CITIES[x][0])
    refresh_frame3(CITIES[x][0])


# Initiate frame 1 -------------------------------------------------------------
frame1.columnconfigure(0, weight=1)
frame1.columnconfigure(1, weight=1)
frame1.columnconfigure(2, weight=1)
frame1.columnconfigure(3, weight=1)
frame1.columnconfigure(4, weight=1)
frame1.columnconfigure(5, weight=1)

label = Label(frame1, text="Schedule", font=("Arial", 16, "bold"),
              justify="center", relief=RAISED)
label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=6)

insert_label(frame1, 1, 0, "Date", isTitle=True)
insert_label(frame1, 1, 1, "Home", isTitle=True)
insert_label(frame1, 1, 2, "Away", isTitle=True)
insert_label(frame1, 1, 3, "Game", isTitle=True)
insert_label(frame1, 1, 4, "Name", isTitle=True)
insert_label(frame1, 1, 5, "Capacity", isTitle=True)

for i, row in all_df.iterrows():
    insert_label(frame1, i + 2, 0, row["Date"])
    insert_button(frame1, i + 2, 1, row["Home"], func=click)
    insert_label(frame1, i + 2, 2, row["Away"])
    insert_label(frame1, i + 2, 3, row["Game"])
    insert_label(frame1, i + 2, 4, row["Name"])
    insert_label(frame1, i + 2, 5, row["Capacity"])

# Start Main -------------------------------------------------------------------
root.mainloop()
