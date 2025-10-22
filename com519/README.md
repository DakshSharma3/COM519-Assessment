poetry run pyinstaller --onefile src/com519/main.py

if you dont want the console to be outputted then use:

python -m poetry run pyinstaller --noconsole --onefile src/com519/main.py
