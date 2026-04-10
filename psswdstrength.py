import customtkinter as ctk
from tkinter import messagebox
import pyperclip  
import re
import string
import secrets
import hashlib  
import requests 

# Set app-wide theme
ctk.set_appearance_mode("Dark")  # Forcing dark mode for a sleek cybersecurity feel
ctk.set_default_color_theme("blue")  

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vault - Secure Password Tool")
        self.root.geometry("520x720")
        self.root.resizable(False, False)

        # --- Professional Font System ---
        # Falls back to standard sans-serif if Segoe/Helvetica aren't available
        self.font_title = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font_heading = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.font_body = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_small = ctk.CTkFont(family="Segoe UI", size=12)

        # --- Brand Color Palette ---
        self.colors = {
            "bg_card": "#1E293B",       # Slate 800
            "border": "#334155",        # Slate 700
            "primary": "#4F46E5",       # Indigo 600
            "primary_hover": "#4338CA", # Indigo 700
            "secondary": "#475569",     # Slate 600
            "secondary_hover": "#334155",
            "success": "#10B981",       # Emerald 500
            "danger": "#EF4444",        # Red 500
            "danger_hover": "#DC2626"
        }

        self.word_list = [
            "apple", "river", "cloud", "stone", "train", "light", "mouse", "chair",
            "brain", "glass", "water", "plant", "music", "table", "paper", "heart",
            "ocean", "bread", "watch", "house", "night", "smile", "dream", "space"
        ]

        self.create_widgets()

    def create_widgets(self):
        self.master_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.master_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # ==========================================
        # CARD 1: THE CHECKER
        # ==========================================
        self.checker_card = ctk.CTkFrame(
            self.master_frame, 
            corner_radius=10, 
            fg_color=self.colors["bg_card"],
            border_width=1,
            border_color=self.colors["border"]
        )
        self.checker_card.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(self.checker_card, text="Security Analyzer", font=self.font_title).pack(pady=(20, 5))
        ctk.CTkLabel(self.checker_card, text="Evaluate your password strength and breach history.", 
                     text_color="gray", font=self.font_small).pack(pady=(0, 20))

        entry_frame = ctk.CTkFrame(self.checker_card, fg_color="transparent")
        entry_frame.pack(pady=5)

        self.password_entry = ctk.CTkEntry(
            entry_frame, show="*", width=280, height=40,
            font=self.font_body, placeholder_text="Enter password...",
            border_color=self.colors["border"]
        )
        self.password_entry.grid(row=0, column=0, padx=(0, 10))
        self.password_entry.bind("<KeyRelease>", self.update_strength_indicator)

        self.show_cb = ctk.CTkCheckBox(entry_frame, text="Show", width=60, font=self.font_small,
                                       command=self.toggle_password_visibility)
        self.show_cb.grid(row=0, column=1)

        self.strength_label = ctk.CTkLabel(self.checker_card, text="Strength: Pending", font=self.font_heading)
        self.strength_label.pack(pady=(20, 5))

        self.strength_bar = ctk.CTkProgressBar(self.checker_card, width=340, height=8, corner_radius=4)
        self.strength_bar.set(0) 
        self.strength_bar.pack(pady=5)

        self.pwned_btn = ctk.CTkButton(
            self.checker_card, text="Check Data Breaches", font=self.font_body,
            command=self.check_pwned_api, fg_color=self.colors["danger"], 
            hover_color=self.colors["danger_hover"], height=35
        )
        self.pwned_btn.pack(pady=15)

        self.pwned_label = ctk.CTkLabel(self.checker_card, text="", font=self.font_small)
        self.pwned_label.pack(pady=(0, 15))

        # ==========================================
        # CARD 2: THE GENERATOR
        # ==========================================
        self.gen_card = ctk.CTkFrame(
            self.master_frame, 
            corner_radius=10, 
            fg_color=self.colors["bg_card"],
            border_width=1,
            border_color=self.colors["border"]
        )
        self.gen_card.pack(fill="x")

        ctk.CTkLabel(self.gen_card, text="Secure Generator", font=self.font_title).pack(pady=(20, 5))

        self.generated_display = ctk.CTkEntry(
            self.gen_card, width=340, height=45, justify="center",
            font=ctk.CTkFont(family="Courier New", size=18, weight="bold"), # Monospace looks better for passwords
            state="readonly", border_color=self.colors["border"]
        )
        self.generated_display.pack(pady=15)

        self.copy_btn = ctk.CTkButton(
            self.gen_card, text="Copy to Clipboard", font=self.font_body,
            command=self.copy_to_clipboard, fg_color=self.colors["secondary"], 
            hover_color=self.colors["secondary_hover"], height=35
        )
        self.copy_btn.pack(pady=(0, 20))

        btn_grid = ctk.CTkFrame(self.gen_card, fg_color="transparent")
        btn_grid.pack(pady=5)

        random_btn = ctk.CTkButton(
            btn_grid, text="Random String", width=160, height=40, font=self.font_body,
            command=self.generate_random_password, fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"]
        )
        random_btn.grid(row=0, column=0, padx=5)

        passphrase_btn = ctk.CTkButton(
            btn_grid, text="Passphrase", width=160, height=40, font=self.font_body,
            command=self.generate_passphrase, fg_color=self.colors["success"], 
            hover_color="#047857"
        ) 
        passphrase_btn.grid(row=0, column=1, padx=5)

        # Custom Generator UI
        ctk.CTkLabel(self.gen_card, text="Custom Memorable Password", font=self.font_small, text_color="gray").pack(pady=(20, 5))

        input_frame = ctk.CTkFrame(self.gen_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=40, pady=5)

        self.base_word_entry = ctk.CTkEntry(input_frame, placeholder_text="Word", width=140, font=self.font_body)
        self.base_word_entry.pack(side="left", padx=5)

        self.number_entry = ctk.CTkEntry(input_frame, placeholder_text="Number", width=90, font=self.font_body)
        self.number_entry.pack(side="left", padx=5)

        custom_btn = ctk.CTkButton(
            input_frame, text="Generate", width=80, font=self.font_body,
            command=self.generate_custom_password, fg_color=self.colors["secondary"],
            hover_color=self.colors["secondary_hover"]
        )
        custom_btn.pack(side="left", padx=5)
        
        ctk.CTkLabel(self.gen_card, text="", font=ctk.CTkFont(size=10)).pack()

    # --- LOGIC METHODS ---
    # (The logic methods remain exactly the same as your previous build)

    def check_pwned_api(self):
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Empty", "Please enter a password to check.")
            return

        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        self.pwned_btn.configure(text="Checking...", state="disabled")
        self.root.update()

        try:
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                hashes = (line.split(':') for line in response.text.splitlines())
                found_count = 0
                for h, count in hashes:
                    if h == suffix:
                        found_count = int(count)
                        break
                
                if found_count > 0:
                    self.pwned_label.configure(text=f"WARNING: Found in {found_count:,} breaches!", text_color=self.colors["danger"])
                else:
                    self.pwned_label.configure(text="Safe: Not found in known breaches.", text_color=self.colors["success"])
            else:
                self.pwned_label.configure(text="Error connecting to the API.", text_color="gray")

        except requests.exceptions.RequestException:
            self.pwned_label.configure(text="No internet connection.", text_color="gray")
        finally:
            self.pwned_btn.configure(text="Check Data Breaches", state="normal")

    def copy_to_clipboard(self):
        password = self.generated_display.get()
        if password:
            pyperclip.copy(password)
            self.copy_btn.configure(text="Copied to Clipboard!", fg_color=self.colors["success"])
            self.root.after(2000, lambda: self.copy_btn.configure(text="Copy to Clipboard", fg_color=self.colors["secondary"]))
        else:
            messagebox.showwarning("Empty", "Generate a password first!")

    def toggle_password_visibility(self):
        if self.show_cb.get() == 1:
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def display_generated_password(self, new_password):
        self.generated_display.configure(state="normal")
        self.generated_display.delete(0, ctk.END)
        self.generated_display.insert(0, new_password)
        self.generated_display.configure(state="readonly")
        
        self.password_entry.delete(0, ctk.END)
        self.password_entry.insert(0, new_password)
        self.show_cb.select() 
        self.toggle_password_visibility()
        self.update_strength_indicator()
        self.pwned_label.configure(text="") 

    def generate_random_password(self, length=14):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+"
        required_chars = [
            secrets.choice(string.ascii_lowercase), secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits), secrets.choice("!@#$%^&*()_+")
        ]
        rest_of_password = [secrets.choice(alphabet) for _ in range(length - 4)]
        password_list = required_chars + rest_of_password
        secrets.SystemRandom().shuffle(password_list) 
        self.display_generated_password("".join(password_list))

    def generate_passphrase(self):
        words = [secrets.choice(self.word_list) for _ in range(4)]
        passphrase = "-".join(words)
        passphrase += str(secrets.randbelow(100))
        self.display_generated_password(passphrase)

    def generate_custom_password(self):
        base = self.base_word_entry.get().strip()
        num = self.number_entry.get().strip()
        
        if not base or not num:
            messagebox.showwarning("Missing Input", "Please enter a Word and a Number.")
            return 
            
        subs = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '!'}
        transformed_base = "".join([subs.get(char, char) for char in base.lower()])
            
        if transformed_base and transformed_base[0].isalpha():
            transformed_base = transformed_base[0].upper() + transformed_base[1:]
        elif transformed_base:
            transformed_base = "A" + transformed_base 
            
        special_char = secrets.choice("!@#$%^&*")
        password = f"{transformed_base}{num}{special_char}"
        
        while len(password) < 12:
            password += secrets.choice(string.ascii_letters)
            
        self.display_generated_password(password)

    def check_password_strength(self, password):
        if not password:
            return "Pending", 0, "gray"

        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1 
        if re.search(r"[a-z]", password): score += 1 
        if re.search(r"[A-Z]", password): score += 1 
        if re.search(r"\d", password): score += 1    
        if re.search(r"[!@#$%^&*(),.?\":{}|<>\-]", password): score += 1 

        if score <= 3: return "Weak", 0.25, self.colors["danger"]
        elif score <= 5: return "Fair", 0.50, "#F59E0B" # Amber
        elif score == 6: return "Good", 0.75, "#3B82F6" # Blue
        else: return "Strong", 1.0, self.colors["success"]

    def update_strength_indicator(self, event=None):
        password = self.password_entry.get()
        strength, value, color = self.check_password_strength(password)
        
        if event:
            self.pwned_label.configure(text="")

        if strength == "Pending":
            self.strength_label.configure(text="Strength: Pending", text_color="gray")
            self.strength_bar.set(0)
            self.strength_bar.configure(progress_color="gray")
        else:
            self.strength_label.configure(text=f"Strength: {strength}", text_color=color)
            self.strength_bar.set(value)
            self.strength_bar.configure(progress_color=color)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PasswordStrengthApp(root)
    root.mainloop()