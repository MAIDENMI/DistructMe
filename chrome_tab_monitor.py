#!/usr/bin/env python3
"""
Chrome Tab Monitor

A simple function to get all open Chrome tabs with their titles and URLs.
Uses AppleScript to communicate with Google Chrome on macOS.

Usage:
    from chrome_tab_monitor import get_chrome_tabs
    tabs = get_chrome_tabs()
    for tab in tabs:
        print(f"{tab['title']}: {tab['url']}")
"""

import subprocess
from typing import List, Dict

def get_chrome_tabs() -> List[Dict[str, str]]:
    """
    Get all open tabs from all Chrome windows.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing:
            - 'title': The tab title
            - 'url': The tab URL
    
    Example:
        tabs = get_chrome_tabs()
        for tab in tabs:
            print(f"Title: {tab['title']}")
            print(f"URL: {tab['url']}")
    """
    try:
        script = '''
        tell application "Google Chrome"
            set tabList to ""
            repeat with w in windows
                repeat with t in tabs of w
                    set tabTitle to title of t
                    set tabURL to URL of t
                    set tabList to tabList & tabTitle & "|||" & tabURL & "\\n"
                end repeat
            end repeat
            return tabList
        end tell
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            tabs = []
            for line in result.stdout.strip().split('\n'):
                if '|||' in line:
                    parts = line.split('|||', 1)
                    if len(parts) == 2:
                        tabs.append({
                            'title': parts[0].strip(),
                            'url': parts[1].strip()
                        })
            return tabs
        
        return []
    except Exception as e:
        print(f"Error getting Chrome tabs: {e}")
        return []

# Example usage
if __name__ == "__main__":
    tabs = get_chrome_tabs()
    print(tabs)  # Returns list of dictionaries
