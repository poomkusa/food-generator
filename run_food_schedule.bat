@echo off

:: Initialize Conda
call "%USERPROFILE%\miniconda3\Scripts\activate.bat"
:: Activate your environment
call conda activate myenv

:: Define parameters (remove inline comments to avoid errors)
set "START_DATE=2026-01-20"
set "NUM_DAYS=10"

:: Get the directory of the current script
set "SCRIPT_DIR=%~dp0"

:: Run the Python script with the parameters
python "%SCRIPT_DIR%main.py" --start_date "%START_DATE%" --num_days "%NUM_DAYS%" --not_lunch_days "24"

pause