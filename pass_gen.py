import string
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import random

class password_generator:
    def __init__(self,root):
        self.root=root
        self.root.title("Password Generator")
        self.root.geometry("600x600+370+50")

        main_frame=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        main_frame.place(x=0,y=0,width=600,height=600)

        title_lbl=Label(main_frame,text="PASSWORD GENERATOR",font=("times new roman",20,"bold"),bg="white",fg="black").place(x=0,y=0,width=600)

        try:
            img1=Image.open("pass_gen.png") 
            img1 = img1.resize((596,280), Image.Resampling.LANCZOS)
            self.photoimg1=ImageTk.PhotoImage(img1)
            lblimg1=Label(main_frame,image=self.photoimg1).place(x=0,y=50,width=600,height=190)
        except:
            pass

        length_label=Label(main_frame,text="Enter Password Length",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=40,y=250)

        self.var_entry=StringVar()
        
        entry_fill=ttk.Entry(main_frame,textvariable=self.var_entry,width=51,font=("times new roman",15,"bold"))
        entry_fill.place(x=42,y=290)

        btn=Button(main_frame,text="GENERATE PASSWORD",font=("times new roman",15,"bold"),bg="blue",fg="white",bd=4,relief=GROOVE,cursor="hand2",command=self.generate_password).place(x=40,y=340,width=520,height=40)

        pass_label=Label(main_frame,text="Generated Password",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=40,y=400)

        self.show_pass_label=Label(main_frame,text="",font=("times new roman",15,"bold"),bg="white",fg="green",bd=2,relief=GROOVE)
        self.show_pass_label.place(x=40,y=440,width=520,height=40)

    def generate_password(self):
        if self.var_entry.get() == "":
            messagebox.showerror("Error","Please enter the password length")
        else:
            try:
                num=int(self.var_entry.get())
                
                if num < 4:
                    messagebox.showerror("Error","Password length must be at least 4")
                    return
                
                s1="abcdefghijklmnopqrstuvwxyz"
                s2="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                s3="0123456789"
                s4="#@_.$"

                password=[]
                # Add at least one character from each category
                password.append(random.choice(s1))
                password.append(random.choice(s2))
                password.append(random.choice(s3))
                password.append(random.choice(s4))
                
                # Fill remaining characters randomly from all categories
                s=[]
                s.extend(list(s1))
                s.extend(list(s2))
                s.extend(list(s3))
                s.extend(list(s4))
                
                for _ in range(num - 4):
                    password.append(random.choice(s))
                
                # Shuffle the password so it doesn't follow a pattern
                random.shuffle(password)
                final_password=''.join(password)

                self.show_pass_label.config(text=final_password)
            except ValueError:
                messagebox.showerror("Error","Please enter a valid number")

            

if __name__=="__main__":
    root=Tk()
    obj=password_generator(root)
    root.mainloop()