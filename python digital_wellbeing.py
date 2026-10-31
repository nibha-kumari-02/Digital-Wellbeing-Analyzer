
import tkinter as tk
from tkinter import ttk, messagebox

import ctypes
from ctypes import wintypes

import time
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
# WINDOWS APPLICATION TRACKING
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
class LASTINPUTINFO(ctypes.Structure):

    _fields_ = [
        ("cbSize", wintypes.UINT),
        ("dwTime", wintypes.DWORD)
    ]
# GET IDLE TIME
def get_idle_time():

    info = LASTINPUTINFO()

    info.cbSize = ctypes.sizeof(info)

    result = user32.GetLastInputInfo(
        ctypes.byref(info)
    )

    if result:

        current_tick = kernel32.GetTickCount()

        idle_ms = (
            current_tick - info.dwTime
        ) & 0xFFFFFFFF

        return idle_ms / 1000

    return 0
# GET ACTIVE APPLICATION
def get_active_application():

    hwnd = user32.GetForegroundWindow()

    if not hwnd:

        return "Unknown", "No active window"

    # Get actual window title
    buffer = ctypes.create_unicode_buffer(1024)
    user32.GetWindowTextW(
        hwnd,
        buffer,
        1024
    )
    window_title = buffer.value.strip()
    # Get process ID
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(
        hwnd,
        ctypes.byref(pid)
    )
    if pid.value == 0:

        return "Unknown", window_title
    # Open process
    process = kernel32.OpenProcess(
        PROCESS_QUERY_LIMITED_INFORMATION,
        False,
        pid.value
    )
    if not process:

        return "Unknown", window_title
    try:

        process_buffer = ctypes.create_unicode_buffer(
            1024
        )

        size = wintypes.DWORD(1024)
        result = kernel32.QueryFullProcessImageNameW(
            process,
            0,
            process_buffer,
            ctypes.byref(size)
        )
        if result:

            app_name = os.path.basename(
                process_buffer.value
            )

        else:

            app_name = "Unknown"

    finally:

        kernel32.CloseHandle(process)
    return app_name, window_title
# APPLICATION CATEGORY
STUDY_APPS = [
    "code.exe",
    "python.exe",
    "pythonw.exe",
    "pycharm64.exe",
    "notepad.exe",
    "notepad++.exe",
    "winword.exe",
    "powerpnt.exe",
    "excel.exe",
    "devenv.exe",
    "idea64.exe"
]
SOCIAL_APPS = [
    "whatsapp.exe",
    "telegram.exe",
    "discord.exe",
    "slack.exe"
]
ENTERTAINMENT_APPS = [
    "spotify.exe",
    "vlc.exe",
    "steam.exe",
    "epicgameslauncher.exe"
]
BROWSER_APPS = [
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "brave.exe"
]
def get_category(app):
    app = app.lower()

    if app in STUDY_APPS:

        return "Study"
    elif app in SOCIAL_APPS:

        return "Social Media"
    elif app in ENTERTAINMENT_APPS:

        return "Entertainment"
    elif app in BROWSER_APPS:

        return "Browser"
    else:

        return "Other"
# OOP CLASS
class DigitalWellbeing:

    def __init__(self):
        self.apps = {}
        self.current_app = "Unknown"
        self.current_title = "No application"
        self.last_app = None
        self.last_title = None
        self.last_time = time.monotonic()
    # TRACK APPLICATION
    def track(self):
        app, title = get_active_application()
        now = time.monotonic()
        elapsed = now - self.last_time
        idle = get_idle_time()
        # Count time when user is active
        if idle < 60 and 0 < elapsed <= 3:

            if self.last_app:
                self.save_usage(
                    self.last_app,
                self.last_title,
                elapsed
                )
        self.current_app = app
        self.current_title = title
        self.last_app = app
        self.last_title = title
        self.last_time = now
    # SAVE USAGE
    def save_usage(
        self,
        app,
        title,
        seconds
    ):
        category = get_category(app)
        if app not in self.apps:

            self.apps[app] = {
                "category": category,
                "seconds": 0,
                "titles": {}
            }
        self.apps[app]["seconds"] += seconds
        # Track window titles separately
        if title not in self.apps[app]["titles"]:

            self.apps[app]["titles"][title] = 0
        self.apps[app]["titles"][title] += seconds
    # GET APPLICATION DATA
    def get_dataframe(self):
        data = []
        for app, details in self.apps.items():
            data.append({
                "Application": app,
                "Category": details["category"],
                "Minutes": details["seconds"] / 60

            })
        return pd.DataFrame(data)
    # GET TOTAL USAGE
    def total_usage(self):
        values = [
            details["seconds"]
            for details in self.apps.values()

        ]
        return np.sum(values)
    # GET CATEGORY USAGE
    def category_usage(self, category):
        total = 0
        for app, details in self.apps.items():
            if details["category"] == category:
                total += details["seconds"]
        return total
    # GET CURRENT APPLICATION USAGE
    def current_app_usage(self):
        if self.current_app in self.apps:

            return self.apps[
                self.current_app
            ]["seconds"]
        return 0
    # FORMAT TIME
    def format_time(self, seconds):

        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )
