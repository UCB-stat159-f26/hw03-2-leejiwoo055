import re
import requests
import unicodedata
import json


base_url = "https://www.tennisabstract.com"
match_array = re.compile(r"\bvar\s+morematchmx\s*=\s*(?=\[)")

def player_input(player_name):
    name = unicodedata.normalize("NFKD", player_name)
    name = name.encode("ascii", "ignore").decode()
    words = re.findall(r"[A-Za-z]+", name)
    if not words:
        raise ValueError("Enter a player name")
    return "".join(word[0].upper() + word[1:] for word in words)

def download(url):
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        raise RuntimeError(f"Could not download {url}") from error

def parse_match_rows(js):
    start = match_array.search(js).end()
    rows, _ = json.JSONDecoder().raw_decode(js[start:])
    return rows
