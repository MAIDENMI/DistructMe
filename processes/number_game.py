import tkinter as tk
from typing import List, Tuple

from windows_manager import WindowsManager


class NumberGame:
    def __init__(self, manager: WindowsManager) -> None:
        self.manager = manager
        self.active_ids: List[str] = []
        self.mode = None

    def start(self) -> None:
        if self.active_ids:
            return  # already running
        self.mode = 6
        self._spawn_number_six()

    def _on_child_closed(self, window_id: str) -> None:
        if window_id in self.active_ids:
            self.active_ids.remove(window_id)
        if not self.active_ids:
            # All closed, switch to 7
            self._show_seven_window()

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
        tk.Label(win, text=title, font=("Helvetica", 12, "bold")).pack(pady=4)
        self.active_ids.append(child_id)

    def _spawn_number_six(self) -> None:
        sw, sh = self.manager.get_screen_size()
        # Define a grid and place rectangles to approximate a "6"
        grid_w = 7
        grid_h = 7
        cell_w = max(80, sw // (grid_w + 4))
        cell_h = max(60, sh // (grid_h + 6))
        start_x = cell_w
        start_y = cell_h

        coords: List[Tuple[int, int]] = []
        # Outer loop of "6"
        for x in range(1, 6):
            coords.append((x, 1))
        for y in range(1, 6):
            coords.append((1, y))
        for x in range(1, 6):
            coords.append((x, 5))
        # inner tail
        for y in range(3, 6):
            coords.append((4, y))
        for x in range(2, 5):
            coords.append((x, 3))

        # Deduplicate
        coords = sorted(set(coords))

        for gx, gy in coords:
            px = start_x + gx * cell_w
            py = start_y + gy * cell_h
            self._spawn_window("6", px, py, cell_w - 20, cell_h - 20)

    def _show_seven_window(self) -> None:
        # Single celebratory 7 window
        sw, sh = self.manager.get_screen_size()
        x = sw // 2 - 150
        y = sh // 2 - 100
        child_id, win = self.manager.create_window(
            title="7",
            width=300,
            height=200,
            x=x,
            y=y,
            window_type="number_game",
            topmost=True,
            resizable=False,
            on_close=lambda _id: None,
        )
        tk.Label(win, text="7", font=("Helvetica", 72, "bold")).pack(expand=True)
        self.active_ids = [child_id]
