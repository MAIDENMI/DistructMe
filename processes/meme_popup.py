import io
import tkinter as tk
from typing import Callable, Optional

import requests
from PIL import Image, ImageTk

from windows_manager import WindowsManager


def open_meme_popup(
    manager: WindowsManager,
    image_url: str,
    on_click: Optional[Callable[[], None]] = None,
) -> None:
    """Open a popup displaying a GIF/image. Clicking triggers callback."""
    window_id, win = manager.create_window(
        title="Meme",
        width=600,
        height=500,
        window_type="meme_popup",
        topmost=True,
        resizable=True,
    )

    container = tk.Frame(win)
    container.pack(expand=True, fill=tk.BOTH)

    status = tk.Label(container, text="Loading meme…")
    status.pack(pady=8)

    image_label = tk.Label(container)
    image_label.pack(expand=True)

    frames = []
    durations = []

    def _play_frames(idx: int = 0) -> None:
        if not frames:
            return
        image_label.configure(image=frames[idx])
        next_idx = (idx + 1) % len(frames)
        delay = durations[idx] if 0 <= idx < len(durations) else 80
        win.after(delay, _play_frames, next_idx)

    def _load_image() -> None:
        try:
            # Check if it's a local file or URL
            if image_url.startswith(('http://', 'https://')):
                # Online URL
                resp = requests.get(image_url, timeout=8)
                resp.raise_for_status()
                data = io.BytesIO(resp.content)
                img = Image.open(data)
            else:
                # Local file
                img = Image.open(image_url)

            # Extract frames for GIFs
            try:
                while True:
                    frame = ImageTk.PhotoImage(img.copy())
                    frames.append(frame)
                    durations.append(img.info.get("duration", 80))
                    img.seek(len(frames))
            except EOFError:
                pass

            # Static image fallback
            if not frames:
                frames.append(ImageTk.PhotoImage(img))
                durations.append(200)

            # Auto-resize window to fit image
            img_width, img_height = img.size
            max_width, max_height = 800, 600
            if img_width > max_width or img_height > max_height:
                # Scale down if too large
                scale = min(max_width/img_width, max_height/img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                win.geometry(f"{new_width}x{new_height}")
            else:
                # Use image size if reasonable
                win.geometry(f"{img_width}x{img_height}")

            status.pack_forget()
            _play_frames(0)
        except Exception:
            status.configure(text="Couldn't load meme. You're still NGMI.")

    def _handle_click(_event=None) -> None:
        if on_click:
            try:
                on_click()
            except Exception:
                pass

    image_label.bind("<Button-1>", _handle_click)
    win.after(50, _load_image)
