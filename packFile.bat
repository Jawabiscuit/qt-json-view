@echo off

rem Executables
set PATH=%cd%\bin;%PATH%

rem Python paths
set paths=%cd%;%cd%\vendor\Qt.py
if not defined PYTHONPATH (
    set PYTHONPATH=%paths%
) else (
    set PYTHONPATH=%paths%;%PYTHONPATH%
)

