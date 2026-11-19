<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_037.md`  
> **Objetivo:** 037 · Respuesta — recepción personalizada del Agente Administrador  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1110 · **Última modificación:** 20261119 1110
<!--/encabezado-grupo-->

# 037 · Respuesta — Recepción personalizada

**Prompt:** [`../prompts_ejecutados/prompt_037.md`](../prompts_ejecutados/prompt_037.md)

---

## 1. Qué se hizo

- **`saludo_hora()`**: saludo según la hora de Santiago (buenos días/tardes/noches) + hora y fecha.
- **Nombre propio**: el administrador responde **tarea2curso2** si le preguntan quién es.
- **Recordar nombre (durable)**: tabla `perfiles` en `memoria` SQLite; herramientas `nombre_usuario` y
  `recordar_nombre`. El **login** llega al administrador como contexto confiable
  `[usuario_identificado: <login>]` (inyectado por el coordinador, con limpieza anti-spoofing).
- **Coloquialidades**: cortesías, despedidas, "¿cómo estás?", hora/fecha; trato inclusivo; no repite el
  saludo en cada mensaje.
- **Ficha** actualizada; **tests** nuevos (`test_agente_administrador.py`).

## 2. Plumbing (identidad → agente)

`gateway (x_usuario)` → `Estado.usuario` → `consultar` inyecta `[usuario_identificado: <login>]` **solo**
al `agente_administrador` (otros agentes reciben la pregunta tal cual). El nombre se guarda/lee por
`login` en el store `memoria` (durable, sobrevive reinicios), coherente con **ADR-0001**.

## 3. Verificación (local)

- `pytest tests/test_agente_administrador.py tests/test_tarea2.py` → **15 passed** (franja por hora,
  estructura de `saludo_hora`, guardar/obtener nombre).

## 4. Pendiente de activación

- `sudo systemctl restart t2c2-langgraph t2c2-api` (agente + coordinador). Verificación en vivo:
  saludo por hora, "¿cuál es tu nombre?" → tarea2curso2, y recordar un nombre entre turnos.

## 5. Estado

- ✅ Implementado, desplegado, ficha aplicada; tests verdes. Bitácora **037**.