# CREATE OBJECT
wellbeing = DigitalWellbeing()
# GUI
root = tk.Tk()

root.title(
    "Digital Wellbeing Analyzer"
)
root.geometry(
    "1150x780"
)
root.configure(
    bg="#101827"
)
root.minsize(
    950,
    650
)
# COLORS

BG = "#101827"
CARD = "#1F2937"
TEXT = "#F9FAFB"
BLUE = "#3B82F6"
GREEN = "#10B981"
PURPLE = "#8B5CF6"
ORANGE = "#F59E0B"
# HEADER
header = tk.Frame(
    root,
    bg=BG
)
header.pack(
    fill="x",
    padx=25,
    pady=20
)
tk.Label(
    header,
    text="DIGITAL WELLBEING ANALYZER",
    font=("Segoe UI", 23, "bold"),
    bg=BG,
    fg=TEXT
).pack(anchor="w")
tk.Label(
    header,
    text="Automatic Application Tracking Dashboard",
    font=("Segoe UI", 11),
    bg=BG,
    fg="#9CA3AF"
).pack(anchor="w", pady=5)

# CURRENT APPLICATION CARD
current_frame = tk.Frame(
    root,
    bg="#263248",
    padx=20,
    pady=15
)
current_frame.pack(
    fill="x",
    padx=25,
    pady=10
)
tk.Label(
    current_frame,
    text="CURRENTLY OPEN APPLICATION",
    font=("Segoe UI", 10, "bold"),
    bg="#263248",
    fg="#9CA3AF"
).pack(anchor="w")
current_app_label = tk.Label(
    current_frame,
    text="Waiting for application...",
    font=("Segoe UI", 20, "bold"),
    bg="#263248",
    fg=GREEN
)
current_app_label.pack(
    anchor="w",
    pady=5
)
current_title_label = tk.Label(
    current_frame,
    text="Window title will appear here",
    font=("Segoe UI", 10),
    bg="#263248",
    fg=TEXT
)
current_title_label.pack(
    anchor="w",
    pady=3
)
current_timer_label = tk.Label(
    current_frame,
    text="00:00:00",
    font=("Segoe UI", 22, "bold"),
    bg="#263248",
    fg=BLUE
)
current_timer_label.pack(
    anchor="w",
    pady=5
)
# DASHBOARD CARDS
cards = tk.Frame(
    root,
    bg=BG
)
cards.pack(
    fill="x",
    padx=20,
    pady=10
)
def create_card(title, color):

    frame = tk.Frame(
        cards,
        bg=CARD,
        padx=15,
        pady=12
    )
    frame.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5
    )
    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 10),
        bg=CARD,
        fg="#9CA3AF"
    ).pack(anchor="w")
    value = tk.Label(
        frame,
        text="00:00:00",
        font=("Segoe UI", 17, "bold"),
        bg=CARD,
        fg=color
    )
    value.pack(
        anchor="w",
        pady=5
    )
    return value
