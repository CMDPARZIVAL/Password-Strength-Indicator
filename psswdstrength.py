import tkinter as tk
from tkinter import ttk

def check_password_strength(password):
    length = len(password)
    if length < 6:
        return "Weak", 25, "#ff4d4d"  # Red
    elif 6 <= length < 8:
        return "Fair", 50, "#ffcc00"  # Yellow
    elif 8 <= length < 12:
        return "Good", 75, "#ffa500"  # Orange
    else:
        return "Strong", 100, "#33cc33"  # Green

def update_strength_indicator(event=None):
    password = password_entry.get()
    strength, value, color = check_password_strength(password)
    
    strength_label.config(text=f"Strength: {strength}", foreground=color)
    strength_bar['value'] = value
    strength_bar['style'] = f"{strength}.Horizontal.TProgressbar"
    
# Set up the main application window
app = tk.Tk()
app.title("Password Strength Indicator")
app.geometry("400x250")
app.configure(bg="#f5f5f5")

# Title Label
title_label = tk.Label(app, text="Password Strength Checker", font=("Arial", 14, "bold"), bg="#f5f5f5")
title_label.pack(pady=10)

# Create the password entry field
password_entry = tk.Entry(app, show="*", width=30, font=("Arial", 12, "bold"))
password_entry.pack(pady=10)
password_entry.bind("<KeyRelease>", update_strength_indicator)  # Real-time checking

# Strength Indicator Label
strength_label = tk.Label(app, text="Strength: ", font=("Arial", 12, "bold"), bg="#f5f5f5")
strength_label.pack(pady=5)

# Style for progress bar
style = ttk.Style()
style.configure("Weak.Horizontal.TProgressbar", foreground="#ff4d4d", background="#ff4d4d")
style.configure("Fair.Horizontal.TProgressbar", foreground="#ffcc00", background="#ffcc00")
style.configure("Good.Horizontal.TProgressbar", foreground="#ffa500", background="#ffa500")
style.configure("Strong.Horizontal.TProgressbar", foreground="#33cc33", background="#33cc33")

# Strength Bar
strength_bar = ttk.Progressbar(app, length=300, mode='determinate')
strength_bar.pack(pady=10)

# Run the GUI loop
app.mainloop()
