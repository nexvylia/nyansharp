@echo off
rem Lanzador de nyac para Windows (CMD y PowerShell).
rem Usa el lanzador "py" si existe; si no, "python".
where py >nul 2>&1
if %errorlevel%==0 (
  py -3 "%~dp0nyac.py" %*
) else (
  python "%~dp0nyac.py" %*
)
exit /b %errorlevel%
