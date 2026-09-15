@echo off
setlocal
cd /d "%~dp0"
start "" "%~dp0..\pythonw.exe" "%~dp0activation_import.py" %*
