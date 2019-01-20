@echo off
title qt-json-view

rem
rem  To run this at startup, use this as your shortcut target:
rem  %windir%\system32\cmd.exe /k c:\path\to\project\shell.bat
rem


rem Startup bat
set startup="%appdata%\Microsoft\Windows\Start Menu\Programs\Startup\startup.bat"
pushd .
if exist %startup% ( call %startup% )
popd

rem Pack env
if exist packFile.bat ( call packFile.bat )

rem Activate conda env
call activate python27

rem Aliases
if exist ".\aliases.cmd" ( call ".\aliases.cmd" )

rem Qt.py preferred Qt binding
set QT_PREFERRED_BINDING=PyQt5

