#!/usr/bin/env python3
"""
Chrome Tab Monitor
Detects when user switches tabs and shows meme popups to disturb them
"""

import subprocess
import time
import os
from pathlib import Path

def get_current_chrome_tab():
    """Get the current active Chrome tab title and URL"""
    try:
        script = '''
        tell application "Google Chrome"
            if (count of windows) > 0 then
                set activeTab to active tab of front window
                set tabTitle to title of activeTab
                set tabURL to URL of activeTab
                return tabTitle & "|||" & tabURL
            end if
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=3
        )
        
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split('|||', 1)
            if len(parts) == 2:
                return {
                    'title': parts[0].strip(),
                    'url': parts[1].strip()
                }
        return None
    except Exception as e:
        print(f"Error getting Chrome tab: {e}")
        return None

def show_meme_popup():
    """Show a popup window beside the apps using AppleScript"""
    try:
        # Create a popup window using AppleScript
        script = '''
        tell application "Google Chrome"
            if (count of windows) > 0 then
                tell front window
                    set newTab to make new tab with properties {URL:"file:///Users/voicepodcast/DistructMe/DistructMe/meme_popup.html"}
                end tell
            end if
        end tell
        
        -- Create a separate popup window
        tell application "System Events"
            tell process "Google Chrome"
                set frontmost to true
            end tell
        end tell
        
        tell application "Google Chrome"
            make new window with properties {URL:"file:///Users/voicepodcast/DistructMe/DistructMe/meme_popup.html"}
            set bounds of front window to {1200, 100, 1700, 600}
        end tell
        '''
        
        subprocess.run([
            "osascript", "-e", script
        ], check=True)
        print("🎭 Meme popup window opened beside apps!")
    except subprocess.CalledProcessError:
        print("❌ Failed to open meme popup window")

def check_chrome_running():
    """Check if Chrome is currently running"""
    try:
        result = subprocess.run([
            "pgrep", "-f", "Google Chrome"
        ], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def is_distracting_site(url):
    """Check if the URL is a distracting site that should trigger memes"""
    distracting_sites = [
        'netflix.com', 'youtube.com', 'facebook.com', 'instagram.com', 
        'twitter.com', 'tiktok.com', 'reddit.com', 'twitch.tv',
        'pinterest.com', 'snapchat.com', 'discord.com', 'spotify.com',
        'amazon.com', 'ebay.com', 'shopping', 'entertainment'
    ]
    
    url_lower = url.lower()
    return any(site in url_lower for site in distracting_sites)

def monitor_tabs():
    """Monitor Chrome tabs and show memes when user switches to distracting sites"""
    print("🎭 DistructMe Tab Monitor Started")
    print("👀 Watching your Chrome tabs in real-time...")
    print("🎪 Memes will appear when you visit distracting sites!")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    if not check_chrome_running():
        print("❌ Chrome is not running. Please open Chrome first.")
        return
    
    last_tab = None
    tab_switch_count = 0
    
    try:
        while True:
            if not check_chrome_running():
                print("⚠️  Chrome closed, waiting for it to reopen...")
                time.sleep(2)
                continue
            
            current_tab = get_current_chrome_tab()
            
            if current_tab:
                # Check if tab changed
                if last_tab is None:
                    last_tab = current_tab
                    print(f"📍 Started monitoring: {current_tab['title']}")
                elif (last_tab['title'] != current_tab['title'] or 
                      last_tab['url'] != current_tab['url']):
                    
                    tab_switch_count += 1
                    print(f"🔄 Tab switched! ({tab_switch_count} switches)")
                    print(f"   From: {last_tab['title']}")
                    print(f"   To: {current_tab['title']}")
                    print(f"   URL: {current_tab['url']}")
                    
                    # Check if it's a distracting site
                    if is_distracting_site(current_tab['url']):
                        print("🚨 DISTRACTING SITE DETECTED! Showing meme...")
                        show_meme_popup()
                    else:
                        print("✅ Productive site, no meme needed")
                    
                    last_tab = current_tab
            
            time.sleep(0.5)  # Check every 0.5 seconds for real-time detection
            
    except KeyboardInterrupt:
        print(f"\n👋 Tab monitor stopped. You switched tabs {tab_switch_count} times!")
        print("🎯 Mission accomplished - you were successfully distracted!")

if __name__ == "__main__":
    monitor_tabs()
