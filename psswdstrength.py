import customtkinter as ctk
from tkinter import messagebox
import pyperclip  
import re
import string
import secrets
import hashlib  # Needed for encrypting the password
import requests # Needed for talking to the web API

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Password Tool")
        self.root.geometry("450x700") # Increased height slightly

        self.word_list = [
            "apple", "river", "cloud", "stone", "train", "light", "mouse", "chair",
            "brain", "glass", "water", "plant", "music", "table", "paper", "heart",
            "ocean", "bread", "watch", "house", "night", "smile", "dream", "space",
            "block", "flame", "grape", "honey", "juice", "lemon", "mango", "peach"
        ]

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- CHECKER SECTION ---
        title_label = ctk.CTkLabel(self.main_frame, text="Password Security Checker", 
                                   font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))

        entry_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        entry_frame.pack(pady=10)

        self.password_entry = ctk.CTkEntry(entry_frame, show="*", width=240, 
                                           font=ctk.CTkFont(size=14), placeholder_text="Type password here...")
        self.password_entry.grid(row=0, column=0, padx=(0, 5))
        self.password_entry.bind("<KeyRelease>", self.update_strength_indicator)

        self.copy_btn = ctk.CTkButton(entry_frame, text="📋 Copy", width=50, 
                                      command=self.copy_to_clipboard, fg_color="#4b5563", hover_color="#374151")
        self.copy_btn.grid(row=0, column=1)

        self.show_cb = ctk.CTkCheckBox(self.main_frame, text="Show Password", 
                                       command=self.toggle_password_visibility)
        self.show_cb.pack(pady=5)

        self.strength_label = ctk.CTkLabel(self.main_frame, text="Strength: None", 
                                           font=ctk.CTkFont(size=16, weight="bold"))
        self.strength_label.pack(pady=(10, 0))

        self.strength_bar = ctk.CTkProgressBar(self.main_frame, width=300, height=12)
        self.strength_bar.set(0) 
        self.strength_bar.pack(pady=5)

        # --- NEW: API BREACH CHECKER SECTION ---
        self.pwned_btn = ctk.CTkButton(self.main_frame, text="🔍 Check if Pwned (Data Breach)", 
                                       command=self.check_pwned_api, fg_color="#b91c1c", hover_color="#991b1b")
        self.pwned_btn.pack(pady=10)

        self.pwned_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=12))
        self.pwned_label.pack(pady=(0, 10))

        # --- GENERATOR SECTION ---
        gen_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        gen_frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(gen_frame, text="Need a secure password?", 
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))

        random_btn = ctk.CTkButton(gen_frame, text="🎲 Generate Random Password", 
                                   command=self.generate_random_password, 
                                   fg_color="#4b5563", hover_color="#374151")
        random_btn.pack(fill="x", padx=20, pady=5)

        passphrase_btn = ctk.CTkButton(gen_frame, text="📚 Generate Memorable Passphrase", 
                                   command=self.generate_passphrase, 
                                   fg_color="#059669", hover_color="#047857") 
        passphrase_btn.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(gen_frame, text="-- OR --", text_color="gray").pack()

        input_frame = ctk.CTkFrame(gen_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=5)

        self.base_word_entry = ctk.CTkEntry(input_frame, placeholder_text="Memorable Word", width=130)
        self.base_word_entry.grid(row=0, column=0, padx=5, pady=5)

        self.number_entry = ctk.CTkEntry(input_frame, placeholder_text="Fav Number", width=130)
        self.number_entry.grid(row=0, column=1, padx=5, pady=5)

        custom_btn = ctk.CTkButton(gen_frame, text="✨ Generate Custom Password", 
                                   command=self.generate_custom_password)
        custom_btn.pack(fill="x", padx=20, pady=(10, 20))

    # --- LOGIC METHODS ---

    def check_pwned_api(self):
        """Securely checks the password against the Have I Been Pwned API."""
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Empty", "Please enter a password to check.")
            return

        # 1. Hash the password using SHA-1
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        # 2. Split the hash for K-Anonymity security
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        # 3. Update UI to show loading state
        self.pwned_btn.configure(text="⏳ Checking...", state="disabled")
        self.root.update()

        try:
            # 4. Request data from the API
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                # API returns lines like "SUFFIX:COUNT". We split and check them.
                hashes = (line.split(':') for line in response.text.splitlines())
                found_count = 0
                for h, count in hashes:
                    if h == suffix:
                        found_count = int(count)
                        break
                
                # 5. Display the results
                if found_count > 0:
                    self.pwned_label.configure(text=f"⚠️ WARNING: Found in {found_count:,} data breaches!", text_color="#ef4444")
                else:
                    self.pwned_label.configure(text="✅ Safe: Not found in any known data breaches.", text_color="#22c55e")
            else:
                self.pwned_label.configure(text="❌ Error connecting to the API.", text_color="gray")

        except requests.exceptions.RequestException:
            self.pwned_label.configure(text="❌ No internet connection or API is down.", text_color="gray")
        
        finally:
            # Reset button state
            self.pwned_btn.configure(text="🔍 Check if Pwned (Data Breach)", state="normal")

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            self.copy_btn.configure(text="✅ Copied!")
            self.root.after(2000, lambda: self.copy_btn.configure(text="📋 Copy"))
        else:
            messagebox.showwarning("Empty", "There is no password to copy!")

    def toggle_password_visibility(self):
        if self.show_cb.get() == 1:
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def apply_generated_password(self, new_password):
        self.password_entry.delete(0, ctk.END)
        self.password_entry.insert(0, new_password)
        self.show_cb.select() 
        self.toggle_password_visibility()
        self.update_strength_indicator()
        # Reset the pwned label when a new password is generated
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
        self.apply_generated_password("".join(password_list))

    def generate_passphrase(self):
        words = [secrets.choice(self.word_list) for _ in range(4)]
        passphrase = "-".join(words)
        passphrase += str(secrets.randbelow(100))
        self.apply_generated_password(passphrase)

    def generate_custom_password(self):
        base = self.base_word_entry.get().strip()
        num = self.number_entry.get().strip()
        
        if not base or not num:
            messagebox.showwarning("Missing Input", "Please enter both a 'Memorable Word' and a 'Favorite Number'.")
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
            self.apply_generated_password(password)

    def check_password_strength(self, password):
        if not password:
            return "None", 0, "gray"

        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1 
        if re.search(r"[a-z]", password): score += 1 
        if re.search(r"[A-Z]", password): score += 1 
        if re.search(r"\d", password): score += 1    
        if re.search(r"[!@#$%^&*(),.?\":{}|<>\-]", password): score += 1 

        if score <= 3: return "Weak", 0.25, "#ff4d4d"
        elif score <= 5: return "Fair", 0.50, "#ffcc00"
        elif score == 6: return "Good", 0.75, "#ffa500"
        else: return "Strong", 1.0, "#33cc33"

    def update_strength_indicator(self, event=None):
        password = self.password_entry.get()
        strength, value, color = self.check_password_strength(password)
        
        # Reset the breach label if the user starts typing a new password
        if event:
            self.pwned_label.configure(text="")

        if strength == "None":
            self.strength_label.configure(text="Strength: None", text_color="gray")
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