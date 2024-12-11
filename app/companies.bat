@echo off
REM Activate the virtual environment
call "C:\Users\user\Desktop\Repositories\Finance-Analytics\finenv\Scripts\activate.bat"

REM Run the watchdog script
python watch.py

REM Keep the command prompt open
pause
