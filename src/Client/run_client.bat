@echo off
set "exe_path=App\Client.exe"

if exist "%exe_path%" (
    start "" "%exe_path%"
) else (
    echo Il file "%exe_path%" non esiste.
    pause
)
