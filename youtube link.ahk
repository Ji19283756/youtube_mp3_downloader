#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

+!d::
send, ^l
send, ^l
sleep 200
send, ^c
run, "PATH TO Python.exe" final_mp3_downloader.py
return
