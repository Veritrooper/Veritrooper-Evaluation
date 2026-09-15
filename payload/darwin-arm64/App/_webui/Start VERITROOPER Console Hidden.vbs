Option Explicit

' Launch the existing diagnostic-friendly batch file without showing a command window.
' The batch file still owns readiness polling, browser opening, and log/error handling.
Dim shell, scriptFolder, launcher, command
Set shell = CreateObject("WScript.Shell")
scriptFolder = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
launcher = scriptFolder & "Start VERITROOPER Console.bat"
command = Chr(34) & launcher & Chr(34)
shell.Run command, 0, False
