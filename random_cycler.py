#!/usr/bin/env python3
"""
Random Distraction Cycler

Automatically cycles through different distraction types every 6 seconds:
- Memes (local and online)
- Videos (YouTube)
- GIFs (animated content)
- Streams (Twitch/YouTube live)
"""

import random
import time
import threading
import webbrowser
import tkinter as tk
from typing import List, Dict, Optional, Callable
from windows_manager import WindowsManager
from processes.meme_popup import open_meme_popup
from processes.media_link_opener import open_random_media
from processes.ngmi_popup import open_ngmi_editor
from processes.number_game import NumberGame

class RandomDistractionCycler:
    def __init__(self, manager: WindowsManager, on_distraction: Optional[Callable] = None):
        """
        Initialize the random distraction cycler.
        
        Args:
            manager: WindowsManager instance for creating windows
            on_distraction: Callback function when distraction is triggered
        """
        self.manager = manager
        self.on_distraction = on_distraction
        self.cycling = False
        self.cycle_thread = None
        self.cycle_interval = 6.0  # 6 seconds
        
        # Distraction types and their content
        self.distraction_types = {
            "meme": {
                "name": "Meme Popup",
                "content": [
                    "memes/tenor.gif",
                    "memes/tenor (1).gif", 
                    "memes/tenor (2).gif",
                    "memes/tenor (3).gif",
                    "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
                    "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",
                    "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",
                ]
            },
            "video": {
                "name": "YouTube Video",
                "content": [
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
                    "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - GANGNAM STYLE
                    "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito
                    "https://www.youtube.com/watch?v=YQHsXMglC9A",  # Hello - Adele
                    "https://www.youtube.com/watch?v=JGwWNGJdvx8",  # Shape of You - Ed Sheeran
                    "https://www.youtube.com/@KaiCenat",
                    "https://www.youtube.com/@GamesDoneQuick",
                    "https://www.youtube.com/@SummoningSalt",
                ]
            },
            "gif": {
                "name": "Animated GIF",
                "content": [
                    "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",  # cat typing
                    "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif",  # laughing cat
                    "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",  # cat laugh roll
                    "https://media.giphy.com/media/26BRrSvJUoB0z2xMQ/giphy.gif",  # dancing cat
                    "https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif",  # cat keyboard
                    "https://media.giphy.com/media/3o6Zt4HU9u8vq/giphy.gif",  # cat surprise
                ]
            },
            "stream": {
                "name": "Live Stream",
                "content": [
                    "https://www.twitch.tv/kaicenat",
                    "https://www.twitch.tv/xqc",
                    "https://www.twitch.tv/sykkuno",
                    "https://www.twitch.tv/valkyrae",
                    "https://www.twitch.tv/corpse_husband",
                    "https://www.twitch.tv/gamesdonequick",
                    "https://www.twitch.tv/speedrun",
                ]
            }
        }
        
        # Initialize number game for interactive distractions
        self.number_game = NumberGame(manager)
        
    def start_cycling(self, interval: float = 6.0):
        """
        Start the random distraction cycling.
        
        Args:
            interval: How often to trigger distractions (seconds)
        """
        if self.cycling:
            return
            
        self.cycling = True
        self.cycle_interval = interval
        self.cycle_thread = threading.Thread(
            target=self._cycle_loop,
            daemon=True
        )
        self.cycle_thread.start()
        print(f"🎪 Random distraction cycling started! (every {interval}s)")
        
    def stop_cycling(self):
        """Stop the random distraction cycling."""
        self.cycling = False
        if self.cycle_thread:
            self.cycle_thread.join(timeout=1)
        print("🛑 Random distraction cycling stopped!")
        
    def _cycle_loop(self):
        """Main cycling loop that runs in background thread."""
        while self.cycling:
            try:
                # Randomly select distraction type
                distraction_type = random.choice(list(self.distraction_types.keys()))
                self._trigger_distraction(distraction_type)
                
                # Wait for next cycle
                time.sleep(self.cycle_interval)
                
            except Exception as e:
                print(f"❌ Error in distraction cycle: {e}")
                time.sleep(self.cycle_interval)
                
    def _trigger_distraction(self, distraction_type: str):
        """Trigger a specific type of distraction."""
        distraction_info = self.distraction_types[distraction_type]
        content = random.choice(distraction_info["content"])
        
        print(f"🎯 Triggering {distraction_info['name']}: {content}")
        
        try:
            if distraction_type == "meme":
                self._trigger_meme_distraction(content)
            elif distraction_type == "video":
                self._trigger_video_distraction(content)
            elif distraction_type == "gif":
                self._trigger_gif_distraction(content)
            elif distraction_type == "stream":
                self._trigger_stream_distraction(content)
                
            # Execute callback if provided
            if self.on_distraction:
                self.on_distraction(distraction_type, content)
                
        except Exception as e:
            print(f"❌ Error triggering {distraction_type}: {e}")
            
    def _trigger_meme_distraction(self, content: str):
        """Trigger meme popup distraction."""
        def on_click():
            # Escalate with more distractions
            self._trigger_random_escalation()
            
        open_meme_popup(self.manager, content, on_click)
        
    def _trigger_video_distraction(self, content: str):
        """Trigger YouTube video distraction."""
        webbrowser.open(content)
        
    def _trigger_gif_distraction(self, content: str):
        """Trigger animated GIF distraction."""
        def on_click():
            # Escalate with more distractions
            self._trigger_random_escalation()
            
        open_meme_popup(self.manager, content, on_click)
        
    def _trigger_stream_distraction(self, content: str):
        """Trigger live stream distraction."""
        webbrowser.open(content)
        
    def _trigger_random_escalation(self):
        """Trigger random escalation distractions."""
        escalation_options = [
            lambda: open_random_media(),
            lambda: open_ngmi_editor(self.manager, refresh_interval_ms=3000, editable=True),
            lambda: self.number_game.start(),
        ]
        
        # 70% chance of escalation
        if random.random() < 0.7:
            random.choice(escalation_options)()
            
    def trigger_manual_distraction(self, distraction_type: str = None):
        """Manually trigger a specific distraction type."""
        if distraction_type is None:
            distraction_type = random.choice(list(self.distraction_types.keys()))
            
        self._trigger_distraction(distraction_type)
        
    def set_cycle_interval(self, interval: float):
        """Set the cycling interval."""
        self.cycle_interval = interval
        print(f"⏱️ Cycle interval set to {interval} seconds")
        
    def is_cycling(self) -> bool:
        """Check if cycling is active."""
        return self.cycling
        
    def get_available_distractions(self) -> List[str]:
        """Get list of available distraction types."""
        return list(self.distraction_types.keys())

