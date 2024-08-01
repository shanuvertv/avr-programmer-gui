import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import subprocess
import serial.tools.list_ports
import os
import sys

class AVRProgrammer(ThemedTk):
    def __init__(self):
        super().__init__(theme="plastik")
        self.title("AVR Programmer")
        self.geometry("450x300")
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # COM Port
        ttk.Label(frame, text="COM Port:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.com_var = tk.StringVar()
        self.com_combo = ttk.Combobox(frame, textvariable=self.com_var)
        self.com_combo['values'] = self.get_com_ports()
        self.com_combo.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))

        # Baud Rate
        ttk.Label(frame, text="Baud Rate:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.baud_var = tk.StringVar(value="115200")
        ttk.Entry(frame, textvariable=self.baud_var).grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))

        # Chip Type
        ttk.Label(frame, text="Chip Type:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.chip_var = tk.StringVar()
        self.chip_combo = ttk.Combobox(frame, textvariable=self.chip_var)
        self.chip_combo['values'] = self.get_supported_chips()
        self.chip_combo.grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))

        # File Selection
        ttk.Label(frame, text="File:").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.file_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.file_var).grid(row=3, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(frame, text="Browse", command=self.browse_file).grid(row=3, column=2, padx=10, pady=10)

        # Program Button
        ttk.Button(frame, text="Program", command=self.program_chip).grid(row=4, column=1, padx=10, pady=10)

        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def get_com_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def get_supported_chips(self):
        # List of supported AVR chips
        return [
            "m328p", "m328pb", "m32u4", "m2560", "m2561",
            "m1280", "m1281", "m64", "m64hvb", "m32",
            "m32hvb", "m16", "m16hva", "m8", "m8hva",
            "m88", "m168", "m169", "m8515", "m8535"
        ]

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("ELF files", "*.elf"), ("HEX files", "*.hex")])
        self.file_var.set(file_path)

    def program_chip(self):
        com_port = self.com_var.get()
        baud_rate = self.baud_var.get()
        chip_type = self.chip_var.get()
        file_path = self.file_var.get()

        if not (com_port and baud_rate and chip_type and file_path):
            messagebox.showerror("Error", "All fields must be filled!")
            return

        # Correctly format the file path for AVRDude and quote it
        file_path = os.path.normpath(file_path)
        print(f"File path: {file_path}")  # Debugging: Print the file path

        avrdude_path = os.path.join(sys._MEIPASS, 'resources', 'avrdude.exe') if getattr(sys, 'frozen', False) else 'avrdude'
        avrdude_conf_path = os.path.join(sys._MEIPASS, 'resources', 'avrdude.conf') if getattr(sys, 'frozen', False) else 'avrdude.conf'

        avrdude_command = [
            avrdude_path,
            "-C", avrdude_conf_path,
            "-c", "arduino",
            "-p", chip_type,
            "-P", com_port,
            "-b", baud_rate,
            "-U", f"flash:w:{file_path}:i"
        ]

        print(f"AVRDude command: {' '.join(avrdude_command)}")  # Debugging: Print the AVRDude command

        try:
            result = subprocess.run(avrdude_command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", "Programming completed successfully!")
            else:
                messagebox.showerror("Error", f"Programming failed:\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    app = AVRProgrammer()
    app.mainloop()
