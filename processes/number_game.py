import tkinter as tk
from typing import List, Tuple
import sys
import os

# Add parent directory to path to import windows_manager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from windows_manager import WindowsManager


class SmileyGame:
    def __init__(self, manager: WindowsManager) -> None:
        self.manager = manager
        self.active_ids: List[str] = []
        self.mode = None

    def start(self) -> None:
        if self.active_ids:
            return  # already running
        self.mode = "smiley"
        self._spawn_smiley_face()

    def _on_child_closed(self, window_id: str) -> None:
        if window_id in self.active_ids:
            self.active_ids.remove(window_id)
        # Don't do anything when windows are closed - just let them disappear

    def _spawn_window(self, title: str, x: int, y: int, w: int, h: int) -> None:
        child_id, win = self.manager.create_window(
            title=title,
            width=w,
            height=h,
            x=x,
            y=y,
            window_type="number_game",
            topmost=True,
            resizable=False,
            on_close=self._on_child_closed,
        )
        tk.Label(win, text=title, font=("Helvetica", 24, "bold")).pack(pady=8)
        self.active_ids.append(child_id)

    def _spawn_smiley_face(self) -> None:
        sw, sh = self.manager.get_screen_size()
        # Define a grid to create a smiley face
        grid_w = 9
        grid_h = 9
        # Make cells much larger - use about 60% of screen space
        cell_w = max(120, sw // (grid_w + 2))
        cell_h = max(100, sh // (grid_h + 2))
        start_x = sw // 2 - (grid_w * cell_w) // 2
        start_y = sh // 2 - (grid_h * cell_h) // 2

        coords: List[Tuple[int, int, str]] = []
        
        # Face outline (circle)
        face_coords = [
            (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
            (1, 2), (7, 2),
            (0, 3), (8, 3),
            (0, 4), (8, 4),
            (0, 5), (8, 5),
            (1, 6), (7, 6),
            (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)
        ]
        
        # Left eye
        left_eye = [ (3, 3)]
        
        # Right eye  
        right_eye = [(5, 3)]
        
        # Smile
        smile = [(2, 5), (3, 6), (4, 6), (5, 6), (6, 5)]
        
        # Add all coordinates with labels
        for x, y in face_coords:
            coords.append((x, y, "😊"))
        for x, y in left_eye:
            coords.append((x, y, "👁"))
        for x, y in right_eye:
            coords.append((x, y, "👁"))
        for x, y in smile:
            coords.append((x, y, "😄"))

        for gx, gy, emoji in coords:
            px = start_x + gx * cell_w
            py = start_y + gy * cell_h
            self._spawn_window(emoji, px, py, cell_w - 20, cell_h - 20)




if __name__ == "__main__":

    class DummyManager:
        def get_screen_size(self):
            root = tk.Tk()
            root.withdraw()
            sw = root.winfo_screenwidth()
            sh = root.winfo_screenheight()
            root.destroy()
            return sw, sh

        def create_window(self, title, width, height, x, y, window_type, topmost, resizable, on_close):
            win = tk.Toplevel()
            win.title(title)
            win.geometry(f"{width}x{height}+{x}+{y}")
            win.attributes("-topmost", topmost)
            win.resizable(resizable, resizable)
            win.protocol("WM_DELETE_WINDOW", lambda: (on_close(str(id(win))), win.destroy()))
            return str(id(win)), win

    root = tk.Tk()
    root.withdraw()  # Hide main window

    manager = DummyManager()
    game = SmileyGame(manager)
    game.start()

    tk.mainloop()