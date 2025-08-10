import pandas as pd
import numpy as np
import os
import argparse
from datetime import timedelta

# # Function to generate the food schedule and probabilities
# def generate_food_schedule(num_days, start_date, food_df):
#     # Calculate probabilities with subtype allocation
#     unique_foods = []
#     probabilities = []

#     for _, row in food_df.iterrows():
#         food = row['Food']
#         subtype = row['Subtype']
#         subtype2 = row['Subtype2']

#         # If there's no subtype, add the food with equal probability
#         if pd.isna(subtype) or subtype == "":
#             unique_foods.append(food)
#             probabilities.append(1 / len(food_df))
#         else:
                        
#             # Split subtypes and subtype2, allocating probabilities
#             subtypes = subtype.split(',')
            
#             for stype in subtypes:
#                 if pd.isna(subtype2) or subtype2 == "":
#                     # If no subtype2, allocate probability only for subtype
#                     unique_foods.append(f"{food}_{stype.strip()}")
#                     probabilities.append((1 / len(food_df)) / len(subtypes))
#                 else:
#                     # Allocate probabilities for both subtype and subtype2
#                     subtype2_list = subtype2.split(',')
#                     prob_per_subtype2 = (1 / len(food_df)) / (len(subtypes) * len(subtype2_list))
                    
#                     for stype2 in subtype2_list:
#                         unique_foods.append(f"{food}_{stype.strip()}_{stype2.strip()}")
#                         probabilities.append(prob_per_subtype2)
    
#     # Normalize probabilities to ensure they sum to 1
#     total_probability = sum(probabilities)
#     probabilities = [p / total_probability for p in probabilities]

#     # Generate the list of dates
#     dates = [pd.to_datetime(start_date) + timedelta(days=i) for i in range(num_days)]

#     # Randomly assign a food item to each date based on probabilities
#     chosen_foods = np.random.choice(unique_foods, size=num_days, p=probabilities)
#     food_schedule = pd.DataFrame({'Date': dates, 'Dinner': chosen_foods})

#     # Remove time from date column
#     food_schedule['Date'] = food_schedule['Date'].dt.date

#     # Probability DataFrame for review
#     prob_df = pd.DataFrame({'Food': unique_foods, 'Probability': probabilities})

#     return food_schedule, prob_df

def generate_food_schedule(num_days, start_date, food_df):
    # Calculate probabilities with subtype allocation
    unique_foods = []
    probabilities = []

    for _, row in food_df.iterrows():
        food = row['Food']
        subtype = row['Subtype']
        subtype2 = row['Subtype2']

        if pd.isna(subtype) or subtype == "":
            unique_foods.append(food)
            probabilities.append(1 / len(food_df))
        else:
            subtypes = subtype.split(',')
            for stype in subtypes:
                if pd.isna(subtype2) or subtype2 == "":
                    unique_foods.append(f"{food}_{stype.strip()}")
                    probabilities.append((1 / len(food_df)) / len(subtypes))
                else:
                    subtype2_list = subtype2.split(',')
                    prob_per_subtype2 = (1 / len(food_df)) / (len(subtypes) * len(subtype2_list))
                    for stype2 in subtype2_list:
                        unique_foods.append(f"{food}_{stype.strip()}_{stype2.strip()}")
                        probabilities.append(prob_per_subtype2)

    # Normalize probabilities
    total_probability = sum(probabilities)
    probabilities = [p / total_probability for p in probabilities]

    # Generate list of dates and filter to Tue(1), Wed(2), Fri(4), Sun(6)
    all_dates = [pd.to_datetime(start_date) + timedelta(days=i) for i in range(num_days * 2)]
    dates = [d for d in all_dates if d.weekday() in [1, 2, 4, 6]][:num_days]

    # Randomly assign foods based on probabilities
    chosen_foods = np.random.choice(unique_foods, size=len(dates), p=probabilities)
    food_schedule = pd.DataFrame({'Date': dates, 'Dinner': chosen_foods})
    food_schedule['Date'] = food_schedule['Date'].dt.date  # remove time

    # Probability DataFrame
    prob_df = pd.DataFrame({'Food': unique_foods, 'Probability': probabilities})

    return food_schedule, prob_df


# # Function to generate the food schedule and probabilities
# def generate_lunch_schedule(num_days, start_date, food_df):
#     # Calculate probabilities with subtype allocation
#     unique_foods = []
#     probabilities = []

#     for _, row in food_df.iterrows():
#         food = row['Food']
#         subtype = row['Subtype']

#         # If there's no subtype, add the food with equal probability
#         if pd.isna(subtype) or subtype == "":
#             unique_foods.append(food)
#             probabilities.append(1 / len(food_df))
#         else:
#             # Get all subtypes (comma-separated) and divide probability equally among them
#             subtypes = subtype.split(',')
#             prob_per_subtype = (1 / len(food_df)) / len(subtypes)
            
#             for stype in subtypes:
#                 unique_foods.append(f"{food}_{stype.strip()}")
#                 probabilities.append(prob_per_subtype)
    
#     # Normalize probabilities to ensure they sum to 1
#     total_probability = sum(probabilities)
#     probabilities = [p / total_probability for p in probabilities]

