@echo off
set /p python=<"%~dp0\.python"
set /p resources=<"%~dp0\.resources"
if "%~1" == "--window" (
    start cmd /c ""%python%"\python.exe "%resources%\repl.py" & pause"
) else (
    cmd /c ""%python%"\python.exe "%resources%\repl.py""
)
