@echo off
chcp 65001 >nul
title Instalador de NyanSharp
echo.
echo   === NyanSharp - instalador para Windows (=^.^=) ===
echo.

where python >nul 2>&1 || (
  echo   [X] Falta Python 3. Instalalo desde https://www.python.org/downloads/
  echo       IMPORTANTE: marca "Add python.exe to PATH" en el instalador.
  pause & exit /b 1
)
where dotnet >nul 2>&1 || (
  echo   [X] Falta .NET SDK 8. Instalalo desde https://dotnet.microsoft.com/download/dotnet/8.0
  echo       Descarga el "SDK" (no el Runtime).
  pause & exit /b 1
)
where code >nul 2>&1 || (
  echo   [!] No encuentro el comando "code" de VS Code.
  echo       Instala VS Code o abre VS Code, Ctrl+Shift+P, "Shell Command: Install 'code' command".
  echo       Seguire sin instalar la extension; puedes instalar el .vsix a mano luego.
)

set DEST=%LOCALAPPDATA%\NyanSharp
echo   Copiando a %DEST% ...
if not exist "%DEST%" mkdir "%DEST%"
xcopy /E /I /Y /Q "%~dp0*" "%DEST%\" >nul

echo   Anadiendo al PATH del usuario...
for /f "tokens=2*" %%A in ('reg query HKCU\Environment /v Path 2^>nul') do set "UPATH=%%B"
echo %UPATH% | find /I "%DEST%" >nul || setx Path "%UPATH%;%DEST%" >nul

where code >nul 2>&1 && (
  echo   Instalando extension de VS Code...
  call code --install-extension "%DEST%\nyansharp-1.0.0.vsix" --force >nul 2>&1
)

echo.
echo   Listo desu~  Cierra y abre de nuevo la terminal, y prueba:
echo.
echo       nyac run "%DEST%\ejemplos\hola.nya"
echo.
echo   Documentacion: %DEST%\docs.html   (se abre ahora)
start "" "%DEST%\docs.html"
pause
