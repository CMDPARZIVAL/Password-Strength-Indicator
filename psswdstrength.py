<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # 1. Imported the messagebox module
import re
import string
import secrets

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Indicator & Generator")
        self.root.geometry("450x550")
        self.root.configure(bg="#f5f5f5")

        self.style = ttk.Style()
        self.style.theme_use('clam') 
        self.setup_styles()

        self.create_widgets()

    def setup_styles(self):
        self.style.configure("Weak.Horizontal.TProgressbar", background="#ff4d4d")
        self.style.configure("Fair.Horizontal.TProgressbar", background="#ffcc00")
        self.style.configure("Good.Horizontal.TProgressbar", background="#ffa500")
        self.style.configure("Strong.Horizontal.TProgressbar", background="#33cc33")

    def create_widgets(self):
        # --- CHECKER SECTION ---
        title_label = tk.Label(self.root, text="Password Strength Checker", 
                               font=("Arial", 14, "bold"), bg="#f5f5f5")
        title_label.pack(pady=(15, 5))

        self.password_entry = tk.Entry(self.root, show="*", width=30, font=("Arial", 12))
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<KeyRelease>", self.update_strength_indicator)

        self.show_password_var = tk.BooleanVar()
        show_cb = tk.Checkbutton(self.root, text="Show Password", 
                                 variable=self.show_password_var, 
                                 command=self.toggle_password_visibility, 
                                 bg="#f5f5f5", font=("Arial", 9))
        show_cb.pack()

        self.strength_label = tk.Label(self.root, text="Strength: None", 
                                       font=("Arial", 12, "bold"), bg="#f5f5f5")
        self.strength_label.pack(pady=5)

        self.strength_bar = ttk.Progressbar(self.root, length=300, mode='determinate')
        self.strength_bar.pack(pady=5)

        # --- GENERATOR SECTION ---
        gen_frame = tk.LabelFrame(self.root, text="Password Suggestions", bg="#f5f5f5", font=("Arial", 10, "bold"), padx=10, pady=10)
        gen_frame.pack(pady=20, fill="x", padx=20)

        # 1. Random Generator
        random_btn = tk.Button(gen_frame, text="🎲 Generate Random Strong Password", 
                               command=self.generate_random_password, bg="#e0e0e0")
        random_btn.pack(fill="x", pady=(0, 15))

        # 2. Custom Detail Generator
        tk.Label(gen_frame, text="Or create a memorable one based on:", bg="#f5f5f5").pack(anchor="w")
        
        input_frame = tk.Frame(gen_frame, bg="#f5f5f5")
        input_frame.pack(fill="x", pady=5)

        tk.Label(input_frame, text="Memorable Word:", bg="#f5f5f5").grid(row=0, column=0, sticky="w", pady=2)
        self.base_word_entry = tk.Entry(input_frame, width=15)
        self.base_word_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Favorite Number:", bg="#f5f5f5").grid(row=1, column=0, sticky="w", pady=2)
        self.number_entry = tk.Entry(input_frame, width=15)
        self.number_entry.grid(row=1, column=1, padx=5, pady=2)

        custom_btn = tk.Button(gen_frame, text="✨ Generate Custom Strong Password", 
                               command=self.generate_custom_password, bg="#e0e0e0")
        custom_btn.pack(fill="x", pady=(5, 0))

    # --- LOGIC METHODS ---

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def apply_generated_password(self, new_password):
        """Helper to insert the new password and trigger the strength check."""
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)
        self.show_password_var.set(True)
        self.toggle_password_visibility()
        self.update_strength_indicator()

    def generate_random_password(self, length=14):
        """Generates a highly secure random string."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+"
        
        required_chars = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice("!@#$%^&*()_+")
        ]
        
        rest_of_password = [secrets.choice(alphabet) for _ in range(length - 4)]
        
        password_list = required_chars + rest_of_password
        secrets.SystemRandom().shuffle(password_list) 
        
        self.apply_generated_password("".join(password_list))

    def generate_custom_password(self):
        """Generates a secure password mangled from user inputs."""
        base = self.base_word_entry.get().strip()
        num = self.number_entry.get().strip()
        
        # 2. Check for empty fields and show a warning popup
        if not base or not num:
            messagebox.showwarning(
                title="Missing Input", 
                message="Please enter both a 'Memorable Word' and a 'Favorite Number' to generate a custom password."
            )
            return  # This stops the function here, preventing the password from generating
            
        # Common Leetspeak substitutions
        subs = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '!'}
        transformed_base = ""
        for char in base.lower():
            transformed_base += subs.get(char, char)
            
        # Ensure there is an uppercase letter
        if transformed_base and transformed_base[0].isalpha():
            transformed_base = transformed_base[0].upper() + transformed_base[1:]
        elif transformed_base:
            transformed_base = "A" + transformed_base 
            
        # Combine base, number, and guarantee a special character
        special_char = secrets.choice("!@#$%^&*")
        password = f"{transformed_base}{num}{special_char}"
        
        # Ensure length is at least 12 for max strength score
        while len(password) < 12:
            password += secrets.choice(string.ascii_letters)
            
        self.apply_generated_password(password)

    def check_password_strength(self, password):
        if not password:
            return "None", 0, "black"

        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if re.search(r"[a-z]", password): score += 1 
        if re.search(r"[A-Z]", password): score += 1 
        if re.search(r"\d", password): score += 1    
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1 

        if score <= 2: return "Weak", 25, "#ff4d4d"
        elif score <= 4: return "Fair", 50, "#ffcc00"
        elif score == 5: return "Good", 75, "#ffa500"
        else: return "Strong", 100, "#33cc33"

    def update_strength_indicator(self, event=None):
        password = self.password_entry.get()
        strength, value, color = self.check_password_strength(password)
        
        if strength == "None":
            self.strength_label.config(text="Strength: None", foreground="black")
            self.strength_bar['value'] = 0
        else:
            self.strength_label.config(text=f"Strength: {strength}", foreground=color)
            self.strength_bar['value'] = value
            self.strength_bar['style'] = f"{strength}.Horizontal.TProgressbar"


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthApp(root)
    root.mainloop()
