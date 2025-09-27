import tkinter as tk
from tkinter import messagebox, ttk
import easygui
import webbrowser
import random
import time
import threading
import subprocess
import os
from PIL import Image, ImageTk
import requests
from io import BytesIO
import psutil
from AppKit import NSWorkspace, NSApplication

class DistractionManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DistructMe - Distraction Manager")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')
        
        # Distraction types
        self.distractions = {
            "NGMI Message": self.ngmi_message,
            "Cat Meme": self.cat_meme,
            "YouTube Video": self.youtube_video,
            "Window Spam (6)": self.window_spam_6,
            "Window Spam (7)": self.window_spam_7,
            "Random Popup": self.random_popup,
            "Meme Popup": self.meme_popup,
            "Text Editor NGMI": self.text_editor_ngmi
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎯 DistructMe - Ultimate Distraction Suite", 
            font=("Arial", 20, "bold"),
            fg='#e74c3c',
            bg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Description
        desc_label = tk.Label(
            self.root,
            text="Choose your distraction weapon of choice:",
            font=("Arial", 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        desc_label.pack(pady=10)
        
        # Distraction buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Create buttons for each distraction
        row = 0
        col = 0
        for distraction_name in self.distractions.keys():
            btn = tk.Button(
                buttons_frame,
                text=distraction_name,
                command=lambda name=distraction_name: self.trigger_distraction(name),
                font=("Arial", 10, "bold"),
                bg='#3498db',
                fg='white',
                width=15,
                height=2,
                relief='raised',
                bd=3
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(3):
            buttons_frame.columnconfigure(i, weight=1)
        
        # Random distraction button
        random_btn = tk.Button(
            self.root,
            text="🎲 RANDOM DISTRACTION",
            command=self.random_distraction,
            font=("Arial", 14, "bold"),
            bg='#e74c3c',
            fg='white',
            height=3,
            relief='raised',
            bd=5
        )
        random_btn.pack(pady=20, padx=20, fill='x')
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to distract! 🚀",
            font=("Arial", 10),
            fg='#27ae60',
            bg='#2c3e50'
        )
        self.status_label.pack(pady=10)
        
    def trigger_distraction(self, distraction_name):
        """Trigger a specific distraction"""
        self.status_label.config(text=f"Triggering: {distraction_name}...")
        self.root.update()
        
        try:
            self.distractions[distraction_name]()
            self.status_label.config(text=f"✅ {distraction_name} activated!")
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}")
        
    def random_distraction(self):
        """Trigger a random distraction"""
        distraction_name = random.choice(list(self.distractions.keys()))
        self.trigger_distraction(distraction_name)
        
    def ngmi_message(self):
        """Show NGMI message popup"""
        messagebox.showwarning("NGMI Alert", "You got a message from someone!\n\nNGMI (Not Gonna Make It) 🚨")
        
    def cat_meme(self):
        """Open cat meme in browser"""
        meme_url = "https://tenor.com/view/cat-meme-laughing-gif-lol-funny-loud-laugh-gif-7926424135311815001"
        webbrowser.open(meme_url)
        
    def youtube_video(self):
        """Open a long YouTube video"""
        long_videos = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - GANGNAM STYLE
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito
            "https://www.youtube.com/watch?v=YQHsXMglC9A",  # Hello - Adele
            "https://www.youtube.com/watch?v=JGwWNGJdvx8"   # Shape of You - Ed Sheeran
        ]
        video_url = random.choice(long_videos)
        webbrowser.open(video_url)
        
    def window_spam_6(self):
        """Create 6 windows in the shape of a 6"""
        self.create_number_windows(6)
        
    def window_spam_7(self):
        """Create 7 windows in the shape of a 7"""
        self.create_number_windows(7)
        
    def create_number_windows(self, number):
        """Create windows in the shape of a number"""
        if number == 6:
            # Create windows in the shape of 6
            positions = [
                (100, 100), (150, 100), (200, 100),  # Top horizontal
                (100, 150), (100, 200), (100, 250),  # Left vertical
                (100, 300), (150, 300), (200, 300),  # Bottom horizontal
                (200, 250), (200, 200), (200, 150),  # Right vertical
                (100, 200), (150, 200), (200, 200),  # Middle horizontal
            ]
        else:  # 7
            # Create windows in the shape of 7
            positions = [
                (100, 100), (150, 100), (200, 100),  # Top horizontal
                (200, 150), (200, 200), (200, 250),  # Right vertical
                (200, 300), (150, 300), (100, 300),  # Bottom horizontal
            ]
        
        for i, (x, y) in enumerate(positions):
            self.create_popup_window(f"Window {i+1}", x, y)
            
    def create_popup_window(self, title, x, y):
        """Create a popup window at specific position"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry(f"200x150+{x}+{y}")
        popup.configure(bg='#e74c3c')
        
        label = tk.Label(
            popup,
            text=f"🎯 {title}",
            font=("Arial", 12, "bold"),
            fg='white',
            bg='#e74c3c'
        )
        label.pack(expand=True)
        
        # Auto-close after 3 seconds
        popup.after(3000, popup.destroy)
        
    def random_popup(self):
        """Show a random popup message"""
        messages = [
            "You've been distracted! 🎯",
            "Focus broken! 💥",
            "Distraction successful! 🚀",
            "Mission accomplished! ✅",
            "You fell for it! 😂",
            "NGMI! 🚨",
            "Distraction deployed! 🎪"
        ]
        message = random.choice(messages)
        messagebox.showinfo("Distraction Alert", message)
        
    def meme_popup(self):
        """Create a meme popup window"""
        meme_window = tk.Toplevel(self.root)
        meme_window.title("Meme Alert")
        meme_window.geometry("400x300")
        meme_window.configure(bg='#2c3e50')
        
        # Meme text
        meme_texts = [
            "DISTRACTION ACTIVATED",
            "YOU GOT DISTRACTED",
            "FOCUS = BROKEN",
            "NGMI ALERT",
            "DISTRACTION SUCCESS"
        ]
        
        meme_text = random.choice(meme_texts)
        label = tk.Label(
            meme_window,
            text=meme_text,
            font=("Arial", 20, "bold"),
            fg='#e74c3c',
            bg='#2c3e50'
        )
        label.pack(expand=True)
        
        # Close button
        close_btn = tk.Button(
            meme_window,
            text="Close",
            command=meme_window.destroy,
            bg='#3498db',
            fg='white',
            font=("Arial", 12, "bold")
        )
        close_btn.pack(pady=10)
        
    def text_editor_ngmi(self):
        """Open a text editor with NGMI content"""
        # Create a text editor window
        editor = tk.Toplevel(self.root)
        editor.title("Text Editor - NGMI")
        editor.geometry("500x400")
        editor.configure(bg='#2c3e50')
        
        # Text area
        text_area = tk.Text(
            editor,
            font=("Courier", 12),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='white'
        )
        text_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Insert NGMI content
        ngmi_content = """NGMI - Not Gonna Make It

You got a message from someone!

This is a distraction text editor.
Your focus has been successfully broken.

NGMI = Not Gonna Make It
You're not gonna make it if you keep getting distracted!

🚨 DISTRACTION SUCCESSFUL 🚨

Type here if you want... but you're already distracted!"""
        
        text_area.insert('1.0', ngmi_content)
        
        # Buttons
        button_frame = tk.Frame(editor, bg='#2c3e50')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        save_btn = tk.Button(
            button_frame,
            text="Save (NGMI)",
            command=lambda: messagebox.showinfo("Save", "File saved as NGMI.txt"),
            bg='#27ae60',
            fg='white'
        )
        save_btn.pack(side='left', padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=editor.destroy,
            bg='#e74c3c',
            fg='white'
        )
        close_btn.pack(side='right', padx=5)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = DistractionManager()
    app.run()
