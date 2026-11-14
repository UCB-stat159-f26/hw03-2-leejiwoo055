# Tennis Career Package
## Introduction

For HW 3, I created a Python package that downloads career match data from [Tennis Abstract](https://www.tennisabstract.com/), determines the player’s and opponent’s ages at each match, and plots the age difference against the player’s age. The scatter plot uses different colors for wins and losses.

## Installation

From the repository root, run:

```bash
python -m pip install .
```

## Usage

```python
import matplotlib.pyplot as plt

from tennis_career import career_matches, plot_career_matches

matches = career_matches("Serena Williams")
print(matches.head())

plot_career_matches(matches)
plt.show()
```

The horizontal axis shows the player's age at each match. The vertical axis
shows the player's age minus the opponent's age, so a positive value means
the player was older. Wins and losses appear in different colors.

## Tests

From the repository root, run:

```bash
python -m pip install ".[test]"
python -m pytest -q
```

The tests use the homework's Serena Williams and Rafael Nadal JavaScript
samples in `tests/data/`. They check both opponent-age formats without
contacting Tennis Abstract.

## Reflection

I learned how to turn a Python script into an installable package. One challenge
was that Serena's sample stores opponents' birth dates, while Nadal's sample
stores their ages directly. Testing both formats with local sample files gave me
a way to check the age calculations without depending on a live website.