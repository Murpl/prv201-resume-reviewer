@echo off
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe app.py
) else (
  python -c "import pypdf" >nul 2>&1
  if errorlevel 1 (
    echo First run: follow the setup commands in README.md.
  ) else (
    python app.py
  )
)
pause
