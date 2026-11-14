# Tennis Career Package

## Introduction

For HW 3, I created a Python package that downloads career match data from [Tennis Abstract](https://www.tennisabstract.com/), determines the player’s and opponent’s ages at each match, and plots the age difference against the player’s age. The scatter plot uses different colors for wins and losses.

## File Structure
| Path | Purpose |
|---|---|
| `setup.py` | Defines how to install the package and lists its dependencies. |
| `tennis_career/__init__.py` | Exposes `career_matches()` and `plot_career_matches()`. |
| `tennis_career/career.py` | Downloads and cleans match data, calculates ages, and creates the scatter plot. |
| `tests/test_career.py` | Tests both opponent-age formats using local JavaScript files. |
| `tests/data/` | Contains the Serena Williams and Rafael Nadal career data used by the tests. |
| `.gitignore` | Lists generated files and folders that Git should ignore. |

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

For Hw 3, I learned how to turn a Python script into an installable package. I also learned how setup.py declares the package’s dependencies so someone else can install it and use the same functions. I used __init__.py to make the two main functions available directly from tennis_career. Writing the installation and usage steps helped me think through what a new user would do after cloning the repository.
One challenge was that Serena's sample stores opponents' birth dates, while Nadal's sample stores their ages directly, which two files gave me different information about the opponent. So I tested both formats to make sure my code produced an opponent age in years before calculating the age difference.

