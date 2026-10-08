@echo off
pyinstaller --onefile --distpath . %~n0.py --add-data "Languages;Languages"
