@echo off
set /p python=<"%~dp0\.python"
"%python%"\python.exe "-c" "import sys; sys.path.remove(''); import runpy; runpy._run_module_as_main('pip')" %*
