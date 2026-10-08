@echo off
setlocal EnableExtensions
title Instalador de NyanSharp
rem Uso: doble clic, o "instalar.bat /silencioso" (sin pausas, para pruebas).
set "SILENCIOSO="
if /i "%~1"=="/silencioso" set "SILENCIOSO=1"

echo.
echo   === NyanSharp - instalador para Windows (=^.^=) ===
echo.

rem --- Carpeta del repositorio (donde esta este .bat), sin la barra final ---
set "NYA=%~dp0"
if "%NYA:~-1%"=="\" set "NYA=%NYA:~0,-1%"

if not exist "%NYA%\nyac.py" (
  echo   [X] No encuentro nyac.py junto a este instalador.
  echo       Ejecuta instalar.bat desde la carpeta del repositorio clonado.
  goto :fallo
)
echo "%NYA%" | find /i "\AppData\Local\Temp\" >nul && (
  echo   [X] Estas ejecutando el instalador desde dentro de un ZIP o una carpeta temporal.
  echo       Clona el repositorio ^(o descomprime el ZIP^) en una carpeta fija y repite.
  goto :fallo
)

rem --- 1. Python 3 ---
set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY (
  python --version >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo   [X] Falta Python 3.
  echo       Instalalo con:  winget install Python.Python.3.12
  echo       o desde https://www.python.org/downloads/  marcando "Add python.exe to PATH".
  goto :fallo
)
for /f "delims=" %%V in ('%PY% --version 2^>^&1') do echo   [OK] %%V

rem --- 2. .NET SDK 8 ---
where dotnet >nul 2>&1 || (
  echo   [X] Falta el .NET SDK 8.
  echo       Instalalo con:  winget install Microsoft.DotNet.SDK.8
  echo       o desde https://dotnet.microsoft.com/download/dotnet/8.0  ^(el "SDK", no el "Runtime"^).
  goto :fallo
)
dotnet --list-sdks 2>nul | findstr /b /l "8." >nul || (
  echo   [X] Tienes dotnet, pero no el SDK 8. Versiones encontradas:
  dotnet --list-sdks
  echo       Instalalo con:  winget install Microsoft.DotNet.SDK.8
  goto :fallo
)
echo   [OK] .NET SDK 8

rem --- 3. Anadir la carpeta del repositorio al PATH del usuario ---
rem     Se hace con PowerShell: setx corta el PATH a 1024 caracteres.
echo   Anadiendo "%NYA%" al PATH de tu usuario...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$d = $env:NYA; $k = Get-Item 'HKCU:\Environment';" ^
  "$p = [string]$k.GetValue('Path', '', 'DoNotExpandEnvironmentNames');" ^
  "$partes = @($p -split ';' | Where-Object { $_ -and ($_.TrimEnd('\') -ne $d) });" ^
  "$nuevo = (@($partes) + $d) -join ';';" ^
  "Set-ItemProperty -Path 'HKCU:\Environment' -Name Path -Value $nuevo -Type ExpandString;" ^
  "[Environment]::SetEnvironmentVariable('NYANSHARP_HOME', $d, 'User')"
if errorlevel 1 (
  echo   [X] No pude modificar el PATH. Anade a mano esta carpeta al Path de tu usuario:
  echo       "%NYA%"
  goto :fallo
)
echo   [OK] PATH actualizado

rem --- 4. Extension de VS Code (y editores compatibles) ---
set "EXT=0"
for %%E in (code codium cursor windsurf) do (
  where %%E >nul 2>&1 && (
    echo   Instalando la extension en %%E...
    call %%E --install-extension "%NYA%\nyansharp-1.0.0.vsix" --force >nul 2>&1 && (
      echo   [OK] Extension instalada en %%E
      set "EXT=1"
    )
  )
)
if "%EXT%"=="0" (
  echo   [!] No encontre VS Code en el PATH. Instala la extension a mano:
  echo       VS Code ^> Extensiones ^> "..." ^> Install from VSIX ^> nyansharp-1.0.0.vsix
)

rem --- 5. Prueba rapida con el Python encontrado ---
%PY% "%NYA%\nyac.py" version >nul 2>&1 && echo   [OK] nyac responde

echo.
echo   Listo desu~
echo.
echo   IMPORTANTE: cierra TODAS las terminales y VS Code y vuelve a abrirlos
echo   ^(el PATH nuevo solo lo ven las ventanas que se abran despues^). Luego prueba:
echo.
echo       cd "%NYA%"
echo       nyac run ejemplos\hola.nya
echo.
if not defined SILENCIOSO (
  start "" "%NYA%\docs.html"
  pause
)
exit /b 0

:fallo
echo.
echo   No se ha instalado nada. Arregla lo anterior y vuelve a ejecutar instalar.bat.
if not defined SILENCIOSO pause
exit /b 1
