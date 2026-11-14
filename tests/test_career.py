from pathlib import Path
import pandas as pd
import pytest
from tennis_career import career

data = Path(__file__).parent / "data"

@pytest.mark.parametrize(
    "filename, birth_date, opponent, expected_age",
    [
        ("SerenaWilliamsCareer.js", "1981-09-26", "Anne Miller", 18.78),
        ("RafaelNadalCareer.js", "1986-06-03", "Israel Matos Gil", 18.7597535934),
    ],
)
def test_clean_career_matches(filename, birth_date, opponent, expected_age):
    js = (data / filename).read_text(encoding="utf-8")
    rows = career.parse_match_rows(js)
    matches = career.clean_matches(rows, pd.Timestamp(birth_date))
    
    assert len(matches) == 3

    match = matches.loc[matches["opponent"] == opponent].iloc[0]
    expected_difference = match["player_age"] - expected_age

    assert match["opponent_age"] == pytest.approx(expected_age, abs=0.01)
    assert match["age_difference"] == pytest.approx(expected_difference, abs=0.01)