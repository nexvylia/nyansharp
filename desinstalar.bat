@echo off
setlocal EnableExtensions
title Desinstalar NyanSharp
set "NYA=%~dp0"
if "%NYA:~-1%"=="\" set "NYA=%NYA:~0,-1%"

echo   Quitando "%NYA%" del PATH de tu usuario...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$d = $env:NYA; $k = Get-Item 'HKCU:\Environment';" ^
  "$p = [string]$k.GetValue('Path', '', 'DoNotExpandEnvironmentNames');" ^
  "$nuevo = @($p -split ';' | Where-Object { $_ -and ($_.TrimEnd('\') -ne $d) }) -join ';';" ^
  "Set-ItemProperty -Path 'HKCU:\Environment' -Name Path -Value $nuevo -Type ExpandString;" ^
  "[Environment]::SetEnvironmentVariable('NYANSHARP_HOME', $null, 'User')"

for %%E in (code codium cursor windsurf) do (
  where %%E >nul 2>&1 && call %%E --uninstall-extension nexvylia.nyansharp >nul 2>&1
)
echo   Hecho. Ya puedes borrar la carpeta del repositorio.
if /i not "%~1"=="/silencioso" pause
exit /b 0
