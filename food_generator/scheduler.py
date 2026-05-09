import pandas as pd
import numpy as np
from datetime import timedelta


def generate_food_schedule(num_days, start_date, food_df, not_lunch_days):
    unique_foods, probabilities = _expand_foods(food_df, has_subtype2=True)

    all_dates = [pd.to_datetime(start_date) + timedelta(days=i) for i in range(num_days * 2)]
    dates = [d for d in all_dates if d.weekday() in not_lunch_days][:num_days]

    chosen_foods = np.random.choice(unique_foods, size=len(dates), p=probabilities)
    food_schedule = pd.DataFrame({"Date": dates, "Dinner": chosen_foods})
    food_schedule["Date"] = food_schedule["Date"].dt.date

    prob_df = pd.DataFrame({"Food": unique_foods, "Probability": probabilities})
    return food_schedule, prob_df


def generate_lunch_schedule(num_days, start_date, food_df, not_lunch_days):
    unique_foods, probabilities = _expand_foods(food_df, has_subtype2=False)

    dates = []
    current_date = pd.to_datetime(start_date)
    for _ in range(num_days):
        if current_date.weekday() not in not_lunch_days:
            dates.append(current_date)
        current_date += timedelta(days=1)

    chosen_foods = np.random.choice(unique_foods, size=len(dates), p=probabilities)
    food_schedule = pd.DataFrame({"Date": dates, "Lunch": chosen_foods})
    food_schedule["Date"] = food_schedule["Date"].dt.date
    return food_schedule


def weekdays_from_number(n):
    """Return weekday indices NOT in the digit string n (Mon=0…Sun=6)."""
    all_days = set(range(7))
    excluded = set(int(d) for d in str(n))
    return sorted(all_days - excluded)


def is_last_saturday(date):
    last_day_of_month = (date + pd.offsets.MonthEnd(0)).date()
    return date.weekday() == 5 and (date + timedelta(days=7)).date() > last_day_of_month


def _expand_foods(food_df, has_subtype2=False):
    """Expand food rows with subtypes into individual variants with equal-split probabilities."""
    unique_foods = []
    probabilities = []

    for _, row in food_df.iterrows():
        food = row["Food"]
        subtype = row["Subtype"]
        subtype2 = row.get("Subtype2") if has_subtype2 else None

        if pd.isna(subtype) or subtype == "":
            unique_foods.append(food)
            probabilities.append(1 / len(food_df))
        else:
            subtypes = subtype.split(",")
            for stype in subtypes:
                if pd.isna(subtype2) or subtype2 == "" or not has_subtype2:
                    unique_foods.append(f"{food}_{stype.strip()}")
                    probabilities.append((1 / len(food_df)) / len(subtypes))
                else:
                    subtype2_list = subtype2.split(",")
                    prob = (1 / len(food_df)) / (len(subtypes) * len(subtype2_list))
                    for stype2 in subtype2_list:
                        unique_foods.append(f"{food}_{stype.strip()}_{stype2.strip()}")
                        probabilities.append(prob)

    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    return unique_foods, probabilities
