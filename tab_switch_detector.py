#!/usr/bin/env python3
"""
Tab Switch Detector with Kai Cenat Speed Stream Integration

Monitors Chrome tab switches and triggers Kai Cenat speed stream popups
when users switch between tabs.
"""

import subprocess
import time
import threading
import webbrowser
import tkinter as tk
from typing import List, Dict, Optional, Callable
from chrome_tab_monitor import get_chrome_tabs

class TabSwitchDetector:
    def __init__(self, on_tab_switch: Optional[Callable] = None):
        """
        Initialize the tab switch detector.
        
        Args:
            on_tab_switch: Callback function to execute when tab switch is detected
        """
        self.on_tab_switch = on_tab_switch
        self.monitoring = False
        self.monitor_thread = None
        self.previous_tabs = []
        self.kai_cenat_streams = [
            "https://www.twitch.tv/kaicenat",
            "https://www.twitch.tv/kaicenat/videos",
            "https://www.youtube.com/@KaiCenat",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll as backup
        ]
        
        # Additional speed streamers and content
        self.speed_streams = [
            # Kai Cenat streams
            "https://www.twitch.tv/kaicenat",
            "https://www.twitch.tv/kaicenat/videos",
            "https://www.youtube.com/@KaiCenat",
            
            # Other popular speed streamers
            "https://www.twitch.tv/xqc",
            "https://www.twitch.tv/xqcow",
            "https://www.twitch.tv/sykkuno",
            "https://www.twitch.tv/valkyrae",
            "https://www.twitch.tv/corpse_husband",
            
            # Speed content and challenges
            "https://www.youtube.com/results?search_query=speed+stream",
            "https://www.youtube.com/results?search_query=fast+streaming",
            "https://www.youtube.com/results?search_query=speed+run+stream",
            
            # Popular speed run channels
            "https://www.youtube.com/@GamesDoneQuick",
            "https://www.youtube.com/@SummoningSalt",
            "https://www.youtube.com/@Tomatoanus",
            
            # Chaos content
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll
            "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - GANGNAM STYLE
            "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito
            "https://www.youtube.com/watch?v=YQHsXMglC9A",  # Hello - Adele
            "https://www.youtube.com/watch?v=JGwWNGJdvx8",  # Shape of You - Ed Sheeran
            
            # Speed run specific games
            "https://www.youtube.com/results?search_query=mario+speed+run",
            "https://www.youtube.com/results?search_query=zelda+speed+run",
            "https://www.youtube.com/results?search_query=sonic+speed+run",
            "https://www.youtube.com/results?search_query=minecraft+speed+run",
        ]
        
    def start_monitoring(self, check_interval: float = 2.0):
        """
        Start monitoring for tab switches.
        
        Args:
            check_interval: How often to check for tab changes (seconds)
        """
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(check_interval,),
            daemon=True
        )
        self.monitor_thread.start()
        print("🔍 Tab switch monitoring started!")
        
    def stop_monitoring(self):
        """Stop monitoring for tab switches."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("🛑 Tab switch monitoring stopped!")
        
    def _monitor_loop(self, check_interval: float):
        """Main monitoring loop that runs in background thread."""
        while self.monitoring:
            try:
                current_tabs = get_chrome_tabs()
                
                # Check if tabs have changed
                if self._tabs_changed(current_tabs):
                    print("🔄 Tab switch detected!")
                    self._handle_tab_switch(current_tabs)
                    
                self.previous_tabs = current_tabs.copy()
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"❌ Error monitoring tabs: {e}")
                time.sleep(check_interval)
                
    def _tabs_changed(self, current_tabs: List[Dict[str, str]]) -> bool:
        """Check if the current tabs are different from previous tabs."""
        if len(current_tabs) != len(self.previous_tabs):
            return True
            
        # Check if any tab URLs have changed
        current_urls = {tab['url'] for tab in current_tabs}
        previous_urls = {tab['url'] for tab in self.previous_tabs}
        
        return current_urls != previous_urls
        
    def _handle_tab_switch(self, current_tabs: List[Dict[str, str]]):
        """Handle tab switch detection."""
        print("🎯 Tab switch detected! Triggering Kai Cenat speed stream...")
        
        # Trigger Kai Cenat speed stream popup
        self._trigger_kai_cenat_popup()
        
        # Execute custom callback if provided
        if self.on_tab_switch:
            try:
                self.on_tab_switch(current_tabs)
            except Exception as e:
                print(f"❌ Error in tab switch callback: {e}")
                
    def _trigger_kai_cenat_popup(self):
        """Trigger speed stream popup with expanded options."""
        import random
        
        # Randomly select from all speed streams
        stream_url = random.choice(self.speed_streams)
        
        # Create popup window
        popup = tk.Toplevel()
        popup.title("SPEED STREAM ALERT! 🚀")
        popup.geometry("500x450")
        popup.configure(bg='#9146FF')  # Twitch purple
        popup.attributes('-topmost', True)
        
        # Center the window
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (500 // 2)
        y = (popup.winfo_screenheight() // 2) - (450 // 2)
        popup.geometry(f"500x450+{x}+{y}")
        
        # Main content
        title_label = tk.Label(
            popup,
            text="SPEED STREAM ALERT! 🚀",
            font=("Arial", 20, "bold"),
            fg='white',
            bg='#9146FF'
        )
        title_label.pack(pady=20)
        
        message_label = tk.Label(
            popup,
            text="You switched tabs! Time for some SPEED content!",
            font=("Arial", 14),
            fg='white',
            bg='#9146FF',
            wraplength=450
        )
        message_label.pack(pady=10)
        
        # Speed stream info
        speed_info = tk.Label(
            popup,
            text="Featuring: Kai Cenat, xQc, Speed Runs, and more!",
            font=("Arial", 12),
            fg='#00D4AA',
            bg='#9146FF'
        )
        speed_info.pack(pady=5)
        
        # Stream info
        info_label = tk.Label(
            popup,
            text="Click below to open a random speed stream:",
            font=("Arial", 12),
            fg='white',
            bg='#9146FF'
        )
        info_label.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(popup, bg='#9146FF')
        button_frame.pack(pady=20)
        
        # Open stream button
        open_btn = tk.Button(
            button_frame,
            text="🚀 OPEN SPEED STREAM",
            command=lambda: self._open_kai_cenat_stream(stream_url),
            font=("Arial", 12, "bold"),
            bg='#00D4AA',  # Twitch green
            fg='white',
            width=20,
            height=2
        )
        open_btn.pack(pady=5)
        
        # Additional speed stream buttons
        extra_buttons = tk.Frame(popup, bg='#9146FF')
        extra_buttons.pack(pady=10)
        
        # xQc button
        xqc_btn = tk.Button(
            extra_buttons,
            text="xQc Stream",
            command=lambda: self._open_kai_cenat_stream("https://www.twitch.tv/xqc"),
            font=("Arial", 10),
            bg='#FF6B6B',
            fg='white',
            width=12
        )
        xqc_btn.pack(side='left', padx=5)
        
        # Speed run button
        speedrun_btn = tk.Button(
            extra_buttons,
            text="Speed Runs",
            command=lambda: self._open_kai_cenat_stream("https://www.youtube.com/@GamesDoneQuick"),
            font=("Arial", 10),
            bg='#4ECDC4',
            fg='white',
            width=12
        )
        speedrun_btn.pack(side='left', padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=popup.destroy,
            font=("Arial", 10),
            bg='#FF6B6B',
            fg='white',
            width=10
        )
        close_btn.pack(pady=5)
        
        # Auto-close after 10 seconds
        popup.after(10000, popup.destroy)
        
    def _open_kai_cenat_stream(self, stream_url: str):
        """Open Kai Cenat stream in browser."""
        print(f"🚀 Opening Kai Cenat stream: {stream_url}")
        webbrowser.open(stream_url)
        
    def get_current_tabs(self) -> List[Dict[str, str]]:
        """Get current Chrome tabs."""
        return get_chrome_tabs()
        
    def is_monitoring(self) -> bool:
        """Check if monitoring is active."""
        return self.monitoring

# Example usage and testing
if __name__ == "__main__":
    def custom_tab_switch_handler(tabs):
        print(f"📊 Current tabs: {len(tabs)}")
        for i, tab in enumerate(tabs[:3]):  # Show first 3 tabs
            print(f"  {i+1}. {tab['title'][:50]}...")
    
    # Create detector
    detector = TabSwitchDetector(on_tab_switch=custom_tab_switch_handler)
    
    # Start monitoring
    detector.start_monitoring(check_interval=1.0)
    
    try:
        print("🔍 Tab switch detector running...")
        print("Switch between Chrome tabs to trigger Kai Cenat popups!")
        print("Press Ctrl+C to stop...")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping tab switch detector...")
        detector.stop_monitoring()
        print("✅ Tab switch detector stopped!")
