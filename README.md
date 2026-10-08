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

## Estado

Versión 1.0 terminada (septiembre 2026). Probado en Linux. El instalador de
Windows (`instalar.bat`) está hecho pero sin probar en un Windows real.

## Stack

- Python 3 (el compilador `nyac`, sin dependencias)
- .NET SDK 8 (compila el C# generado)
- Extensión de VS Code: resaltado, icono y snippets

## Instalar

Linux / Mac:

```bash
git clone github-nexvylia:nexvylia/nyansharp.git
cd nyansharp
ln -s "$PWD/nyac" ~/bin/nyac            # o añade la carpeta al PATH
code --install-extension nyansharp-1.0.0.vsix
```

Windows: instala Python 3, .NET SDK 8 y VS Code, y haz doble clic en
`instalar.bat`. Detalle en [`LEEME-WINDOWS.txt`](LEEME-WINDOWS.txt).

## Uso

```bash
nyac hola.nya                 # archivo suelto -> ./bin/hola
nyac run hola.nya             # compila y ejecuta
nyac new miapp                # proyecto: carpeta + nyansharp.json + main.nya
nyac build [carpeta]          # compila todos los .nya de la carpeta
nyac run [carpeta] [args]     # compila y ejecuta el proyecto
nyac add Newtonsoft.Json      # añade paquete NuGet (versión opcional)
nyac cs hola.nya              # ver el C# generado
nyac check hola.nya           # avisa de nombres que chocan con palabras C#
nyac diccionario [filtro]     # las 101 palabras
```

En VS Code, con la carpeta abierta, Ctrl+Shift+B compila el proyecto del
archivo activo (tareas en `.vscode/tasks.json`).

## Configuración del proyecto (`nyansharp.json`)

```json
{ "nombre": "miapp", "tipo": "exe", "paquetes": { "Newtonsoft.Json": "13.0.3" }, "nullable": false }
```

`tipo` puede ser `exe` o `lib` (genera una `.dll`). No usa variables de entorno.

## Reglas del lenguaje

- `;` se escribe `nya`. Las `~` sueltas se ignoran.
- Cadenas y comentarios no se traducen, salvo los huecos `{…}` de `$"…"`.
- `@palabra` fuerza un identificador literal (`@kazu` no se traduce).
- `iu` = Console.WriteLine, `sasayaku` = Console.Write, `kiku` = Console.ReadLine,
  `hajimeru` = Main.
- Los errores de compilación señalan archivo, línea y columna del `.nya`.

## Documentación

La referencia completa está en [`docs.html`](docs.html) (ábrela en el navegador).

## Estructura

| Ruta | Qué es |
|---|---|
| `nyac` / `nyac.py` | Compilador (los dos son el mismo script; `nyac` para Linux/Mac) |
| `nyac.cmd` | Lanzador para Windows |
| `vscode-ext/` | Código de la extensión de VS Code |
| `nyansharp-1.0.0.vsix` | Extensión empaquetada, lista para instalar |
| `ejemplos/` | hola, kawaii, calculadora, tresenraya y biblioteca (proyecto con NuGet) |
| `docs.html` | Documentación completa |
| `instalar.bat`, `LEEME-WINDOWS.txt` | Instalación en Windows |
| `pruebas.sh` | Suite de pruebas |

## Pruebas

```bash
./pruebas.sh     # 9 casos, unos 3 minutos (necesita .NET 8)
```

## Licencia

MIT. © 2026 Matias Quiriquino / NEXVYLIA. Ver [`LICENSE`](LICENSE).
