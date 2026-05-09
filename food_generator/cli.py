import argparse
import os

import pandas as pd

from .scheduler import (
    generate_food_schedule,
    generate_lunch_schedule,
    weekdays_from_number,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate food schedule.")
    parser.add_argument("--start_date", type=str, default="2025-08-11")
    parser.add_argument("--num_days", type=int, default=110)
    parser.add_argument("--not_lunch_days", type=str, default="24")
    return parser.parse_args()


def main():
    args = parse_arguments()
    not_lunch_days = weekdays_from_number(args.not_lunch_days)

    food_df = pd.read_csv(os.path.join(DATA_DIR, "list.csv"), encoding="utf-8-sig")
    lunch_df = pd.read_csv(os.path.join(DATA_DIR, "lunch_list.csv"), encoding="utf-8-sig")

    food_schedule, prob_df = generate_food_schedule(args.num_days, args.start_date, food_df, not_lunch_days)
    lunch_schedule = generate_lunch_schedule(args.num_days, args.start_date, lunch_df, not_lunch_days)

    lunch_rows = lunch_schedule.rename(columns={"Lunch": "Meal"})
    dinner_rows = food_schedule.rename(columns={"Dinner": "Meal"})
    combined = pd.concat([lunch_rows, dinner_rows], ignore_index=True)

    combined["Remarks"] = combined["Date"].apply(_get_remarks)
    combined = combined.sort_values("Date").reset_index(drop=True)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "food_schedule.csv")
    combined.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Food schedule saved to {output_path}")
    print(combined)
    print("\nFood Probabilities:")
    print(prob_df)


def _get_remarks(date):
    wd = pd.to_datetime(date).weekday()
    if wd == 4:   # Friday
        return "ใส่ 2 กล่องก่อน 7.30PM"
    elif wd == 2:  # Wednesday
        return "ใส่ 1 กล่องก่อน 7.30PM"
    return ""
