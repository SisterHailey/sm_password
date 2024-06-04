import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

class SMPWDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrap Mechanic Password Tool")

        # Set window size and center contents
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        # Main frame for centering the elements
        main_frame = tk.Frame(root)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(main_frame, text="Server Password:").grid(row=0, column=0, pady=10)
        self.password_entry = tk.Entry(main_frame, width=30)
        self.password_entry.grid(row=0, column=1, pady=10)

        self.cheats_var = tk.IntVar()
        tk.Checkbutton(main_frame, text="Server has cheats", variable=self.cheats_var).grid(row=1, columnspan=2, pady=10)

        set_button = tk.Button(main_frame, text="Set", command=self.set_password, width=20)
        set_button.grid(row=2, columnspan=2, pady=10)

        restore_button = tk.Button(main_frame, text="Restore", command=self.restore_defaults, width=20)
        restore_button.grid(row=3, columnspan=2, pady=10)

        self.scrap_mechanic_path = self.find_scrap_mechanic_directory()
        if not self.scrap_mechanic_path or not self.check_integrity(self.scrap_mechanic_path):
            self.scrap_mechanic_path = filedialog.askdirectory(title="Select Scrap Mechanic Directory")
            if not self.check_integrity(self.scrap_mechanic_path):
                messagebox.showerror("Error", "Invalid Scrap Mechanic directory.")
                self.root.quit()
                return

    def find_scrap_mechanic_directory(self):
        possible_paths = []
        for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f"{drive}:\\"
            if os.path.exists(drive_path):
                possible_paths.extend([
                    os.path.join(drive_path, r"SteamLibrary\steamapps\common\Scrap Mechanic"),
                    os.path.join(drive_path, r"Program Files (x86)\Steam\steamapps\common\Scrap Mechanic"),
                ])

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def check_integrity(self, path):
        return os.path.exists(os.path.join(path, "Survival", "Scripts", "game", "SurvivalGame.lua"))

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self):
        survival_game_path = os.path.join(self.scrap_mechanic_path, "Survival", "Scripts", "game", "SurvivalGame.lua")
        password = self.password_entry.get()

        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        hashed_password = self.hash_password(password)

        with open(survival_game_path, 'r') as file:
            lines = file.readlines()

        # Update password
        if lines[0].startswith('--smpwd: '):
            lines[0] = f'--smpwd: {hashed_password}\n'
        else:
            lines.insert(0, f'--smpwd: {hashed_password}\n')

        # Update cheats setting
        for i in range(len(lines)):
            if lines[i].strip().startswith("local addCheats"):
                if self.cheats_var.get():
                    lines[i] = "	local addCheats = true\n"
                else:
                    lines[i] = "	local addCheats = g_survivalDev\n"
                break

        with open(survival_game_path, 'w') as file:
            file.writelines(lines)

        messagebox.showinfo("Success", "Settings updated successfully.")

    def restore_defaults(self):
        survival_game_path = os.path.join(self.scrap_mechanic_path, "Survival", "Scripts", "game", "SurvivalGame.lua")

        with open(survival_game_path, 'r') as file:
            lines = file.readlines()

        # Remove password line if it exists
        if lines[0].startswith('--smpwd: '):
            lines.pop(0)

        # Reset cheats setting to default
        for i in range(len(lines)):
            if lines[i].strip().startswith("local addCheats"):
                lines[i] = "	local addCheats = g_survivalDev\n"
                break

        with open(survival_game_path, 'w') as file:
            file.writelines(lines)

        messagebox.showinfo("Success", "Defaults restored successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SMPWDApp(root)
    root.mainloop()