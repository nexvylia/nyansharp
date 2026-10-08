#!/usr/bin/env python3
"""nyac — compilador de NyanSharp (.nya) a ejecutable nativo vía C#/.NET.

Uso:
  nyac archivo.nya                 compila un archivo suelto -> ./bin/<nombre>
  nyac run archivo.nya [args...]   compila y ejecuta
  nyac new <nombre>                crea un proyecto (carpeta + nyansharp.json + main.nya)
  nyac build [carpeta]             compila un proyecto (todos los .nya de la carpeta)
  nyac run [carpeta] [args...]     compila y ejecuta un proyecto
  nyac add <Paquete> [version]     añade un paquete NuGet al proyecto
  nyac cs archivo.nya              muestra el C# generado
  nyac check archivo.nya           avisa de identificadores que chocan con palabras clave
  nyac diccionario [filtro]        lista palabras clave
  nyac version
"""
import json, os, re, subprocess, sys

# Windows: si la salida va a un pipe (tareas, CI), no reventar con los emoticonos.
for _s in (sys.stdout, sys.stderr):
    try:
        if not _s.isatty():
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Salida de dotnet: en Windows usa la página de códigos de la consola.
SALIDA_DOTNET = "oem" if os.name == "nt" else "utf-8"

def ruta_corta(ruta):
    """relpath que no falla en Windows si la ruta está en otra unidad (C: vs D:)."""
    try:
        return os.path.relpath(ruta)
    except ValueError:
        return ruta

VERSION = "1.0.0"

# ---------- diccionario kawaii -> C# ----------
PALABRAS = {
    # estructura
    "onegai": "using", "sekai": "System", "oshiro": "namespace", "nakama": "class",
    "kokoro": "struct", "yakusoku": "interface", "erabimono": "enum", "kiroku": "record",
    "hajimeru": "Main", "bubun": "partial", "tojita": "sealed", "uchi": "internal",
    "minna_no": "global",
    # modificadores
    "minna": "public", "himitsu": "private", "mamoru": "protected", "zutto": "static",
    "kawaranai": "readonly", "taisetsu": "const", "yume": "abstract",
    "kakikaeru": "override", "maboroshi": "virtual", "nonbiri": "async", "matte": "await",
    "hitsuyou": "required", "hajime": "init", "yuragu": "volatile", "sotogawa": "extern",
    "abunai": "unsafe", "atarashiku": "new",
    # tipos
    "nanimo": "void", "kazu": "int", "nagakazu": "long", "chibikazu": "short",
    "puchikazu": "float", "dekakazu": "double", "okane": "decimal", "kotoba": "string",
    "moji": "char", "hontou": "bool", "mono": "object", "nanika": "var",
    "baito": "byte", "sbaito": "sbyte", "ukazu": "uint", "unagakazu": "ulong",
    "uchibikazu": "ushort", "dainamikku": "dynamic", "yubisaki": "nint",
    # literales
    "hai": "true", "iie": "false", "nai": "null",
    # control
    "moshi": "if", "janakya": "else", "aida": "while", "yaru": "do",
    "kurikaeshi": "for", "hitotsuzutsu": "foreach", "naka": "in",
    "erabu": "switch", "baai": "case", "futsuu": "default", "toki": "when",
    "yamete": "break", "tsuzukete": "continue", "kaeru": "return", "tobu": "goto",
    "ageteku": "yield", "kagi": "lock", "tashikame": "checked", "tekitou": "unchecked",
    # objetos
    "atarashii": "new", "atashi": "this", "okaasan": "base", "desu": "is",
    "toshite": "as", "soto": "out", "sasu": "ref", "nanikore": "typeof",
    "choudai": "get", "ageru": "set", "namae": "nameof", "ookisa": "sizeof",
    "ippai": "params", "tomoni": "with", "doko": "where", "ensou": "operator",
    "sotto": "implicit", "hakkiri": "explicit", "yakusokushita": "delegate",
    "dekigoto": "event", "kotei": "fixed", "tsumu": "stackalloc",
    # errores
    "ganbaru": "try", "daijoubu": "catch", "owari": "finally", "nageru": "throw",
    # entrada / salida
    "iu": "Console.WriteLine", "sasayaku": "Console.Write", "kiku": "Console.ReadLine",
    # fin de sentencia
    "nya": ";",
}
INVERSO = {}
for k, v in PALABRAS.items():
    INVERSO.setdefault(v, k)

