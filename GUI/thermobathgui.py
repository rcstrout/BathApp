import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
import serial

class BathController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Water Bath Controller")

        self.root.configure(bg="#333333")  # Dark background color

        self.status_label = tk.Label(self.root, text="Not connected", font=("Helvetica", 14), fg="red", bg="#333333")
        self.status_label.pack(pady=(10, 0))

        self.connect_button = tk.Button(self.root, text="Connect", font=("Helvetica", 12), command=self.connect_to_bath)
        self.connect_button.pack(pady=(10, 0))

        self.bath_connected = False
        self.bath = None

        self.terminal_frame = tk.Frame(self.root, bg="#111111")  # Dark terminal frame
        self.terminal_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.terminal_scroll = tk.Scrollbar(self.terminal_frame)
        self.terminal_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.terminal = tk.Text(self.terminal_frame, wrap=tk.WORD, width=60, height=15, bg="#111111", fg="#FFFFFF", yscrollcommand=self.terminal_scroll.set)  # Dark terminal
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.terminal_scroll.config(command=self.terminal.yview)
        
        self.stop_button = tk.Button(self.root, text="Stop", font=("Helvetica", 12), command=self.stop_program, state=tk.DISABLED)
        self.stop_button.pack(pady=(10, 0))

    def print_to_terminal(self, message):
        self.terminal.insert(tk.END, message + "\n")
        self.terminal.see(tk.END)

    def connect_to_bath(self):
        if not self.bath_connected:
            try:
                self.bath = serial.Serial('COM3', baudrate=19200, bytesize=8, stopbits=1, timeout=1)
                self.bath.write(b"SE1\r")  # turn on command echo
                response = self.bath.readline()  # always read the response to clear the buffer
                self.bath_connected = True
                self.status_label.config(text="Connected", fg="green")
                self.connect_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)  # Enable the Stop button
                self.run_program()
                self.print_to_terminal("Connected to bath.")
            except Exception as e:
                self.print_to_terminal(f"Failed to connect to the bath: {e}")
                messagebox.showerror("Error", f"Failed to connect to the bath: {e}")

    def stop_program(self):
        if hasattr(self, 'ramp_thread') and self.ramp_thread.is_alive():
            self.ramp_thread.join()  # Wait for the thread to finish
            self.print_to_terminal("Program stopped.")
        else:
            self.print_to_terminal("No program running to stop.")

    def ramp(self, program):
        if program == 0:
            set_temp = simpledialog.askfloat("Constant Temperature", "Enter the constant setpoint temperature (C):")
            if set_temp is not None:
                self.print_to_terminal(f"Setting constant temperature: {set_temp} C")
                # Add your logic here to set the constant temperature
        # ... (rest of the ramp method remains the same)

    # ... (rest of the methods remain the same)

if __name__ == "__main__":
    controller = BathController()
    controller.run()

