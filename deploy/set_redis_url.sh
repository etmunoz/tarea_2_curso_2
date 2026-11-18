# --8<-- encabezado-grupo
# Archivo: deploy/set_redis_url.sh
# Objetivo: Guardar el REDIS_URL (con clave) en el almacen de config SIN mostrarlo ni dejarlo en /etc.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# --8<-- fin-encabezado-grupo
#!/usr/bin/env bash
# Lee el REDIS_URL de forma OCULTA (no se muestra en pantalla, no queda en el history ni en el chat)
# y lo guarda en el almacen de config (logs/config.sqlite). Debe correr como el usuario de la app (web6).
# Uso (desde el shell de administrator):
#   sudo -u web6 bash /var/www/clients/client1/web6/home/etmkuseretmk2/tarea_2_curso_2/deploy/set_redis_url.sh
set -euo pipefail
cd "$(cd "$(dirname "$0")/.." && pwd)"
read -rs -p "Pega el REDIS_URL (rediss://usuario:password@host:puerto/0) — no se mostrara: " RU
echo
printf '%s' "$RU" | .venv/bin/python -c 'import sys; sys.path.insert(0, "."); from src.config import ajustes; ok = ajustes.set("REDIS_URL", sys.stdin.read().strip()); print("guardado OK en el almacen de config" if ok else "RECHAZADO (revisa el formato)")'
unset RU
