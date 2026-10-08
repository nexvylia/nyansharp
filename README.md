# NyanSharp (.nya) · v1.0

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

1. [Requisitos](#1-requisitos)
2. [Descargar NyanSharp](#2-descargar-nyansharp)
3. [Instalar el compilador `nyac`](#3-instalar-el-compilador-nyac) (Linux · macOS · Windows)
4. [Instalar la extensión de VS Code](#4-instalar-la-extensión-de-vs-code)
5. [Otros editores](#5-otros-editores) (VSCodium, Cursor, Windsurf, otros)
6. [Tu primer programa](#6-tu-primer-programa)
7. [Compilar desde VS Code con Ctrl+Shift+B](#7-compilar-desde-vs-code-con-ctrlshiftb)
8. [Comandos de `nyac`](#8-comandos-de-nyac)
9. [Problemas frecuentes](#9-problemas-frecuentes)
10. [Desinstalar](#10-desinstalar)

---

## 1. Requisitos

| Programa | Para qué | Descarga |
|---|---|---|
| **Python 3.8+** | Ejecuta el compilador `nyac` (no necesita librerías extra) | <https://www.python.org/downloads/> |
| **.NET SDK 8** | Compila el C# que genera `nyac`. Tiene que ser el **SDK**, no solo el Runtime | <https://dotnet.microsoft.com/download/dotnet/8.0> |
| **VS Code** (opcional) | Resaltado de colores, icono y snippets para `.nya` | <https://code.visualstudio.com/> |

Comprueba que los tienes abriendo una terminal:

```bash
python3 --version    # en Windows: python --version
dotnet --list-sdks   # debe salir una línea que empiece por 8.
code --version       # solo si vas a usar VS Code
```

<details>
<summary>Instalar los requisitos desde la terminal</summary>

**Ubuntu / Debian**

```bash
sudo apt install python3 dotnet-sdk-8.0
```

**Fedora**

```bash
sudo dnf install python3 dotnet-sdk-8.0
```

**Arch**

```bash
sudo pacman -S python dotnet-sdk-8.0
```

**macOS** (con [Homebrew](https://brew.sh/))

```bash
brew install python dotnet@8
```

**Windows** (con winget, desde PowerShell)

```powershell
winget install Python.Python.3.12 Microsoft.DotNet.SDK.8 Microsoft.VisualStudioCode
```

</details>

---

## 2. Descargar NyanSharp

Con git:

```bash
git clone https://github.com/nexvylia/nyansharp.git
cd nyansharp
```

Sin git: en esta página pulsa **Code → Download ZIP** y descomprímelo donde quieras.

---

## 3. Instalar el compilador `nyac`

### Linux y macOS

Desde la carpeta `nyansharp`:

```bash
chmod +x nyac
mkdir -p ~/.local/bin
ln -sf "$PWD/nyac" ~/.local/bin/nyac
```

Si `~/.local/bin` no está en tu PATH, añádelo (una sola vez):

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc   # o ~/.zshrc en macOS/zsh
source ~/.bashrc
```

Prueba:

```bash
nyac run ejemplos/hola.nya
```

> El enlace apunta a la carpeta que has clonado: no la borres ni la muevas. Para
> actualizar basta con `git pull` dentro de ella.

### Windows

**Opción fácil:** doble clic en `instalar.bat`. El instalador:

1. Comprueba que tienes Python, .NET SDK 8 y VS Code.
2. Copia NyanSharp a `%LOCALAPPDATA%\NyanSharp`.
3. Lo añade al PATH de tu usuario.
4. Instala la extensión de VS Code (si encuentra el comando `code`).
5. Abre la documentación.

Después **cierra y vuelve a abrir la terminal** y prueba:

```bat
nyac run ejemplos\hola.nya
```

**Opción manual:** añade la carpeta `nyansharp` al PATH (Inicio → «Editar las
variables de entorno de tu cuenta» → `Path` → Nuevo). El archivo `nyac.cmd` hace
que el comando `nyac` funcione en CMD y PowerShell.

> Al instalar Python en Windows, marca la casilla **«Add python.exe to PATH»**.

---

## 4. Instalar la extensión de VS Code

La extensión da: colores para las 101 palabras kawaii, icono propio para los
archivos `.nya`, cierre automático de llaves y comillas, y snippets.

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

| Mensaje / síntoma | Solución |
|---|---|
| `nyac: command not found` / «no se reconoce como comando» | El PATH no está bien. Repite el paso 3 y **abre una terminal nueva**. |
| `dotnet: command not found` | Falta el .NET SDK 8 (paso 1). |
| `No .NET SDKs were found` o error de versión | Tienes el Runtime pero no el **SDK**. Instala el SDK 8. |
| `python3: not found` (Windows) | En Windows el comando es `python`. Reinstala Python marcando «Add to PATH». |
| `Permission denied` al ejecutar `nyac` | `chmod +x nyac` dentro de la carpeta. |
| Los `.nya` salen sin colores en VS Code | La extensión no está instalada: paso 4. Abajo a la derecha elige el lenguaje **NyanSharp**. |
| Ctrl+Shift+B no hace nada | Abre la **carpeta** del proyecto (Archivo → Abrir carpeta), no un archivo suelto, y copia `.vscode/`. |
| Un nombre tuyo se convierte en otra cosa | Choca con una palabra kawaii: usa `@nombre` o comprueba con `nyac check`. |

---

## 10. Desinstalar

- **Extensión:** `code --uninstall-extension nexvylia.nyansharp` (o desde el panel de Extensiones).
- **Linux/macOS:** `rm ~/.local/bin/nyac` y borra la carpeta clonada.
- **Windows:** borra `%LOCALAPPDATA%\NyanSharp` y quítala del `Path` de tu usuario.

---

## Estructura del repositorio

| Ruta | Qué es |
|---|---|
| `nyac` / `nyac.py` | Compilador (el mismo script; `nyac` para Linux/Mac) |
| `nyac.cmd` | Lanzador para Windows |
| `vscode-ext/` | Código fuente de la extensión de VS Code |
| `nyansharp-1.0.0.vsix` | Extensión empaquetada, lista para instalar |
| `ejemplos/` | hola, kawaii, calculadora, tresenraya y biblioteca (con NuGet) |
| `docs.html` | Documentación completa |
| `instalar.bat`, `LEEME-WINDOWS.txt` | Instalación en Windows |
| `pruebas.sh` | Suite de pruebas (9 casos, ~3 min, necesita .NET 8) |

## Estado

Versión 1.0 (septiembre 2026). Probado en Linux. El instalador de Windows está
hecho pero aún no se ha probado en un Windows real: si lo pruebas, abre un issue
contando cómo fue.

## Licencia

MIT. © 2026 Matias Quiriquino / NEXVYLIA. Ver [`LICENSE`](LICENSE).
