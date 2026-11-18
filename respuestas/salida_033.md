<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_033.md`  
> **Objetivo:** 033 · Respuesta — diagrama arquitectónico técnico vivo + mantención  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1300 · **Última modificación:** 20261118 1300
<!--/encabezado-grupo-->

# 033 · Respuesta — Arquitectura técnica viva

**Prompt:** [`../prompts_ejecutados/prompt_033.md`](../prompts_ejecutados/prompt_033.md)

---

## 1. Qué se entregó

- **`docs/ARQUITECTURA.md`**: diagrama Mermaid técnico (componentes, flujos y fuentes de datos) +
  tablas de componentes/agentes/externos + seguridad + despliegue.
- **Prompt de mantención** embebido: regla para que el diagrama se actualice **en el mismo cambio** que
  toca agentes, herramientas externas, servicios, fuentes o flujos; con fidelidad al código y Mermaid
  validado.
- **`AGENTS.md`** regla 9 y enlace desde **`README.md`**: la mantención queda como parte del flujo.

## 2. Qué muestra el diagrama

Clientes (chat+voz, monitor) → publicación proxy/HTTPS → servicios systemd (`t2c2-web` BFF,
`t2c2-monitor`, `t2c2-api` FastAPI+API_KEY, coordinador supervisor, `t2c2-langgraph` con los 8 agentes,
`t2c2-fichas`) → persistencia (Memoria/Config/Recetas/Usuarios SQLite + Redis) → externos (Gemini, Redis
cloud, Open-Meteo, UniProt, open.er-api, Wikipedia, SMTP). Incluye qué agente usa cada fuente real.

## 3. Mantención

Se actualiza con cada registro futuro. "Última revisión de arquitectura" se mueve con cada cambio
estructural. Validación Mermaid: 7 subgraph / 7 end, sin `end` como id, corchetes balanceados.

## 4. Estado

- ✅ Documento vivo creado, enlazado y versionado. Bitácora **033**.
