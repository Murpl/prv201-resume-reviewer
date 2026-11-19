@echo off
cd /d "%~dp0"
echo Open http://127.0.0.1:8765 in your browser after the server starts.
"C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1112-737-0_26.1112.737.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe" app.py
pause
