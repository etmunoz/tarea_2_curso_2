# --8<-- encabezado-grupo
# Archivo: deploy/deploy_local_a_vps.sh
# Objetivo: Desplegar el codigo LOCAL del repo a la VPS (web6), sin secretos ni bitacora.
# Grupo del curso: Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
# --8<-- fin-encabezado-grupo
#!/usr/bin/env bash
# Despliega el codigo del repo local a la VPS (web6). NO sube secretos (.env), BD ni la bitacora.
# Uso:  bash deploy/deploy_local_a_vps.sh
# Luego: reinicia en la VPS los servicios afectados (requiere sudo / administrator).
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
DEST="etmkuseretmk2@etmk.cl:tarea_2_curso_2/"
rsync -az \
  --exclude ".git" --exclude ".venv" --exclude "logs" --exclude "__pycache__" --exclude "*.pyc" \
  --exclude "*.sqlite" --exclude ".env" --exclude ".env.local" --exclude ".DS_Store" \
  --exclude "prompts_ejecutados" --exclude "respuestas" \
  --exclude ".langgraph_api" --exclude ".pytest_cache" \
  -e "ssh -o BatchMode=yes" "$RAIZ/" "$DEST"
echo "OK · codigo desplegado a la VPS."
echo "Reinicia los servicios afectados, por ejemplo:"
echo "  sudo systemctl restart t2c2-web t2c2-api t2c2-monitor t2c2-langgraph t2c2-fichas"
