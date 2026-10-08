#!/usr/bin/env bash
# Suite de pruebas de NyanSharp. Uso: ./pruebas.sh
set -u
cd "$(dirname "$0")"
ok=0; ko=0
pasa(){ echo "  ✔ $1"; ok=$((ok+1)); }
falla(){ echo "  ✘ $1"; ko=$((ko+1)); }

# 1. ejemplos compilan y su salida contiene lo esperado
prueba(){ # nombre, entrada, texto esperado
  local out; out=$(printf "$2" | ./nyac run "ejemplos/$1.nya" 2>&1)
  grep -qF "$3" <<<"$out" && pasa "$1" || { falla "$1"; echo "$out" | tail -5; }
}
prueba hola        'Matias\n'          'Encantada, Matias-kun'
prueba kawaii      ''                  'pares: 2, 4, 6, 8, 10  suma: 30'
prueba calculadora '3 * 4\n10 / 0\n\n' 'Gomen~ ¡No se divide por cero'
prueba tresenraya  '5\n1\n3\n7\nn\n'   'he ganado yo'

# 2. proyecto multi-archivo + NuGet
out=$(./nyac run ejemplos/biblioteca a b 2>&1)
grep -q '"Titulo": "Kokoro"' <<<"$out" && grep -q 'args recibidos: 2' <<<"$out" && pasa "proyecto biblioteca (2 .nya + Newtonsoft)" || { falla "proyecto biblioteca"; echo "$out" | tail -5; }

# 3. errores con línea correcta y archivo correcto
t=$(mktemp -d); mkdir "$t/p"; printf '{"nombre":"p","tipo":"exe","paquetes":{}}' > "$t/p/nyansharp.json"
printf 'onegai sekai nya\nnakama A { minna zutto nanimo hajimeru() { B.F() nya } }\n' > "$t/p/main.nya"
printf 'nakama B {\n  minna zutto nanimo F() {\n    kazu x = "texto" nya\n  }\n}\n' > "$t/p/otro.nya"
out=$(./nyac build "$t/p" 2>&1)
grep -q 'otro.nya:3:' <<<"$out" && grep -q CS0029 <<<"$out" && pasa "error apunta a otro.nya:3" || { falla "mapa de errores"; echo "$out"; }

# 4. traducción pura
cs=$(printf 'kazu a = 1 nya~\niu($"{kazu.MaxValue} nya {a:0.0}") nya\nkotoba @kazu = "x" nya\n' > "$t/x.nya"; ./nyac cs "$t/x.nya")
grep -qF 'int a = 1;' <<<"$cs" && grep -qF '$"{int.MaxValue} nya {a:0.0}"' <<<"$cs" && grep -qF 'string @kazu' <<<"$cs" \
  && pasa "traducción: ~, huecos interpolados, @verbatim" || { falla "traducción"; echo "$cs"; }

# 5. check
printf 'kazu int = 3 nya\n' > "$t/c.nya"; ./nyac check "$t/c.nya" >/dev/null && falla "check no avisó" || pasa "check avisa de «int» como nombre"

# 6. librería
mkdir "$t/lib"; printf '{"nombre":"MiLib","tipo":"lib","paquetes":{}}' > "$t/lib/nyansharp.json"
printf 'oshiro MiLib { minna zutto nakama U { minna zutto kazu Doble(kazu x) => x * 2 nya } }\n' > "$t/lib/u.nya"
./nyac build "$t/lib" 2>&1 | grep -q 'librería lista' && [ -f "$t/lib/bin/MiLib.dll" ] && pasa "proyecto tipo lib -> .dll" || falla "lib"

rm -rf "$t"
echo; echo "  $ok pasan, $ko fallan"; [ $ko -eq 0 ]
