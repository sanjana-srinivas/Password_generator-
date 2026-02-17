import string
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import random



class password_generator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("600x720+370+50")

        # main container
        self.main_frame = Frame(self.root, bd=5, relief=RIDGE, bg="white")
        self.main_frame.place(x=0, y=0, width=600, height=720)

        self.title_lbl = Label(self.main_frame, text="PASSWORD GENERATOR", font=("times new roman", 20, "bold"), bg="white", fg="black")
        self.title_lbl.place(x=0, y=0, width=600)

        # header image (optional)
        try:
            img1 = Image.open("pass_gen.png")
            img1 = img1.resize((596, 280), Image.Resampling.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
            lblimg1 = Label(self.main_frame, image=self.photoimg1)
            lblimg1.place(x=0, y=50, width=600, height=190)
        except Exception:
            pass

        # length input
        self.length_label = Label(self.main_frame, text="Enter Password Length", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.length_label.place(x=40, y=250)

        self.var_entry = StringVar()
        self.entry_fill = ttk.Entry(self.main_frame, textvariable=self.var_entry, width=51, font=("times new roman", 15, "bold"))
        self.entry_fill.place(x=42, y=290)
        # bind Enter key to generate (on entry)
        self.entry_fill.bind("<Return>", lambda e: self.generate_password())

        # (single password generation — removed Count spinbox)

        # global keyboard shortcuts
        self.root.bind('<Control-c>', lambda e: self.copy_to_clipboard())
        self.root.bind('<Control-C>', lambda e: self.copy_to_clipboard())
        self.root.bind('<Control-l>', lambda e: self.clear_fields())
        self.root.bind('<Control-L>', lambda e: self.clear_fields())
        self.root.bind('<Control-h>', lambda e: self.clear_history())
        self.root.bind('<Control-H>', lambda e: self.clear_history())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())
        self.root.bind('<Control-T>', lambda e: self.toggle_theme())

 
        # suggested length
        self.suggest_label = Label(self.main_frame, text="Recommended length: 12-16", font=("times new roman", 10), bg="white", fg="gray")
        self.suggest_label.place(x=42, y=325)

        # custom character sets (checkboxes)
        self.use_lower = IntVar(value=1)
        self.use_upper = IntVar(value=1)
        self.use_digits = IntVar(value=1)
        self.use_special = IntVar(value=1)
        
        chk_frame = Frame(self.main_frame, bg="white")
        chk_frame.place(x=42, y=343, width=500, height=20)
        
        Checkbutton(chk_frame, text="Lower", variable=self.use_lower, bg="white", font=("times new roman", 9)).pack(side=LEFT, padx=8)
        Checkbutton(chk_frame, text="Upper", variable=self.use_upper, bg="white", font=("times new roman", 9)).pack(side=LEFT, padx=8)
        Checkbutton(chk_frame, text="Digits", variable=self.use_digits, bg="white", font=("times new roman", 9)).pack(side=LEFT, padx=8)
        Checkbutton(chk_frame, text="Special", variable=self.use_special, bg="white", font=("times new roman", 9)).pack(side=LEFT, padx=8)
        

        # generate button
        btn = Button(self.main_frame, text="GENERATE PASSWORD", font=("times new roman", 15, "bold"), bg="blue", fg="white", bd=4, relief=GROOVE, cursor="hand2", command=self.generate_password)
        btn.place(x=40, y=373, width=520, height=40)

        # output label
        self.pass_label = Label(self.main_frame, text="Generated Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.pass_label.place(x=40, y=428)

        # displayed password (readonly Entry) with visibility toggle
        self.display_var = StringVar()
        self.show_pass_entry = Entry(self.main_frame, textvariable=self.display_var, font=("times new roman", 15, "bold"), bg="white", fg="green", bd=2, relief=GROOVE, state='readonly')
        self.show_pass_entry.place(x=40, y=458, width=520, height=40)
        # visibility icon inside entry (Canvas to lock position)
        self.is_hidden = False
        self.visibility_canvas = Canvas(self.main_frame, bg="white", highlightthickness=0, cursor="hand2")
        self.visibility_canvas.place(x=523, y=458, width=37, height=40)
        self.visibility_canvas.create_text(2, 20, text="⊘", font=("Courier New", 16, "bold"), fill="black", anchor="w")
        self.visibility_canvas.bind('<Button-1>', lambda e: self.toggle_visibility())

        # Strength label
        self.strength_var = StringVar(value="Strength: ")
        self.strength_label = Label(self.main_frame, textvariable=self.strength_var, font=("times new roman", 15, "bold"), bg="white", fg="black")
        self.strength_label.place(x=40, y=505)

        # history listbox (shows generated passwords)
        self.history_listbox = Listbox(self.main_frame, bd=2, relief=GROOVE, font=("times new roman", 11))
        # make history taller so buttons don't overlap
        self.history_listbox.place(x=40, y=535, width=520, height=70)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)

        # Clear History button (small) - placed under history list
        clear_hist_btn = Button(self.main_frame, text="Clear History", font=("times new roman", 9), bg="#666666", fg="white", bd=2, relief=GROOVE, cursor="hand2", command=self.clear_history)
        clear_hist_btn.place(x=40, y=612, width=120, height=28)

        # buttons
        copy_btn = Button(self.main_frame, text="COPY", font=("times new roman", 12, "bold"), bg="green", fg="white", bd=4, relief=GROOVE, cursor="hand2", command=self.copy_to_clipboard)
        copy_btn.place(x=40, y=650, width=250, height=36)

        clear_btn = Button(self.main_frame, text="CLEAR", font=("times new roman", 12, "bold"), bg="red", fg="white", bd=4, relief=GROOVE, cursor="hand2", command=self.clear_fields)
        clear_btn.place(x=310, y=650, width=250, height=36)

        # Theme toggle (small square at bottom-right)
        self.is_dark = False
        theme_btn = Button(self.main_frame, text="🌓", font=("times new roman", 10), bg="lightgray", fg="black", command=self.toggle_theme)
        # place at bottom-right corner with a small margin
        theme_btn.place(x=572, y=650, width=28, height=36)

    def generate_password(self):
        if self.var_entry.get() == "":
            messagebox.showerror("Error", "Please enter the password length")
            return
        try:
            num = int(self.var_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return

        if num < 4:
            messagebox.showerror("Error", "Password length must be at least 4")
            return

        # build character sets based on user selection
        s1 = "abcdefghijklmnopqrstuvwxyz" if self.use_lower.get() else ""
        s2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if self.use_upper.get() else ""
        s3 = "0123456789" if self.use_digits.get() else ""
        s4 = "#@_.$" if self.use_special.get() else ""
        
        if not (s1 or s2 or s3 or s4):
            messagebox.showerror("Error", "Select at least one character type")
            return

        def make_one(length):
            pwd_chars = []
            # ensure at least one from each selected category
            if s1:
                pwd_chars.append(random.choice(s1))
            if s2:
                pwd_chars.append(random.choice(s2))
            if s3:
                pwd_chars.append(random.choice(s3))
            if s4:
                pwd_chars.append(random.choice(s4))
            
            pool = list(s1) + list(s2) + list(s3) + list(s4)
            for _ in range(length - len(pwd_chars)):
                pwd_chars.append(random.choice(pool))
            random.shuffle(pwd_chars)
            
            # ensure password doesn't end with special character
            password = ''.join(pwd_chars)
            while password and password[-1] in "#@_.$":
                pwd_chars = list(password)
                random.shuffle(pwd_chars)
                password = ''.join(pwd_chars)
            return password

        generated = [make_one(num)]

        # show the most recently generated password
        self.display_var.set(generated[-1])

        # insert into history (most recent at top)
        for pwd in generated:
            self.history_listbox.insert(0, pwd)

        # calculate strength (use most recent generated)
        pwd = generated[-1]
        score = 0
        if len(pwd) >= 12:
            score += 3
        elif len(pwd) >= 8:
            score += 2
        elif len(pwd) >= 6:
            score += 1

        has_lower = any(c.islower() for c in pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_special = any(c in "#@_.$" for c in pwd)
        score += has_lower + has_upper + has_digit + has_special

        max_score = 7
        percent = int((score / max_score) * 100)

        if percent < 40:
            strength_text = 'Weak'
        elif percent < 70:
            strength_text = 'Medium'
        elif percent < 90:
            strength_text = 'Strong'
        else:
            strength_text = 'Very Strong'

        self.strength_var.set(f"Strength: {strength_text}")

    def copy_to_clipboard(self):
        # prefer selected history item
        sel = self.history_listbox.curselection()
        if sel:
            pwd = self.history_listbox.get(sel[0])
        else:
            pwd = self.display_var.get()
        if not pwd:
            messagebox.showinfo("Info", "No password to copy")
            return
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Password copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy to clipboard: {e}")

    def clear_fields(self):
        self.var_entry.set("")
        self.display_var.set("")
        self.strength_var.set("Strength: ")
        # clear selection in history
        try:
            self.history_listbox.selection_clear(0, END)
        except Exception:
            pass
        

    def clear_history(self):
        try:
            if messagebox.askyesno("Confirm", "Clear all password history?"):
                self.history_listbox.delete(0, END)
                self.display_var.set("")
                self.strength_var.set("Strength: ")
        except Exception:
            pass

    

    def toggle_theme(self):
        if not self.is_dark:
            bg = '#2e2e2e'
            fg = 'white'
            widget_bg = '#3b3b3b'
        else:
            bg = 'white'
            fg = 'black'
            widget_bg = 'white'
        self.is_dark = not self.is_dark
        try:
            self.main_frame.config(bg=bg)
            self.title_lbl.config(bg=bg, fg=fg)
            self.length_label.config(bg=bg, fg=fg)
            self.suggest_label.config(bg=bg, fg='lightgray' if not self.is_dark else 'gray')
            self.pass_label.config(bg=bg, fg=fg)
            # update displayed password entry colors
            try:
                self.show_pass_entry.config(bg=widget_bg, fg='lightgreen' if self.is_dark else 'green')
                self.visibility_canvas.config(bg=widget_bg)
            except Exception:
                pass
            self.strength_label.config(bg=bg, fg=fg)
            # update history bg/fg
            self.history_listbox.config(bg=widget_bg, fg=fg)
        except Exception:
            pass

    def on_history_select(self, event):
        sel = event.widget.curselection()
        if not sel:
            return
        pwd = event.widget.get(sel[0])
        self.display_var.set(pwd)

    def toggle_visibility(self):
        # Toggle masking of the displayed password
        try:
            if self.is_hidden:
                # currently hidden -> show (open eye)
                self.show_pass_entry.config(show='')
                try:
                    self.visibility_canvas.delete("all")
                    self.visibility_canvas.create_text(2, 20, text="👁️", font=("Courier New", 16, "bold"), fill="black", anchor="w")
                except Exception:
                    pass
                self.is_hidden = False
            else:
                # currently visible -> hide (closed eye)
                self.show_pass_entry.config(show='*')
                try:
                    self.visibility_canvas.delete("all")
                    self.visibility_canvas.create_text(2, 20, text="⊘", font=("Courier New", 16, "bold"), fill="black", anchor="w")
                except Exception:
                    pass
                self.is_hidden = True
        except Exception:
            pass


if __name__ == "__main__":
    root = Tk()
    obj = password_generator(root)
    root.mainloop()
