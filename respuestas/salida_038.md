<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_038.md`  
> **Objetivo:** 038 · Respuesta — idioma preferido y forma de saludar en el perfil  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1140 · **Última modificación:** 20261119 1140
<!--/encabezado-grupo-->

# 038 · Respuesta — Idioma y forma de saludar

**Prompt:** [`../prompts_ejecutados/prompt_038.md`](../prompts_ejecutados/prompt_038.md)

---

## 1. Qué se hizo

- **`perfiles`** suma `idioma` y `saludo` (migración `ALTER TABLE` idempotente para la BD existente);
  `guardar_perfil`/`obtener_perfil` actualizan solo los campos provistos.
- Herramientas `preferencias_usuario` / `recordar_preferencias` (nombre/idioma/saludo).
- Prompt del administrador:
  - **Idioma**: español por defecto; responde en el idioma de la persona de forma **consistente** (sin
    mezclar); si usa/pide otro idioma, lo adopta y lo guarda; vuelve a español si la persona vuelve.
  - **Saludo**: replica la forma propia de saludar de la persona («wena», «¡buenas!») y la guarda,
    combinándola con la franja horaria.
- Tests: **15 passed** (nombre/idioma/saludo por separado).

## 2. Pendiente de activación

- `sudo systemctl restart t2c2-langgraph` (agente administrador). Verificación en vivo:
  saludo replicado, cambio de idioma consistente y persistencia del idioma entre turnos/sesiones.

## 3. Estado

- ✅ Implementado, desplegado; tests verdes. Bitácora **038**.