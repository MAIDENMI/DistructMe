import subprocess
import sys

def show_ngmi_popup():
    """Display a popup window with 'ngmi' message using macOS native dialog"""
    try:
        # Use AppleScript to show a native macOS dialog
        applescript = '''
        display dialog "ngmi" with title "NGMI" buttons {"OK"} default button "OK" giving up after 0
        '''
        subprocess.run(['osascript', '-e', applescript], check=True)
    except subprocess.CalledProcessError:
        # do nothing
        pass

if __name__ == "__main__":
    show_ngmi_popup()