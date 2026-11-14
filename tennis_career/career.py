import matplotlib.pyplot as plt
import pandas as pd
import re
import requests
import unicodedata
import json

base_url = "https://www.tennisabstract.com"
match_array = re.compile(r"\bvar\s+morematchmx\s*=\s*(?=\[)")
birth_date = re.compile(r"\b\d{1,2}[- ]+[A-Za-z]{3,9}[- ]+\d{4}\b")

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

def parse_birth_date(html):
    for match in birth_date.finditer(html):
        date = pd.to_datetime(match.group(), dayfirst=True, errors="coerce")
        if pd.notna(date):
            return date
    return pd.NaT

def find_birth_date(slug):
    for page in ("wplayer-classic.cgi", "player-classic.cgi"):
        url = f"{base_url}/cgi-bin/{page}?p={slug}&f=ACareerqq"
        birth_date = parse_birth_date(download(url) or "")
        if pd.notna(birth_date):
            return birth_date
    raise ValueError(f"Could not find a birth date for {slug}.")

def clean_matches(rows, player_birth_date):
    columns = ["match_date", "tournament", "surface", "result", "opponent", "age_value"]
    records = [
        (row[0], row[1], row[2], row[4], row[11], row[16])
        for row in rows if len(row) > 16
    ]
    matches = pd.DataFrame(records, columns=columns)
    dates = pd.to_datetime(matches["match_date"], format="%Y%m%d", errors="coerce")
    age_values = matches.pop("age_value").astype("string").str.strip()
    is_birth_date = age_values.str.fullmatch(r"\d{8}", na=False)
    opponent_birth_dates = pd.to_datetime(
        age_values.where(is_birth_date), format="%Y%m%d", errors="coerce"
    )
    calculated_ages = (dates - opponent_birth_dates).dt.days / 365.25
    reported_ages = pd.to_numeric(age_values.where(~is_birth_date), errors="coerce")
    matches["match_date"] = dates
    matches["player_age"] = (dates - player_birth_date).dt.days / 365.25
    matches["opponent_age"] = reported_ages.where(~is_birth_date, calculated_ages)
    matches["age_difference"] = matches["player_age"] - matches["opponent_age"]
    valid = matches["result"].isin(["W", "L"]) & matches["age_difference"].notna()
    return matches.loc[valid].sort_values("match_date").reset_index(drop=True)

def career_matches(player_name):
    slug = player_input(player_name)
    js = download(f"{base_url}/jsmatches/{slug}Career.js")
    if not js or not match_array.search(js):
        raise ValueError(f"No Tennis Abstract career data found for {player_name!r}.")
    rows = parse_match_rows(js)
    birth_date = find_birth_date(slug)
    matches = clean_matches(rows, birth_date)
    if matches.empty:
        raise ValueError(f"No matches with usable age data for {player_name!r}.")
    return matches

def plot_career_matches(matches):
    _, ax = plt.subplots()

    for result, label in [("W", "Win"), ("L", "Loss")]:
        group = matches[matches["result"] == result]
        ax.scatter(group["player_age"], group["age_difference"], label=label)
    ax.set_xlabel("Player age (years)")
    ax.set_ylabel("Player age − opponent age (years)")
    ax.legend()
    return ax