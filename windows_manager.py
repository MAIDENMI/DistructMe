import time
import uuid
import random
import tkinter as tk
from typing import Any, Callable, Dict, Optional, Tuple


class WindowsManager:
    """Tracks distraction windows and provides helpers for placement and cleanup."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.open_windows: Dict[str, Dict[str, Any]] = {}

    def get_screen_size(self) -> Tuple[int, int]:
        self.root.update_idletasks()
        return self.root.winfo_screenwidth(), self.root.winfo_screenheight()

    def _generate_window_id(self) -> str:
        return str(uuid.uuid4())

    def create_window(
        self,
        title: str,
        width: int = 320,
        height: int = 200,
        x: Optional[int] = None,
        y: Optional[int] = None,
        topmost: bool = True,
        window_type: str = "generic",
        on_close: Optional[Callable[[str], None]] = None,
        resizable: bool = True,
    ) -> Tuple[str, tk.Toplevel]:
        """Create and register a new Toplevel window with optional placement and close hook."""
        window = tk.Toplevel(self.root)
        window_id = self._generate_window_id()

        window.title(title)
        if not resizable:
            window.resizable(False, False)
        if topmost:
            window.attributes("-topmost", True)

        screen_w, screen_h = self.get_screen_size()
        if x is None or y is None:
            x = random.randint(0, max(0, screen_w - width))
            y = random.randint(0, max(0, screen_h - height - 40))
        window.geometry(f"{width}x{height}+{x}+{y}")

        meta = {
            "id": window_id,
            "type": window_type,
            "position": (x, y),
            "size": (width, height),
            "created_at": time.time(),
            "z_index": len(self.open_windows) + 1,
        }
        self.open_windows[window_id] = {"window": window, "meta": meta}

        def _handle_close() -> None:
            try:
                if on_close is not None:
                    on_close(window_id)
            finally:
                # Ensure removal even if callback fails
                self.unregister_window(window_id)
                try:
                    window.destroy()
                except Exception:
                    pass

        window.protocol("WM_DELETE_WINDOW", _handle_close)
        return window_id, window

    def unregister_window(self, window_id: str) -> None:
        if window_id in self.open_windows:
            del self.open_windows[window_id]

    def close_all(self) -> None:
        # Copy keys to avoid modification during iteration
        for window_id in list(self.open_windows.keys()):
            window = self.open_windows[window_id]["window"]
            try:
                window.destroy()
            except Exception:
                pass
        self.open_windows.clear()

    def reposition_window(self, window_id: str, x: int, y: int) -> None:
        entry = self.open_windows.get(window_id)
        if not entry:
            return
        window = entry["window"]
        width, height = entry["meta"]["size"]
        window.geometry(f"{width}x{height}+{x}+{y}")
        entry["meta"]["position"] = (x, y)

    def bring_to_front(self, window_id: str) -> None:
        entry = self.open_windows.get(window_id)
        if not entry:
            return
        window = entry["window"]
        window.lift()
        window.attributes("-topmost", True)

    def get_open_windows(self) -> Dict[str, Dict[str, Any]]:
        # Return a shallow copy to avoid accidental external mutation
        return dict(self.open_windows)
