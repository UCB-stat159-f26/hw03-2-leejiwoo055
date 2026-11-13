import re
import unicodedata


def player_input(player_name):
    name = unicodedata.normalize("NFKD", player_name)
    name = name.encode("ascii", "ignore").decode()
    words = re.findall(r"[A-Za-z]+", name)
    if not words:
        raise ValueError("Enter a player name")
    return "".join(word[0].upper() + word[1:] for word in words)