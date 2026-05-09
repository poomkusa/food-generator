# Food Generator

Generates a randomized meal schedule (lunch + dinner) over a given date range, based on weighted food lists.

## Usage

```bat
run_food_schedule.bat
```

Or directly:

```powershell
conda activate myenv
python main.py --start_date 2026-01-20 --num_days 120 --not_lunch_days 24
```

| Argument | Description | Default |
|---|---|---|
| `--start_date` | Start date (`YYYY-MM-DD`) | `2025-08-11` |
| `--num_days` | Number of days to schedule | `110` |
| `--not_lunch_days` | Digit string of weekdays (Mon=0…Sun=6) that get dinner instead of lunch | `24` |

## Setup

```powershell
pip install -r requirements.txt
```

Place input files in `data/`:
- `list.csv` — dinner foods (`Food`, `Subtype`, `Subtype2`)
- `lunch_list.csv` — lunch foods (`Food`, `Subtype`)

Output is written to `output/food_schedule.csv` with columns `Date`, `Meal`, `Remarks`.

## How It Works

- Each food item gets equal base probability. Comma-separated subtypes split that probability equally (e.g. a food with 2 subtypes and 3 subtype2s expands into 6 variants).
- `not_lunch_days` controls which weekdays get dinner vs lunch. For example `"24"` means Tuesday (2) and Thursday (4) get dinner; all other days get lunch.
- Friday and Wednesday get Thai-language packing remarks in the `Remarks` column.
