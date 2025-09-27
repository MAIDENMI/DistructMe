import os
import random
import subprocess
import tkinter as tk
from typing import Optional

from windows_manager import WindowsManager
from processes.ngmi_popup import open_ngmi_editor
from processes.meme_popup import open_meme_popup
from processes.media_link_opener import open_random_media
from processes.number_game import NumberGame
from tab_switch_detector import TabSwitchDetector
from random_cycler import RandomDistractionCycler


def _get_frontmost_app_name_mac() -> Optional[str]:
    """Return the frontmost app on macOS using AppleScript. Fallbacks to None."""
    try:
        script = 'tell application "System Events" to get name of first process whose frontmost is true'
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        name = result.stdout.strip()
        return name or None
    except Exception:
        return None


def _get_active_chrome_tab_title() -> Optional[str]:
    """Return active Google Chrome tab title if Chrome is frontmost. Fallbacks to None."""
    try:
        script = (
            'tell application "Google Chrome"\n'
            'if (count of windows) > 0 then\n'
            'set theTitle to title of active tab of front window\n'
            'return theTitle\n'
            'end if\n'
            'end tell'
        )
        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True, check=True
        )
        title = result.stdout.strip()
        return title or None
    except Exception:
        return None


class DistractorApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("NGMI Distractor")
        self.root.geometry("480x400")
        self.manager = WindowsManager(self.root)
        self.number_game = NumberGame(self.manager)
        
        # Initialize tab switch detector
        self.tab_detector = TabSwitchDetector(on_tab_switch=self._on_tab_switch)
        
        # Initialize random distraction cycler
        self.random_cycler = RandomDistractionCycler(self.manager, on_distraction=self._on_random_distraction)

        # Basic control panel
        tk.Label(self.root, text="NGMI Distractor", font=("Helvetica", 18, "bold")).pack(pady=8)
        self.status_var = tk.StringVar(value="Ready to distract…")
        tk.Label(self.root, textvariable=self.status_var).pack(pady=4)

        # Main buttons
        buttons = tk.Frame(self.root)
        buttons.pack(pady=8)
        tk.Button(buttons, text="Meme Now", command=self.trigger_meme_distraction).grid(row=0, column=0, padx=6)
        tk.Button(buttons, text="NGMI Editor Now", command=self.trigger_ngmi_distraction).grid(row=0, column=1, padx=6)
        tk.Button(buttons, text="Number Game", command=self.trigger_number_game).grid(row=0, column=2, padx=6)
        tk.Button(buttons, text="Open Media", command=open_random_media).grid(row=0, column=3, padx=6)
        
        # Tab monitoring controls
        tab_frame = tk.Frame(self.root)
        tab_frame.pack(pady=8)
        
        tk.Label(tab_frame, text="Tab Monitoring:", font=("Helvetica", 12, "bold")).pack()
        
        tab_buttons = tk.Frame(tab_frame)
        tab_buttons.pack(pady=4)
        
        self.tab_monitor_btn = tk.Button(
            tab_buttons, 
            text="🔍 Start Tab Monitor", 
            command=self.toggle_tab_monitoring,
            bg='#9146FF',
            fg='white',
            font=("Helvetica", 10, "bold")
        )
        self.tab_monitor_btn.pack(side='left', padx=5)
        
        tk.Button(
            tab_buttons, 
            text="🚀 Speed Stream Now", 
            command=self.trigger_kai_cenat_popup,
            bg='#00D4AA',
            fg='white',
            font=("Helvetica", 10, "bold")
        ).pack(side='left', padx=5)
        
        # Random cycling controls
        cycle_frame = tk.Frame(self.root)
        cycle_frame.pack(pady=8)
        
        tk.Label(cycle_frame, text="Random Cycling:", font=("Helvetica", 12, "bold")).pack()
        
        cycle_buttons = tk.Frame(cycle_frame)
        cycle_buttons.pack(pady=4)
        
        self.cycle_btn = tk.Button(
            cycle_buttons, 
            text="🎪 Start Random Cycle", 
            command=self.toggle_random_cycling,
            bg='#9b59b6',
            fg='white',
            font=("Helvetica", 10, "bold")
        )
        self.cycle_btn.pack(side='left', padx=5)
        
        tk.Button(
            cycle_buttons, 
            text="🎯 Random Now", 
            command=self.trigger_random_distraction,
            bg='#e67e22',
            fg='white',
            font=("Helvetica", 10, "bold")
        ).pack(side='left', padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self._on_exit)

        # Kick off scheduling loop
        self._schedule_next_distraction(initial_delay_ms=1500)

    # ---------------------------- Scheduling ---------------------------- #
    def _schedule_next_distraction(self, initial_delay_ms: Optional[int] = None) -> None:
        delay_ms = initial_delay_ms if initial_delay_ms is not None else random.randint(8000, 16000)
        self.root.after(delay_ms, self._run_random_distraction)

    def _run_random_distraction(self) -> None:
        front_app = _get_frontmost_app_name_mac()
        # Light heuristic: if user is in Chrome or a code editor, increase chance of heavier distraction
        heavy_weight = 0.6 if (front_app and any(k in front_app.lower() for k in ["chrome", "code", "cursor"])) else 0.35
        choices = [self.trigger_meme_distraction, self.trigger_ngmi_distraction, self.trigger_number_game]
        weights = [0.5, 0.3, heavy_weight]
        # Normalize weights
        s = sum(weights)
        weights = [w / s for w in weights]
        random.choices(choices, weights=weights, k=1)[0]()
        self._schedule_next_distraction()

    # ---------------------------- Actions ---------------------------- #
    def trigger_meme_distraction(self) -> None:
        self.status_var.set("Meme popup dispatched…")
        meme_urls = [
            # Classic cat memes; if any fail, popup will fallback to text
            "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",  # cat typing
            "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",  # laughing cat
            "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",  # cat laugh roll
            # Local memes (add your meme file here)
            "memes/tenor.gif",  # Your custom meme
        ]
        url = random.choice(meme_urls)

        def on_click() -> None:
            # Clicking the meme escalates distractions
            open_random_media()
            # Also spawn an NGMI editor shortly after
            self.root.after(1200, self.trigger_ngmi_distraction)
            # Potentially kick off the number game as well
            if random.random() < 0.5:
                self.root.after(2000, self.trigger_number_game)

        open_meme_popup(self.manager, url, on_click)

    def trigger_ngmi_distraction(self) -> None:
        self.status_var.set("NGMI editor dispatched…")
        open_ngmi_editor(self.manager, refresh_interval_ms=random.randint(2500, 5000), editable=True)

    def trigger_number_game(self) -> None:
        self.status_var.set("Number game dispatched…")
        self.number_game.start()
        
    def toggle_tab_monitoring(self) -> None:
        """Toggle tab monitoring on/off."""
        if self.tab_detector.is_monitoring():
            self.tab_detector.stop_monitoring()
            self.tab_monitor_btn.config(text="🔍 Start Tab Monitor", bg='#9146FF')
            self.status_var.set("Tab monitoring stopped…")
        else:
            self.tab_detector.start_monitoring(check_interval=2.0)
            self.tab_monitor_btn.config(text="🛑 Stop Tab Monitor", bg='#FF6B6B')
            self.status_var.set("Tab monitoring started - Speed stream popups on tab switch!")
            
    def trigger_kai_cenat_popup(self) -> None:
        """Manually trigger speed stream popup."""
        self.status_var.set("Speed stream popup dispatched…")
        self.tab_detector._trigger_kai_cenat_popup()
        
    def _on_tab_switch(self, tabs) -> None:
        """Handle tab switch detection."""
        self.status_var.set(f"Tab switch detected! {len(tabs)} tabs open…")
        print(f"🔄 Tab switch detected! {len(tabs)} tabs currently open")
        
    def toggle_random_cycling(self) -> None:
        """Toggle random distraction cycling on/off."""
        if self.random_cycler.is_cycling():
            self.random_cycler.stop_cycling()
            self.cycle_btn.config(text="🎪 Start Random Cycle", bg='#9b59b6')
            self.status_var.set("Random cycling stopped…")
        else:
            self.random_cycler.start_cycling(interval=6.0)
            self.cycle_btn.config(text="🛑 Stop Random Cycle", bg='#e74c3c')
            self.status_var.set("Random cycling started - memes, videos, GIFs, streams every 6s!")
            
    def trigger_random_distraction(self) -> None:
        """Manually trigger a random distraction."""
        self.status_var.set("Random distraction dispatched…")
        self.random_cycler.trigger_manual_distraction()
        
    def _on_random_distraction(self, distraction_type: str, content: str) -> None:
        """Handle random distraction callback."""
        self.status_var.set(f"Random {distraction_type} triggered!")
        print(f"🎯 Random {distraction_type}: {content}")

    # ---------------------------- Exit ---------------------------- #
    def _on_exit(self) -> None:
        try:
            self.tab_detector.stop_monitoring()
            self.random_cycler.stop_cycling()
            self.manager.close_all()
        finally:
            self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    app = DistractorApp()
    app.run()
