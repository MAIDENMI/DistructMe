import random
import webbrowser

MEDIA_LINKS = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=j5-yKhDd64s",
    "https://www.youtube.com/watch?v=oHg5SJYRHA0",
    "https://www.twitch.tv/directory",
]


def open_random_media() -> None:
    link = random.choice(MEDIA_LINKS)
    webbrowser.open(link)