# Example usage and testing
if __name__ == "__main__":
    import tkinter as tk
    from windows_manager import WindowsManager
    
    # Create test window
    root = tk.Tk()
    root.title("Random Distraction Cycler Test")
    root.geometry("400x300")
    
    manager = WindowsManager(root)
    cycler = RandomDistractionCycler(manager)
    
    # Test controls
    tk.Label(root, text="Random Distraction Cycler Test", font=("Arial", 16, "bold")).pack(pady=10)
    
    def start_cycling():
        cycler.start_cycling(interval=6.0)
        status_label.config(text="🎪 Cycling started!")
        
    def stop_cycling():
        cycler.stop_cycling()
        status_label.config(text="🛑 Cycling stopped!")
        
    def trigger_meme():
        cycler.trigger_manual_distraction("meme")
        
    def trigger_video():
        cycler.trigger_manual_distraction("video")
        
    def trigger_gif():
        cycler.trigger_manual_distraction("gif")
        
    def trigger_stream():
        cycler.trigger_manual_distraction("stream")
    
    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Start Cycling", command=start_cycling, bg='#27ae60', fg='white').pack(side='left', padx=5)
    tk.Button(button_frame, text="Stop Cycling", command=stop_cycling, bg='#e74c3c', fg='white').pack(side='left', padx=5)
    
    manual_frame = tk.Frame(root)
    manual_frame.pack(pady=10)
    
    tk.Button(manual_frame, text="Meme", command=trigger_meme, bg='#3498db', fg='white').pack(side='left', padx=2)
    tk.Button(manual_frame, text="Video", command=trigger_video, bg='#e67e22', fg='white').pack(side='left', padx=2)
    tk.Button(manual_frame, text="GIF", command=trigger_gif, bg='#9b59b6', fg='white').pack(side='left', padx=2)
    tk.Button(manual_frame, text="Stream", command=trigger_stream, bg='#9146FF', fg='white').pack(side='left', padx=2)
    
    status_label = tk.Label(root, text="Ready to cycle...", font=("Arial", 12))
    status_label.pack(pady=10)
    
    # Start the test
    root.mainloop()
