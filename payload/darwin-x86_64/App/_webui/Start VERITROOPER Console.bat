@echo off
setlocal enabledelayedexpansion
title VERITROOPER Console

REM ===========================================================================
REM  Starts the VERITROOPER browser console and opens it.
REM
REM  This is the SHIPPED launcher - it lives inside the installed package, not on
REM  a developer's desktop, so it must not assume anything about the machine:
REM  no Python on PATH, no source tree, no D: drive. Everything is resolved
REM  relative to this file.
REM
REM  Layout it expects (which is what the installer produces):
REM      <app>\Console\Engine\python.exe        the bundled interpreter
REM      <app>\Console\Engine\_webui\server.py  this console
REM
REM  KEEP THIS FILE PLAIN ASCII. cmd.exe reads it in the system code page, and a
REM  smart quote or an em-dash becomes a stray command. That has bitten before.
REM ===========================================================================

set "WEBUI=%~dp0"
set "ENGINE=%WEBUI%.."
set "PORT=8300"
REM Keep the installed application tree immutable.  Runtime bytecode caches are
REM unnecessary in this bundled build and otherwise leave product files behind
REM after a normal uninstall.
set "PYTHONDONTWRITEBYTECODE=1"

REM --- already running? Then just open it. Starting a second one is not an
REM     error the user should have to understand - the first one is what they
REM     wanted. (The server itself also refuses the port now, but saying
REM     "already running" here is friendlier than a log file.)
netstat -ano | findstr /r /c:":%PORT% .*LISTENING" >nul 2>&1
if not errorlevel 1 (
  echo.
  echo   The console is already running.
  start "" "http://127.0.0.1:%PORT%"
  timeout /t 2 >nul
  exit /b 0
)

REM --- find the interpreter. Bundled first: it is the one with the engine's
REM     dependencies in it. A machine Python is a fallback, not a preference.
set "PY="
if exist "%ENGINE%\pythonw.exe" set "PY=%ENGINE%\pythonw.exe"
if not defined PY if exist "%ENGINE%\python.exe" set "PY=%ENGINE%\python.exe"
if not defined PY where pythonw >nul 2>&1 && set "PY=pythonw"
if not defined PY where python  >nul 2>&1 && set "PY=python"
if not defined PY (
  echo.
  echo   Could not find Python.
  echo   Expected it at: %ENGINE%\python.exe
  echo   This usually means the installation is incomplete - reinstall, or
  echo   contact support with this message.
  echo.
  pause
  exit /b 1
)

REM --- a log, always. pythonw.exe has NO console, so without this a server that
REM     fails to start leaves the user with a window that flashes and nothing else.
set "LOGDIR=%ProgramData%\Veritrooper\logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%" >nul 2>&1
set "LOG=%LOGDIR%\console.log"

echo.
echo   Starting the VERITROOPER console...
start "" /b "%PY%" "%WEBUI%server.py" --port %PORT% --log "%LOG%"

REM --- wait for it to answer before opening a browser at it. Opening too early
REM     shows a connection-refused page, which reads as "the product is broken".
set "UP="
for /l %%I in (1,1,40) do (
  if not defined UP (
    netstat -ano | findstr /r /c:":%PORT% .*LISTENING" >nul 2>&1
    if not errorlevel 1 set "UP=1"
    if not defined UP ping -n 2 127.0.0.1 >nul
  )
)

if defined UP (
  start "" "http://127.0.0.1:%PORT%"
  echo   Open at: http://127.0.0.1:%PORT%
  timeout /t 3 >nul
) else (
  echo.
  echo   The console did not start. What went wrong is written here:
  echo       %LOG%
  echo.
  echo   The most common causes are another program already using port %PORT%,
  echo   or the installation being incomplete.
  echo.
  pause
)
endlocal
