import tkinter as tk
from tkinter import scrolledtext
from typing import Optional

from windows_manager import WindowsManager


def open_ngmi_editor(
    manager: WindowsManager,
    refresh_interval_ms: int = 3000,
    editable: bool = True,
) -> None:
    """Open a small editor window that periodically resets to 'NGMI'."""
    window_id, win = manager.create_window(
        title="NGMI",
        width=360,
        height=220,
        window_type="ngmi_editor",
        topmost=True,
        resizable=True,
    )

    label = tk.Label(win, text="You are NGMI", font=("Helvetica", 14, "bold"))
    label.pack(pady=6)

    text = scrolledtext.ScrolledText(win, wrap=tk.WORD, height=6)
    text.pack(expand=True, fill=tk.BOTH, padx=8, pady=6)

    def reset_content() -> None:
        current = text.get("1.0", tk.END).strip()
        # Keep some user text but reinforce NGMI occasionally
        base = "NGMI\n\n" if len(current) == 0 or len(current) > 240 else ""
        text.delete("1.0", tk.END)
        text.insert("1.0", base + "NGMI")
        win.after(refresh_interval_ms, reset_content)

    if not editable:
        text.configure(state=tk.DISABLED)

    # Seed initial content
    text.insert("1.0", "NGMI")
    win.after(refresh_interval_ms, reset_content)

    # Auto-focus the text field to distract typing
    try:
        text.focus_set()
    except Exception:
        pass
