# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important

Never read the contents of any CSV files in `data/` or `output/`. Treat their schemas (column names) as known from this file.

## Running the Script

```bat
run_food_schedule.bat
```

Or directly via Python (requires `myenv` conda environment):

```powershell
conda activate myenv
python main.py --start_date 2026-01-20 --num_days 120 --not_lunch_days 24
```

Install dependencies: `pip install -r requirements.txt`

## Project Structure

```
food-generator/
├── data/                        ← list.csv, lunch_list.csv (input, not committed)
├── output/                      ← food_schedule.csv (generated, not committed)
├── food_generator/
│   ├── scheduler.py             ← pure schedule logic, no I/O
│   └── cli.py                   ← argparse, file I/O, entry point logic
├── main.py                      ← thin entry point
└── run_food_schedule.bat        ← calls main.py via conda myenv
```

## Architecture

**Input files** (`data/`): `list.csv` (dinner — columns: `Food`, `Subtype`, `Subtype2`) and `lunch_list.csv` (lunch — columns: `Food`, `Subtype`).

**Output** (`output/food_schedule.csv`): merged lunch + dinner rows with columns `Date`, `Meal`, `Remarks`.

## Key Logic

**`not_lunch_days` parameter** — a digit string (e.g., `"24"`) where each digit is a weekday number (Mon=0…Sun=6). `weekdays_from_number()` inverts this: the digits become *excluded* weekdays; the complement becomes valid dinner days. So `"24"` means Tue+Thu are dinner days, and all other days get lunch.

**Subtype expansion** (`_expand_foods` in `scheduler.py`) — Foods with comma-separated `Subtype`/`Subtype2` columns expand into individual variants (e.g., `Pasta_Carbonara_Cream`). Each parent food gets equal base probability; subtypes split that equally.

**Remarks column** (`cli.py:_get_remarks`) — Friday → `"ใส่ 2 กล่องก่อน 7.30PM"`, Wednesday → `"ใส่ 1 กล่องก่อน 7.30PM"`.
