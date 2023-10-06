@echo off
SETLOCAL
SET install="%USERPROFILE%\AppData\Local\Programs\boundbuilder"
mkdir %install%
copy base_config.yaml %install%
venv\Scripts\python.exe venv\Scripts\pyinstaller.exe --onefile --distpath %install% --collect-data pikepdf --copy-metadata pikepdf boundbuilder.py
ENDLOCAL