TOKEN = re.compile(r'''
    (?P<coment>//[^\n]*|/\*.*?\*/)              |
    (?P<cadena>\$?@?"(?:\\.|[^"\\])*"|@?\$"(?:\\.|[^"\\])*"|"""[\s\S]*?""")   |
    (?P<caracter>'(?:\\.|[^'\\])')              |
    (?P<verbatim>@[A-Za-z_][A-Za-z0-9_]*)       |
    (?P<palabra>[A-Za-z_][A-Za-z0-9_]*)         |
    (?P<tilde>~+)                               |
    (?P<otro>.)
''', re.S | re.X)

HUECO = re.compile(r'(?<!\{)\{(?!\{)([^{}"]*)\}')

def traducir_interpolada(cadena: str) -> str:
    """Dentro de $"..." solo se traducen los huecos {expresion}, no el texto."""
    def hueco(m):
        exp = m.group(1)
        # no tocar formato tras ':'  ->  {x:0.00}
        cuerpo, sep, fmt = exp.partition(":")
        cuerpo = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", lambda w: PALABRAS.get(w.group(), w.group())
                        if PALABRAS.get(w.group()) != ";" else w.group(), cuerpo)
        return "{" + cuerpo + sep + fmt + "}"
    return HUECO.sub(hueco, cadena)

def traducir(fuente: str) -> str:
    salida = []
    for m in TOKEN.finditer(fuente):
        k = m.lastgroup
        t = m.group()
        if k == "palabra":
            if t == "nya" and salida and salida[-1].isspace():
                salida.pop()               # "x = 1 nya" -> "x = 1;" (C# limpio)
            salida.append(PALABRAS.get(t, t))
        elif k == "cadena" and t.lstrip("@").startswith("$"):
            salida.append(traducir_interpolada(t))
        elif k == "verbatim":
            salida.append(t)               # @kazu -> identificador literal, no se traduce
        elif k == "tilde":
            salida.append("")              # las ~ decorativas se ignoran (uwu~)
        else:
            salida.append(t)
    return "".join(salida)

# ---------- comprobaciones ----------
def check(ruta: str) -> int:
    """Avisa cuando una declaración usa como nombre una palabra clave C# 'a pelo'."""
    fuente = open(ruta, encoding="utf-8").read()
    cs_kw = set(PALABRAS.values()) - {";", "Main", "System", "Console.WriteLine",
                                      "Console.Write", "Console.ReadLine"}
    avisos = 0
    for n, linea in enumerate(fuente.splitlines(), 1):
        for m in re.finditer(r'\b(kazu|kotoba|hontou|nanika|dekakazu|puchikazu|nagakazu|moji|mono)\s+([A-Za-z_]\w*)\s*[=;]', linea):
            nombre = m.group(2)
            if nombre in cs_kw:
                print(f"  (・_・;) {os.path.basename(ruta)}:{n}: la variable «{nombre}» es palabra clave de C#; "
                      f"usa @{nombre} o cambia el nombre (en NyanSharp se dice «{INVERSO.get(nombre, '?')}»)")
                avisos += 1
    if not avisos:
        print("  (✿◠‿◠) sin avisos desu~")
    return avisos

# ---------- errores ----------
def mostrar_errores(texto: str, mapa_nombres):
    patron = re.compile(r'([^\s(]+\.cs)\((\d+),(\d+)\): (error|warning) (CS\d+): (.*?) \[')
    vistos = set()
    for m in patron.finditer(texto):
        archivo, linea, col, tipo, cod, msg = m.groups()
        nya = mapa_nombres.get(os.path.basename(archivo), archivo)
        clave = (nya, linea, col, cod)
        if clave in vistos: continue
        vistos.add(clave)
        cara = "(>_<)" if tipo == "error" else "(・_・;)"
        print(f"  {cara} {nya}:{linea}:{col}  {cod}: {msg}")
    if not vistos:
        print(texto)

# ---------- proyecto ----------
CONFIG = "nyansharp.json"

# Se añade a los ejecutables: consola en UTF-8 para que los emoticonos y las
# tildes salgan bien también en Windows (por defecto usa la página 850/437).
INICIO_CS = """#pragma warning disable
namespace NyanSharpInterno
{
    internal static class Inicio
    {
        [System.Runtime.CompilerServices.ModuleInitializer]
        internal static void Iniciar()
        {
            try { System.Console.OutputEncoding = new System.Text.UTF8Encoding(false); } catch { }
        }
    }
}
"""

CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>{tipo}</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>{nullable}</Nullable>
    <AllowUnsafeBlocks>true</AllowUnsafeBlocks>
    <AssemblyName>{nombre}</AssemblyName>
    <RootNamespace>{nombre}</RootNamespace>
    <InvariantGlobalization>true</InvariantGlobalization>
    <SatelliteResourceLanguages>en</SatelliteResourceLanguages>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
    <TreatWarningsAsErrors>false</TreatWarningsAsErrors>
    <NoWarn>CS8632</NoWarn>
  </PropertyGroup>
  <ItemGroup>
{compilar}
  </ItemGroup>
  <ItemGroup>
{paquetes}
  </ItemGroup>
</Project>
"""

def cargar_config(carpeta):
    ruta = os.path.join(carpeta, CONFIG)
    cfg = {"nombre": os.path.basename(os.path.abspath(carpeta)), "tipo": "exe",
           "paquetes": {}, "nullable": False}
    if os.path.isfile(ruta):
        cfg.update(json.load(open(ruta, encoding="utf-8")))
    return cfg, ruta

def guardar_config(cfg, ruta):
    json.dump(cfg, open(ruta, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

def fuentes_de(carpeta):
    out = []
    for raiz, dirs, files in os.walk(carpeta):
        dirs[:] = [d for d in dirs if d not in (".nyabuild", "bin", "obj", ".git", ".vscode")]
        for f in files:
            if f.endswith(".nya"):
                out.append(os.path.join(raiz, f))
    return sorted(out)

def compilar(fuentes, carpeta, cfg, ejecutar=False, args=()):
    nombre = re.sub(r"[^A-Za-z0-9_]", "_", cfg["nombre"])
    obj = os.path.join(carpeta, ".nyabuild")
    bin_dir = os.path.join(carpeta, "bin")
    os.makedirs(obj, exist_ok=True)

    mapa = {}
    compilar_items = []
    for f in fuentes:
        rel = os.path.relpath(f, carpeta)
        cs_rel = rel[:-4] + ".cs"
        cs_abs = os.path.join(obj, cs_rel)
        os.makedirs(os.path.dirname(cs_abs), exist_ok=True)
        open(cs_abs, "w", encoding="utf-8").write(traducir(open(f, encoding="utf-8").read()))
        mapa[os.path.basename(cs_abs)] = rel
        compilar_items.append(f'    <Compile Include="{cs_rel}" />')

    tipo = {"exe": "Exe", "lib": "Library"}.get(cfg.get("tipo", "exe"), "Exe")
    if tipo == "Exe":
        open(os.path.join(obj, "_nyansharp_inicio.cs"), "w", encoding="utf-8").write(INICIO_CS)
        compilar_items.append('    <Compile Include="_nyansharp_inicio.cs" />')

    paquetes = [f'    <PackageReference Include="{p}" Version="{v}" />' for p, v in cfg.get("paquetes", {}).items()]
    csproj = os.path.join(obj, f"{nombre}.csproj")
    open(csproj, "w", encoding="utf-8").write(CSPROJ.format(
        nombre=nombre, tipo=tipo, nullable="enable" if cfg.get("nullable") else "disable",
        compilar="\n".join(compilar_items), paquetes="\n".join(paquetes)))

    n = len(fuentes)
    print(f"  (≧◡≦) compilando {nombre} ({n} archivo{'s' if n != 1 else ''}) ...")
    r = subprocess.run(
        ["dotnet", "build", "-c", "Release", "-nologo", "-v", "q", "-o", bin_dir, csproj],
        capture_output=True, text=True, encoding=SALIDA_DOTNET, errors="replace",
        env={**os.environ, "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_NOLOGO": "1"})
    if r.returncode != 0:
        print("  (>_<) gomen nasai~ hay errores:")
        mostrar_errores(r.stdout + r.stderr, mapa)
        sys.exit(1)
    if "warning" in r.stdout:
        mostrar_errores(r.stdout, mapa)

    if tipo == "Library":
        print(f"  (✿◠‿◠) librería lista desu~  ->  {ruta_corta(os.path.join(bin_dir, nombre + '.dll'))}")
        return
    exe = os.path.join(bin_dir, nombre + (".exe" if os.name == "nt" else ""))
    print(f"  (✿◠‿◠) listo desu~  ->  {ruta_corta(exe)}")
    if ejecutar:
        print("  ─────────────────────────")
        sys.stdout.flush()
        sys.exit(subprocess.call([exe, *args]))

def objetivo(ruta, ejecutar=False, args=()):
    """Archivo suelto o carpeta de proyecto."""
    if os.path.isdir(ruta):
        cfg, _ = cargar_config(ruta)
        fuentes = fuentes_de(ruta)
        if not fuentes:
            sys.exit(f"  (;_;) no hay archivos .nya en {ruta}")
        compilar(fuentes, ruta, cfg, ejecutar, args)
    elif os.path.isfile(ruta):
        carpeta = os.path.dirname(os.path.abspath(ruta))
        nombre = os.path.splitext(os.path.basename(ruta))[0]
        cfg = {"nombre": nombre, "tipo": "exe", "paquetes": {}}
        # si el archivo vive en un proyecto, respeta sus paquetes
        cfg_proj, _ = cargar_config(carpeta)
        if os.path.isfile(os.path.join(carpeta, CONFIG)):
            cfg["paquetes"] = cfg_proj.get("paquetes", {})
        compilar([ruta], carpeta, cfg, ejecutar, args)
    else:
        sys.exit(f"  (;_;) no encuentro {ruta}")

def nuevo(nombre):
    if os.path.exists(nombre):
        sys.exit(f"  (;_;) ya existe {nombre}")
    os.makedirs(nombre)
    guardar_config({"nombre": nombre, "tipo": "exe", "paquetes": {}, "nullable": False},
                   os.path.join(nombre, CONFIG))
    open(os.path.join(nombre, "main.nya"), "w", encoding="utf-8").write(f"""// {nombre} — creado con nyac new
