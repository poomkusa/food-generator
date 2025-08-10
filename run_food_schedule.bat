@echo off
:: Define parameters (remove inline comments to avoid errors)
set "START_DATE=2025-01-03"
set "NUM_DAYS=365"

:: Get the directory of the current script
set "SCRIPT_DIR=%~dp0"

:: Run the Python script with the parameters
python "%SCRIPT_DIR%generate_food_schedule.py" --start_date "%START_DATE%" --num_days "%NUM_DAYS%"

pause