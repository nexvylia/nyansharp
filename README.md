# NyanSharp (.nya) · v1.0

[![pruebas](https://github.com/nexvylia/nyansharp/actions/workflows/pruebas.yml/badge.svg)](https://github.com/nexvylia/nyansharp/actions/workflows/pruebas.yml)

Un lenguaje de programación de broma pero que funciona de verdad: es C# 12 con
palabras kawaii de anime. El compilador `nyac` traduce el código `.nya` a C# y
lo compila con .NET 8. Todo lo de C# sigue valiendo: genéricos, LINQ, async,
records, pattern matching y paquetes NuGet.

```nya
onegai sekai nya

nakama Programa
{
    minna zutto nanimo hajimeru(kotoba[] args)
    {
        iu("Konnichiwa, sekai~!") nya
    }
}
```

---

## Índice

1. [Qué necesitas](#1-qué-necesitas)
2. [Instalar en Windows (paso a paso)](#2-instalar-en-windows-paso-a-paso)
3. [Instalar en Linux y macOS](#3-instalar-en-linux-y-macos)
4. [Instalar la extensión de VS Code](#4-instalar-la-extensión-de-vs-code)
5. [Otros editores](#5-otros-editores) (VSCodium, Cursor, Windsurf, otros)
6. [Tu primer programa](#6-tu-primer-programa)
7. [Compilar desde VS Code con Ctrl+Shift+B](#7-compilar-desde-vs-code-con-ctrlshiftb)
8. [Comandos de `nyac`](#8-comandos-de-nyac)
9. [Problemas frecuentes](#9-problemas-frecuentes)
10. [Actualizar y desinstalar](#10-actualizar-y-desinstalar)

---

## 1. Qué necesitas

| Programa | Para qué |
|---|---|
| **Git** | Clonar (descargar) este repositorio |
| **Python 3.8 o más nuevo** | Ejecuta el compilador `nyac` (no necesita librerías extra) |
| **.NET SDK 8** | Compila el C# que genera `nyac`. Tiene que ser el **SDK 8**, no el «Runtime» |
| **VS Code** (recomendado) | Colores, icono y snippets para los archivos `.nya` |

NyanSharp **no se descarga como programa aparte**: se clona el repositorio y se
instala desde esa carpeta. La carpeta clonada **es** la instalación, así que no
la borres ni la muevas después.

---

## 2. Instalar en Windows (paso a paso)

Funciona en Windows 10 y 11, desde PowerShell, CMD o el terminal de VS Code.

### Paso 1. Instalar los programas necesarios

Abre **PowerShell** (tecla Windows → escribe `PowerShell` → Enter) y pega:

```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
winget install --id Microsoft.DotNet.SDK.8 -e
winget install --id Microsoft.VisualStudioCode -e
```

Acepta lo que te pregunte (`Y` + Enter). Si ya tienes alguno, winget lo dirá y
pasará al siguiente.

<details>
<summary>¿No tienes <code>winget</code>? Instálalos a mano</summary>

- Git: <https://git-scm.com/download/win> (siguiente, siguiente… con las opciones por defecto).
- Python: <https://www.python.org/downloads/> → en la primera pantalla marca
  **«Add python.exe to PATH»** antes de pulsar Install.
- .NET SDK 8: <https://dotnet.microsoft.com/download/dotnet/8.0> → columna
  **SDK**, «Windows x64 Installer» (no el Runtime).
- VS Code: <https://code.visualstudio.com/> → deja marcada **«Agregar a PATH»**.

</details>

### Paso 2. Cerrar y abrir PowerShell

**Cierra PowerShell y ábrelo otra vez.** Si no, no encontrará los programas que
acabas de instalar. Comprueba que todo responde:

```powershell
git --version
py --version
dotnet --list-sdks
code --version
```

`dotnet --list-sdks` tiene que mostrar una línea que empiece por `8.`.
Si alguno dice «no se reconoce como nombre de un cmdlet», mira
[Problemas frecuentes](#9-problemas-frecuentes).

### Paso 3. Clonar el repositorio

Esto lo descarga en tu carpeta de usuario (`C:\Users\TuNombre\nyansharp`):

```powershell
cd $HOME
git clone https://github.com/nexvylia/nyansharp.git
cd nyansharp
```

### Paso 4. Ejecutar el instalador

Desde esa misma ventana:

```powershell
.\instalar.bat
```

(o doble clic en `instalar.bat` desde el Explorador de archivos, dentro de la
carpeta `nyansharp`).

El instalador:

1. Comprueba que tienes Python 3 y el .NET SDK 8 (si falta algo, te dice el comando exacto para instalarlo y no toca nada).
2. Añade la carpeta `nyansharp` al **PATH de tu usuario**, para que el comando `nyac` funcione en cualquier terminal. No necesita permisos de administrador.
3. Instala la extensión en VS Code (y también en VSCodium, Cursor o Windsurf si los tienes).
4. Abre la documentación en el navegador.

Al final debe salir `Listo desu~`.

### Paso 5. Cerrar todo y probar

**Cierra todas las ventanas de PowerShell/CMD y VS Code** (las que estaban
abiertas no ven el PATH nuevo). Abre PowerShell otra vez y prueba:

```powershell
cd $HOME\nyansharp
nyac run ejemplos\hola.nya
```

Te preguntará tu nombre y te saludará. La primera vez tarda unos segundos
porque .NET prepara el proyecto.

### Paso 6. Abrirlo en VS Code

```powershell
code $HOME\nyansharp
```

Abre `ejemplos\kawaii.nya`: las palabras deben verse de colores y abajo a la
derecha debe poner **NyanSharp**. Pulsa `Ctrl+Shift+B` para compilar.

> **Sin git (ZIP):** en esta página, **Code → Download ZIP**. Haz clic derecho en
> el ZIP → **Extraer todo…** → elige una carpeta fija (por ejemplo
> `C:\Users\TuNombre\nyansharp`). Ejecuta `instalar.bat` **desde la carpeta
> extraída**, nunca desde dentro del ZIP. Si Windows muestra «Windows protegió su
> PC», pulsa **Más información → Ejecutar de todas formas**. Con el ZIP no
> podrás actualizar con `git pull`.

---

## 3. Instalar en Linux y macOS

### Paso 1. Programas necesarios

**Ubuntu / Debian**

```bash
sudo apt install git python3 dotnet-sdk-8.0
```

**Fedora**

```bash
sudo dnf install git python3 dotnet-sdk-8.0
```

**Arch**

```bash
sudo pacman -S git python dotnet-sdk-8.0
```

**macOS** (con [Homebrew](https://brew.sh/))

```bash
brew install git python dotnet@8
```

VS Code: <https://code.visualstudio.com/>. En macOS, después de instalarlo abre
VS Code, `Cmd+Shift+P` → «Shell Command: Install 'code' command in PATH».

### Paso 2. Clonar e instalar

```bash
cd ~
git clone https://github.com/nexvylia/nyansharp.git
cd nyansharp
chmod +x nyac
mkdir -p ~/.local/bin
ln -sf "$PWD/nyac" ~/.local/bin/nyac
code --install-extension nyansharp-1.0.0.vsix
```

Si `~/.local/bin` no está en tu PATH (al escribir `nyac` dice «command not
found»), añádelo una sola vez:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # en macOS: ~/.zshrc
source ~/.bashrc                                            # en macOS: source ~/.zshrc
```

### Paso 3. Probar

```bash
nyac run ejemplos/hola.nya
code ~/nyansharp
```

---

## 4. Instalar la extensión de VS Code

La extensión da: colores para las 101 palabras kawaii, icono propio para los
archivos `.nya`, cierre automático de llaves y comillas, y snippets.

En Windows, `instalar.bat` ya la instala. Usa esta sección si no lo hizo
(por ejemplo, porque VS Code no estaba instalado todavía) o si estás en Linux/macOS.

### Opción A: desde la terminal

Desde la carpeta `nyansharp`:

```bash
code --install-extension nyansharp-1.0.0.vsix
```

### Opción B: desde la interfaz de VS Code

1. Abre VS Code.
2. Ve a **Extensiones** (`Ctrl+Shift+X`, o `Cmd+Shift+X` en Mac).
3. Pulsa los **tres puntos `…`** arriba a la derecha del panel.
4. Elige **«Install from VSIX…»** («Instalar desde VSIX…»).
5. Selecciona el archivo `nyansharp-1.0.0.vsix` de esta carpeta.
6. Si te lo pide, pulsa **Reload** / recargar.

### Comprobar que funciona

Abre `ejemplos/kawaii.nya`. Si ves las palabras en colores y abajo a la derecha
pone **NyanSharp**, está instalada.

> **Importante:** copiar la carpeta `vscode-ext` dentro de `~/.vscode/extensions`
> **no** funciona. Hay que instalar el `.vsix`.

<details>
<summary>¿No tienes el comando <code>code</code> en la terminal?</summary>

- **macOS:** abre VS Code, `Cmd+Shift+P` → «Shell Command: Install 'code' command in PATH».
- **Windows:** reinstala VS Code marcando «Agregar a PATH», o usa la opción B.
- **Linux:** viene con los paquetes oficiales (.deb/.rpm). Con Snap o Flatpak, usa la opción B.

</details>

<details>
<summary>Volver a empaquetar la extensión (solo si cambias <code>vscode-ext/</code>)</summary>

```bash
cd vscode-ext
npx @vscode/vsce package --allow-missing-repository
code --install-extension nyansharp-1.0.0.vsix --force
```

</details>

---

## 5. Otros editores

El mismo `.vsix` sirve en todos los editores basados en VS Code:

| Editor | Cómo instalarla |
|---|---|
| **VSCodium** | `codium --install-extension nyansharp-1.0.0.vsix` o Extensiones → `…` → Install from VSIX |
| **Cursor** | `cursor --install-extension nyansharp-1.0.0.vsix` o Extensiones → `…` → Install from VSIX |
| **Windsurf** | `windsurf --install-extension nyansharp-1.0.0.vsix` o Extensiones → `…` → Install from VSIX |
| **VS Code Insiders** | `code-insiders --install-extension nyansharp-1.0.0.vsix` |

Para **otros editores** (Sublime Text, JetBrains con TextMate Bundles, etc.) puedes
usar la gramática TextMate que está en `vscode-ext/syntaxes/nya.tmLanguage.json`.
Si no, basta con asociar `.nya` a C#: los colores no serán perfectos, pero se lee bien.

El compilador `nyac` no depende de ningún editor: funciona desde cualquier terminal.

---

## 6. Tu primer programa

**Archivo suelto:**

```bash
nyac run ejemplos/hola.nya
```

**Proyecto nuevo:**

```bash
nyac new miapp     # crea miapp/ con nyansharp.json y main.nya
cd miapp
nyac run           # compila y ejecuta
code .             # ábrelo en VS Code
```

El ejecutable queda en `./bin/`. La primera compilación tarda unos segundos
porque .NET prepara el proyecto; las siguientes van más rápido.

Más ejemplos en `ejemplos/`: `kawaii.nya`, `calculadora.nya`, `tresenraya.nya`
y `biblioteca/` (proyecto con un paquete NuGet).

---

## 7. Compilar desde VS Code con Ctrl+Shift+B

Este repositorio trae `.vscode/tasks.json` con dos tareas:

- **`Ctrl+Shift+B`** → «nyac: compilar» (compila la carpeta del archivo abierto).
- **Terminal → Ejecutar tarea… → «nyac: compilar y ejecutar»**.

Los errores salen en el panel **Problemas** y, al hacer clic, te llevan a la
línea exacta del `.nya`.

Para tener lo mismo en tus propios proyectos, copia la carpeta `.vscode/` de
este repositorio dentro de tu proyecto.

---

## 8. Comandos de `nyac`

```bash
nyac hola.nya                 # compila un archivo suelto -> ./bin/hola
nyac run hola.nya             # compila y ejecuta
nyac new miapp                # proyecto: carpeta + nyansharp.json + main.nya
nyac build [carpeta]          # compila todos los .nya de la carpeta
nyac run [carpeta] [args]     # compila y ejecuta el proyecto
nyac add Newtonsoft.Json      # añade un paquete NuGet (versión opcional)
nyac cs hola.nya              # muestra el C# generado
nyac check hola.nya           # avisa de nombres que chocan con palabras C#
nyac diccionario [filtro]     # las 101 palabras kawaii
```

### Configuración del proyecto (`nyansharp.json`)

```json
{ "nombre": "miapp", "tipo": "exe", "paquetes": { "Newtonsoft.Json": "13.0.3" }, "nullable": false }
```

`tipo` puede ser `exe` o `lib` (genera una `.dll`).

### Reglas del lenguaje

- `;` se escribe `nya`. Las `~` sueltas se ignoran.
- Cadenas y comentarios no se traducen, salvo los huecos `{…}` de `$"…"`.
- `@palabra` fuerza un identificador literal (`@kazu` no se traduce).
- `iu` = `Console.WriteLine`, `sasayaku` = `Console.Write`, `kiku` = `Console.ReadLine`,
  `hajimeru` = `Main`.
- Los errores de compilación señalan archivo, línea y columna del `.nya`.

La referencia completa con las 101 palabras está en [`docs.html`](docs.html)
(descárgalo y ábrelo en el navegador) o con `nyac diccionario`.

---

## 9. Problemas frecuentes

### Windows

| Mensaje / síntoma | Solución |
|---|---|
| `nyac : El término 'nyac' no se reconoce…` | No has cerrado y abierto la terminal después de `instalar.bat` (paso 5). Si sigue igual, ejecuta otra vez `instalar.bat` desde la carpeta `nyansharp`. En VS Code, ciérralo **entero** y ábrelo de nuevo. |
| `winget : El término 'winget' no se reconoce…` | Instala «Instalador de aplicación» desde Microsoft Store, o instala los programas a mano (paso 1, desplegable). |
| `git`, `py`, `dotnet` o `code` «no se reconoce» justo después de instalarlos | Cierra PowerShell y ábrelo otra vez (paso 2). |
| `python` abre Microsoft Store o no hace nada | Es el acceso directo falso de Windows. Instala Python con winget (paso 1). `nyac` usa el lanzador `py`, que no tiene este problema. |
| El instalador dice «Falta el .NET SDK 8» pero tienes .NET | Tienes el Runtime u otra versión (9, 10…). Instala también el SDK 8: `winget install --id Microsoft.DotNet.SDK.8 -e`. Pueden convivir. |
| «Estas ejecutando el instalador desde dentro de un ZIP» | Extrae el ZIP (clic derecho → Extraer todo…) y ejecuta `instalar.bat` desde la carpeta extraída. |
| `.\instalar.bat` no se reconoce | No estás dentro de la carpeta: `cd $HOME\nyansharp` y repite. |
| «Windows protegió su PC» | Solo pasa con el ZIP descargado: **Más información → Ejecutar de todas formas**. |
| La extensión no se instaló | VS Code no estaba instalado o no estaba en el PATH al ejecutar `instalar.bat`. Instálala a mano (sección 4, opción B) o vuelve a ejecutar `instalar.bat`. |
| Los emoticonos salen como `?` | Usa **Windows Terminal** o el terminal de VS Code; la consola antigua (conhost) no tiene esos símbolos en su fuente. |

### Linux y macOS

| Mensaje / síntoma | Solución |
|---|---|
| `nyac: command not found` | Falta `~/.local/bin` en el PATH (sección 3, paso 2) o no has abierto una terminal nueva. |
| `Permission denied` al ejecutar `nyac` | `chmod +x ~/nyansharp/nyac` |
| `dotnet: command not found` / `No .NET SDKs were found` | Falta el .NET SDK 8 (sección 3, paso 1). |

### En todos

| Mensaje / síntoma | Solución |
|---|---|
| Los `.nya` salen sin colores en VS Code | La extensión no está instalada (sección 4). Abajo a la derecha elige el lenguaje **NyanSharp**. |
| Ctrl+Shift+B no hace nada | Abre la **carpeta** (Archivo → Abrir carpeta), no un archivo suelto, y copia `.vscode/` a tu proyecto. |
| Un nombre tuyo se convierte en otra cosa | Choca con una palabra kawaii: usa `@nombre` o comprueba con `nyac check`. |

---

## 10. Actualizar y desinstalar

**Actualizar** (si lo instalaste con git):

```bash
cd ~/nyansharp        # Windows: cd $HOME\nyansharp
git pull
code --install-extension nyansharp-1.0.0.vsix --force
```

**Desinstalar en Windows:** doble clic en `desinstalar.bat` (quita `nyac` del
PATH y la extensión de VS Code). Después borra la carpeta `nyansharp`.

**Desinstalar en Linux/macOS:**

```bash
rm ~/.local/bin/nyac
code --uninstall-extension nexvylia.nyansharp
rm -rf ~/nyansharp
```

---

## Estructura del repositorio

| Ruta | Qué es |
|---|---|
| `nyac` / `nyac.py` | Compilador (el mismo script; `nyac` para Linux/Mac) |
| `nyac.cmd` | Lanzador para Windows (usa `py` o `python`) |
| `instalar.bat`, `desinstalar.bat` | Instalación en Windows |
| `vscode-ext/` | Código fuente de la extensión de VS Code |
| `nyansharp-1.0.0.vsix` | Extensión empaquetada, lista para instalar |
| `ejemplos/` | hola, kawaii, calculadora, tresenraya y biblioteca (con NuGet) |
| `docs.html` | Documentación completa |
| `pruebas.sh` | Suite de pruebas para Linux/macOS (9 casos, necesita .NET 8) |
| `.github/workflows/pruebas.yml` | Pruebas automáticas en Windows y Linux en cada cambio |

## Estado

Versión 1.0 (septiembre 2026). Cada cambio se prueba automáticamente en Windows
(instalación con `instalar.bat`, en PowerShell y CMD) y en Linux. Si algo no te
funciona, abre un issue con el mensaje de error.

## Licencia

MIT. © 2026 Matias Quiriquino / NEXVYLIA. Ver [`LICENSE`](LICENSE).