onegai sekai nya

oshiro {nombre}
{{
    minna nakama Programa
    {{
        minna zutto nanimo hajimeru(kotoba[] args)
        {{
            iu("Konnichiwa desde {nombre}~ (◕‿◕✿)") nya
        }}
    }}
}}
""")
    open(os.path.join(nombre, ".gitignore"), "w", encoding="utf-8").write("bin/\n.nyabuild/\n")
    print(f"  (✿◠‿◠) proyecto {nombre} creado. Prueba:  cd {nombre} && nyac run")

def add(paquete, version=None):
    cfg, ruta = cargar_config(".")
    if not os.path.isfile(ruta):
        sys.exit(f"  (;_;) aquí no hay {CONFIG}. Usa «nyac new» o créalo.")
    if not version:
        r = subprocess.run(["dotnet", "package", "search", paquete, "--exact-match", "--format", "json"],
                           capture_output=True, text=True, encoding=SALIDA_DOTNET, errors="replace")
        try:
            datos = json.loads(r.stdout)
            version = datos["searchResult"][0]["packages"][0]["latestVersion"]
        except Exception:
            sys.exit("  (;_;) no pude averiguar la versión. Pásala: nyac add Paquete 1.2.3")
    cfg.setdefault("paquetes", {})[paquete] = version
    guardar_config(cfg, ruta)
    print(f"  (✿◠‿◠) añadido {paquete} {version}")

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__); return
    cmd = a[0]
    if cmd == "version":
        print(f"nyac {VERSION} · NyanSharp (=^･ω･^=)"); return
    if cmd == "diccionario":
        f = a[1].lower() if len(a) > 1 else ""
        for k, v in PALABRAS.items():
            if f in k or f in v.lower(): print(f"  {k:<14} -> {v}")
        return
    if cmd == "cs":
        print(traducir(open(a[1], encoding="utf-8").read())); return
    if cmd == "check":
        sys.exit(1 if check(a[1]) else 0)
    if cmd == "new":
        nuevo(a[1]); return
    if cmd == "add":
        add(a[1], a[2] if len(a) > 2 else None); return
    if cmd == "build":
        objetivo(a[1] if len(a) > 1 else "."); return
    if cmd == "run":
        if len(a) > 1 and (os.path.exists(a[1])):
            objetivo(a[1], ejecutar=True, args=a[2:])
        else:
            objetivo(".", ejecutar=True, args=a[1:])
        return
    objetivo(cmd)

if __name__ == "__main__":
    main()
