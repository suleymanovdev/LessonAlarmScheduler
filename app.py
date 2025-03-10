import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import threading
import time
import pygame

JSON_FILE = "schedule.json"

if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def load_schedule():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_schedule(schedule):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=4, ensure_ascii=False)

def update_table():
    for row in table.get_children():
        table.delete(row)
    schedule = load_schedule()
    for entry in schedule:
        table.insert("", "end", values=(entry["name"], entry["time"], entry["duration"], entry["path"]))

def add_entry():
    name = name_entry.get()
    time_value = time_entry.get()
    duration = duration_entry.get()
    music_path = file_path.get()

    if not (name and time_value and duration and music_path):
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    try:
        datetime.strptime(time_value, "%H:%M")
        duration = int(duration)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите время в формате ЧЧ:ММ и длительность в секундах!")
        return

    schedule = load_schedule()
    schedule.append({"name": name, "time": time_value, "duration": duration, "path": music_path})
    save_schedule(schedule)
    update_table()

def select_file():
    path = filedialog.askopenfilename(filetypes=[("Аудиофайлы", "*.mp3;*.wav")])
    if path:
        file_path.set(path)

def delete_selected():
    selected_items = table.selection()
    if not selected_items:
        return
    schedule = load_schedule()
    selected_values = [table.item(item, "values") for item in selected_items]
    schedule = [entry for entry in schedule if (entry["name"], entry["time"], str(entry["duration"]), entry["path"]) not in selected_values]
    save_schedule(schedule)
    update_table()

def play_music():
    pygame.mixer.init()
    while True:
        now = datetime.now().strftime("%H:%M")
        schedule = load_schedule()
        for entry in schedule:
            if entry["time"] == now:
                pygame.mixer.music.load(entry["path"])
                pygame.mixer.music.play()
                time.sleep(entry["duration"])
                pygame.mixer.music.stop()
        time.sleep(10)

threading.Thread(target=play_music, daemon=True).start()

root = tk.Tk()
root.title("Расписание звонков")
root.geometry("700x400")

columns = ("Название", "Время", "Длительность", "Путь")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
table.pack(fill=tk.BOTH, expand=True)

frame = tk.Frame(root)
frame.pack(fill=tk.X)

tk.Button(frame, text="Удалить", command=delete_selected).pack(side=tk.LEFT, padx=5, pady=5)

tk.Label(frame, text="Название:").pack(side=tk.LEFT, padx=5)
name_entry = tk.Entry(frame)
name_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame, text="Время (ЧЧ:ММ):").pack(side=tk.LEFT, padx=5)
time_entry = tk.Entry(frame)
time_entry.pack(side=tk.LEFT, padx=5)

tk.Label(frame, text="Длительность (сек):").pack(side=tk.LEFT, padx=5)
duration_entry = tk.Entry(frame)
duration_entry.pack(side=tk.LEFT, padx=5)

file_path = tk.StringVar()
tk.Button(frame, text="Выбрать файл", command=select_file).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Добавить", command=add_entry).pack(side=tk.LEFT, padx=5)

update_table()

root.mainloop()