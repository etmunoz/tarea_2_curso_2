<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_065.md`
> **Objetivo:** 065 · Puesta al día integral de la documentación para presentación a profesores
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz
> **Creación:** 20261123 1730 · **Última modificación:** 20261123 1730
<!--/encabezado-grupo-->

# 065 · Documentación al día para presentar a profesores

**Pedido del usuario (verbatim):**

> «como prompt: actualiza todo lo que tengas que actualizar, readme, bitacora, manuales, documentos,
> arquitectura, dibujos, etc. Para que tengamos ahora todo actualizado como se debe para mostrar a los
> profesores.»

**Objetivo:** dejar TODA la documentación del repo coherente y veraz respecto del estado actual del
sistema, lista para una revisión académica. Fidelidad: los documentos describen lo que está en el
código, no lo aspiracional.

**Estado actual del sistema que la documentación debe reflejar:**
- **9 agentes** A2A (meteorologia, reiki, bioinformatica, mlbioinformatica, machinelearning,
  cocinachilena, viajes, administrador, **meteo_mcp**).
- **meteo_mcp** (PR #1 de Gustavo): MCP de Meteosource con respaldo keyless Open-Meteo
  ("Clima resiliente en dos niveles") — registro 063.
- **PostgresSaver** opcional en el coordinador (memoria durable del hilo; fallback a InMemorySaver) —
  registro 064.
- RAG de Reiki en **Redis cloud** (RediSearch); recepción personalizada (administrador); guardrails
  anti-ofuscación; despliegue por `deploy/deploy_local_a_vps.sh` + servicios systemd `t2c2-*`.

**Alcance (revisar y actualizar donde haga falta):**
1. `README.md` — visión, agentes, arranque, estado.
2. `AGENTS.md` — catálogo y diagramas.
3. `docs/ARQUITECTURA.md` — diagrama vivo (ya en 064; verificar consistencia).
4. `docs/MEJORAS_FUTURAS.md` — backlog (quitar lo ya hecho: Postgres; dejar hardening pendiente).
5. `deploy/README-T2.md` y manuales de despliegue — variables (PG_DSN), pasos.
6. Cualquier manual/documento adicional en `docs/`.
7. Diagramas Mermaid: validar sintaxis y que reflejen 9 agentes + meteo_mcp + Postgres.

**Entregable:** documentación consistente + bitácora 065 (prompt/salida) + Anexo 16 de evidencias.
