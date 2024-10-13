import os
import tkinter as tk
from tkinter import filedialog, messagebox

def get_documents_folder():
    # Windows
    if os.name == 'nt':
        return os.path.join(os.environ['USERPROFILE'], 'Documents')
    # macOS
    elif os.uname().sysname == 'Darwin':
        return os.path.join(os.path.expanduser('~'), 'Documents')
    else:
        messagebox.showerror("Error", "This script only supports Windows and macOS!")
        return None

def get_profile_path():
    documents_path = get_documents_folder()
    if not documents_path:
        return None
    
    profile_path = os.path.join(documents_path, "Plants vs Zombies GW2", "settings", "PROF_SAVE_profile")
    
    if os.path.exists(profile_path):
        return profile_path
    else:
        user_documents = filedialog.askdirectory(title="Plants vs Zombies GW2 folder not found! Please select the folder manually:")
        if user_documents:
            profile_path = os.path.join(user_documents, "settings", "PROF_SAVE_profile")
            if os.path.exists(profile_path):
                return profile_path
            else:
                messagebox.showerror("Error", "PROF_SAVE_profile not found in the selected folder!")
                return None
        else:
            return None

def load_values():
    profile_path = get_profile_path()
    if not profile_path:
        return None
    
    values = {"FieldOfView": None, "FullscreenRefreshRate": None, "WindowedRefreshRate": None}
    
    with open(profile_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("GstRender.FieldOfView"):
                values["FieldOfView"] = float(line.split()[1])
            elif line.startswith("GstRender.FullscreenRefreshRate"):
                values["FullscreenRefreshRate"] = float(line.split()[1])
            elif line.startswith("GstRender.WindowedRefreshRate"):
                values["WindowedRefreshRate"] = float(line.split()[1])
    
    return profile_path, values

def save_values(profile_path, new_values):
    with open(profile_path, "r") as file:
        lines = file.readlines()
    
    with open(profile_path, "w") as file:
        for line in lines:
            if line.startswith("GstRender.FieldOfView"):
                file.write(f"GstRender.FieldOfView {new_values['FieldOfView']}\n")
            elif line.startswith("GstRender.FullscreenRefreshRate"):
                file.write(f"GstRender.FullscreenRefreshRate {new_values['FullscreenRefreshRate']}\n")
            elif line.startswith("GstRender.WindowedRefreshRate"):
                file.write(f"GstRender.WindowedRefreshRate {new_values['WindowedRefreshRate']}\n")
            else:
                file.write(line)

def adjust_values(profile_path, fov_var, fullscreen_var, windowed_var):
    new_values = {
        "FieldOfView": fov_var.get(),
        "FullscreenRefreshRate": fullscreen_var.get(),
        "WindowedRefreshRate": windowed_var.get()
    }
    save_values(profile_path, new_values)

def create_ui():
    root = tk.Tk()
    root.title("BetterGW2")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    small_font = ('Arial', 12)

    profile_path, values = load_values()
    if not values:
        return
    
    fov_var = tk.DoubleVar(value=values["FieldOfView"])
    fullscreen_var = tk.DoubleVar(value=values["FullscreenRefreshRate"])
    windowed_var = tk.DoubleVar(value=values["WindowedRefreshRate"])

    tk.Label(root, text="Field of View:", font=small_font).grid(row=0, column=0, padx=12, pady=6)
    fov_spinbox = tk.Spinbox(root, from_=5, to=180, increment=5, textvariable=fov_var, font=small_font, width=8)
    fov_spinbox.grid(row=0, column=1, padx=12, pady=6)
    
    tk.Label(root, text="Fullscreen Refresh Rate:", font=small_font).grid(row=1, column=0, padx=12, pady=6)
    fullscreen_spinbox = tk.Spinbox(root, from_=5, to=5000, increment=5, textvariable=fullscreen_var, font=small_font, width=8)
    fullscreen_spinbox.grid(row=1, column=1, padx=12, pady=6)
    
    tk.Label(root, text="Windowed Refresh Rate:", font=small_font).grid(row=2, column=0, padx=12, pady=6)
    windowed_spinbox = tk.Spinbox(root, from_=5, to=5000, increment=5, textvariable=windowed_var, font=small_font, width=8)
    windowed_spinbox.grid(row=2, column=1, padx=12, pady=6)

    save_button = tk.Button(root, text="Save", command=lambda: adjust_values(profile_path, fov_var, fullscreen_var, windowed_var), font=small_font)
    save_button.grid(row=3, column=0, columnspan=2, padx=12, pady=12)

    root.mainloop()

if __name__ == "__main__":
    create_ui()