#     # Generate the list of dates (only weekdays + last Saturday of the month)
#     dates = []
#     current_date = pd.to_datetime(start_date)
#     for _ in range(num_days):
#         if current_date.weekday() < 5:  # Weekday check (0-4 are Mon-Fri)
#             dates.append(current_date)
#         elif current_date.weekday() == 5 and is_last_saturday(current_date):  # Last Saturday check
#             dates.append(current_date)
#         current_date += timedelta(days=1)

#     # Randomly assign a food item to each selected date based on probabilities
#     chosen_foods = np.random.choice(unique_foods, size=len(dates), p=probabilities)
#     food_schedule = pd.DataFrame({'Date': dates, 'Lunch': chosen_foods})

#     # Remove time from date column
#     food_schedule['Date'] = food_schedule['Date'].dt.date

#     return food_schedule

def generate_lunch_schedule(num_days, start_date, food_df):
    # Calculate probabilities with subtype allocation
    unique_foods = []
    probabilities = []

    for _, row in food_df.iterrows():
        food = row['Food']
        subtype = row['Subtype']

        if pd.isna(subtype) or subtype == "":
            unique_foods.append(food)
            probabilities.append(1 / len(food_df))
        else:
            subtypes = subtype.split(',')
            prob_per_subtype = (1 / len(food_df)) / len(subtypes)
            for stype in subtypes:
                unique_foods.append(f"{food}_{stype.strip()}")
                probabilities.append(prob_per_subtype)

    # Normalize probabilities
    total_probability = sum(probabilities)
    probabilities = [p / total_probability for p in probabilities]

    # Generate dates excluding Tue(1), Wed(2), Fri(4), Sun(6)
    dates = []
    current_date = pd.to_datetime(start_date)
    for _ in range(num_days):
        if current_date.weekday() not in [1, 2, 4, 6]:
            dates.append(current_date)
        current_date += timedelta(days=1)

    # Randomly assign food
    chosen_foods = np.random.choice(unique_foods, size=len(dates), p=probabilities)
    food_schedule = pd.DataFrame({'Date': dates, 'Lunch': chosen_foods})
    food_schedule['Date'] = food_schedule['Date'].dt.date

    return food_schedule

# Helper function to check if a date is the last Saturday of the month
def is_last_saturday(date):
    last_day_of_month = (date + pd.offsets.MonthEnd(0)).date()  # Convert to date
    return date.weekday() == 5 and (date + timedelta(days=7)).date() > last_day_of_month  # Convert to date for comparison

# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate food schedule based on input parameters.')
    parser.add_argument('--start_date', type=str, help='Start date in YYYY-MM-DD format.', default='2025-08-11')
    parser.add_argument('--num_days', type=int, help='Number of days for the schedule.', default=110)
    return parser.parse_args()

# Main function to run the script
def main():
    # Parse the arguments from the command line
    args = parse_arguments()
    start_date = args.start_date
    num_days = args.num_days

    # Dynamic file paths based on the script's location
    # Check if running as a script or interactively
    if '__file__' in globals():
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    else:
        script_dir = os.getcwd()  # Use the current working directory in interactive environments
    file_path = os.path.join(script_dir, "list.csv")  # Use list.csv instead of list.xlsx

    # Read the CSV file with UTF-8 encoding
    food_df = pd.read_csv(file_path, encoding='utf-8-sig')



    
    # Dynamic file paths based on the script's location
    file_path = os.path.join(script_dir, "lunch_list.csv")  # Use list.csv instead of list.xlsx

    # Read the CSV file with UTF-8 encoding
    lunch_df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    
        
    
    # Generate the food schedule and probability dataframes
    food_schedule, prob_df = generate_food_schedule(num_days, start_date, food_df)

    # Generate the food schedule and probability dataframes
    lunch_schedule = generate_lunch_schedule(num_days, start_date, lunch_df)




    # # Outer join by Date key
    # food_schedule = pd.merge(lunch_schedule, food_schedule, on='Date', how='outer').sort_values(by='Date')
    # Rename to match "Meal"
    lunch_df = lunch_schedule.rename(columns={"Lunch": "Meal"})
    food_df = food_schedule.rename(columns={"Dinner": "Meal"})
    # Concatenate vertically
    food_schedule = pd.concat([lunch_df, food_df], ignore_index=True)
    # Sort by Date
    # Add Remarks column based on weekday
    def get_remarks(date):
        wd = pd.to_datetime(date).weekday()  # Mon=0 ... Sun=6
        if wd in [0, 5]:  # Monday or Saturday
            return "ใส่ 2 กล่องก่อน 12.30PM"
        elif wd == 3:  # Thursday
            return "ใส่ 1 กล่องก่อน 4.30PM"
        else:
            return ""
    
    food_schedule["Remarks"] = food_schedule["Date"].apply(get_remarks)    
    food_schedule = food_schedule.sort_values("Date").reset_index(drop=True)
        
    
    # Save the food schedule to a CSV file in the same directory with UTF-8 encoding
    output_path = os.path.join(script_dir, "food_schedule.csv")
    food_schedule.to_csv(output_path, index=False, encoding='utf-8-sig')

    # Print the output file path for confirmation
    print(f"Food schedule saved to {output_path}")
    print("Generated Food Schedule:")
    print(food_schedule)
    print("Food Probabilities:")
    print(prob_df)

if __name__ == "__main__":
    main()
