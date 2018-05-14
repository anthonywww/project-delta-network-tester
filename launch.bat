@echo off

REM Set the current directory to the script directory
cd /D %~dp0

REM Execute the client
python3 src/client.py

echo ^> Press [ENTER] to quit.
pause>nul
