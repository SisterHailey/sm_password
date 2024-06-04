@echo off
start "" /B "pythonw.exe" "smpwd.pyw"
if %errorlevel% neq 0 (
    echo An error occurred. The script did not execute successfully.
    echo Do you have Python installed?
    pause
)
exit