total_label = create_card(
    "TOTAL USAGE",
    BLUE
)
study_label = create_card(
    "STUDY TIME",
    GREEN
)
social_label = create_card(
    "SOCIAL MEDIA",
    PURPLE
)
entertainment_label = create_card(
    "ENTERTAINMENT",
    ORANGE
)
# MAIN SECTION
main = tk.Frame(
    root,
    bg=BG
)
main.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=15
)
# APPLICATION TABLE
left = tk.Frame(
    main,
    bg=CARD,
    padx=15,
    pady=15
)
left.pack(
    side="left",
    fill="both",
    expand=True
)
tk.Label(
    left,
    text="APPLICATION USAGE DETAILS",
    font=("Segoe UI", 12, "bold"),
    bg=CARD,
    fg=TEXT
).pack(anchor="w", pady=10)
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background=CARD,
    foreground=TEXT,
    fieldbackground=CARD,
    rowheight=30
)
style.configure(
    "Treeview.Heading",
    background="#374151",
    foreground="white"
)
columns = (
    "Application",
    "Category",
    "Time"
)
tree = ttk.Treeview(
    left,
    columns=columns,
    show="headings",
    height=14
)
tree.heading(
    "Application",
    text="Application"
)
tree.heading(
    "Category",
    text="Category"
)
tree.heading(
    "Time",
    text="Total Usage"
)
tree.column(
    "Application",
    width=170
)
tree.column(
    "Category",
    width=120
)
tree.column(
    "Time",
    width=100
)
tree.pack(
    fill="both",
    expand=True
)
# GRAPH SECTION
right = tk.Frame(
    main,
    bg=CARD,
    padx=10,
    pady=15
)
right.pack(
    side="right",
    fill="both",
    padx=(15, 0)
)
tk.Label(
    right,
    text="USAGE ANALYTICS",
    font=("Segoe UI", 12, "bold"),
    bg=CARD,
    fg=TEXT
).pack(anchor="w")
fig, ax = plt.subplots(
    figsize=(4.5, 4.2)
)
fig.patch.set_facecolor(CARD)
ax.set_facecolor(CARD)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(
    fig,
    master=right
)
canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    pady=10
)
# UPDATE DASHBOARD
def update_dashboard():
    df = wellbeing.get_dataframe()
    total_label.config(
        text=wellbeing.format_time(
            wellbeing.total_usage()
        )
    )
    study_label.config(
        text=wellbeing.format_time(
            wellbeing.category_usage("Study")
        )
    )
    social_label.config(
        text=wellbeing.format_time(
            wellbeing.category_usage("Social Media")
        )
    )

    entertainment_label.config(
        text=wellbeing.format_time(
            wellbeing.category_usage("Entertainment")
        )
    )
    # Update application table
    for item in tree.get_children():

        tree.delete(item)
    if not df.empty:

        df = df.sort_values(
            "Minutes",
            ascending=False
        )
        for _, row in df.iterrows():

            seconds = row["Minutes"] * 60
            tree.insert(
                "",
                "end",
                values=(

                    row["Application"],

                    row["Category"],

                    wellbeing.format_time(
                        seconds
                    )

                )
            )
    # Update graph
    ax.clear()
    ax.set_facecolor(CARD)
    fig.patch.set_facecolor(CARD)
    categories = [
        "Study",
        "Social Media",
        "Entertainment",
        "Browser",
        "Other"

    ]
    values = [

        wellbeing.category_usage(category) / 60

        for category in categories

    ]
    if np.sum(values) > 0:
        ax.bar(
            categories,
            values
        )
        ax.set_title(
            "Daily App Usage",
            color="white"
        )
        ax.set_ylabel(
            "Minutes",
            color="white"
        )
        ax.tick_params(
            axis="x",
            rotation=35,
            colors="white"
        )
        ax.tick_params(
            axis="y",
            colors="white"
        )
    else:

        ax.text(
            0.5,
            0.5,
            "Waiting for usage...",
            ha="center",
            color="white"
        )

        ax.set_axis_off()
    fig.tight_layout()

    canvas.draw_idle()
# EXPORT CSV
def export_data():

    df = wellbeing.get_dataframe()
    if df.empty:

        messagebox.showinfo(
            "Information",
            "No usage data available"
        )

        return
    filename = "wellbeing_report.csv"
    df.to_csv(
        filename,
        index=False
    )
    messagebox.showinfo(
        "Success",
        "Report saved successfully:\n"
        + os.path.abspath(filename)
    )
# BUTTONS
button_frame = tk.Frame(
    root,
    bg=BG
)
button_frame.pack(
    fill="x",
    padx=25,
    pady=10
)
tk.Button(
    button_frame,
    text="Refresh Dashboard",
    command=update_dashboard,
    bg=BLUE,
    fg="white",
    padx=15
).pack(
    side="left",
    padx=5
)
tk.Button(
    button_frame,
    text="Export CSV",
    command=export_data,
    bg=PURPLE,
    fg="white",
    padx=15
).pack(
    side="left",
    padx=5
)
# AUTOMATIC TRACKING
def automatic_tracking():
    wellbeing.track()
    # Current application name
    current_app_label.config(
        text=wellbeing.current_app
    )
    # Current window title
    current_title_label.config(
        text=wellbeing.current_title
    )
    # Current application total usage
    current_timer_label.config(
        text=wellbeing.format_time(
            wellbeing.current_app_usage()
        )
    )
    # Update dashboard
    update_dashboard()
    # Run every second
    root.after(
        1000,
        automatic_tracking
    )
# START APPLICATION
automatic_tracking()
root.mainloop()
