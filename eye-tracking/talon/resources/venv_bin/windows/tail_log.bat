@echo off
set /p python=<"%~dp0\.python"
set /p resources=<"%~dp0\.resources"
start cmd /c ""%python%"\python.exe "%resources%\tail.py" "-q" "DEBUG Talon Version:" "%~dp0\..\..\talon.log""
