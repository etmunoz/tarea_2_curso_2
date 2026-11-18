<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_025.md`  
> **Objetivo:** 025 · Revisar y actualizar la documentación de arquitectura al estado actual  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2305 · **Última modificación:** 20261117 2305
<!--/encabezado-grupo-->

# 025 · Documentación de arquitectura al día

**Pedido del usuario (verbatim):**

> «revisa la documentación de la arquitectura actual, para que la actualices como corresponda y el
> detalle correcto»

**Contexto:** tras la migración del RAG a Redis (registro 024) y los cambios acumulados (multiusuario,
almacén de config, monitor activo), varios docs quedaron desactualizados o heredados del Taller 1.

**Alcance:**
1. **`README.md`** — sección *Arquitectura* reescrita al estado real: coordinador supervisor con
   guardias y ruteo por turno, **multiusuario** (sesión/PBKDF2/cookie segura/anti-fuerza-bruta),
   **RAG en Redis cloud**, **almacén de config**, monitor con eventos/cuota/`/config`, correo a
   allowlist. Corrección de variables (`WEB_USUARIOS`/`WEB_ADMIN`/`CLAVE_INICIAL` en vez de
   `WEB_USER`/`WEB_PASS`).
2. **`deploy/README-T2.md`** — monitor **activo** (no pendiente), variables de login nuevas,
   `chown root:client1`, login **por sesión** (no Basic Auth), alternativa por almacén de config,
   recordatorio de reinicio de `t2c2-langgraph` tras el deploy del RAG.
3. **`AGENTS.md`** — reescrito: estaba íntegramente heredado del Taller 1 (`agente-viajes-a2a`,
   `src/consumidor`, `src/swarm`, OpenCode). Ahora describe la arquitectura, estructura y reglas reales
   de T2.

**Restricción:** solo documentación; sin cambios de código ni de comportamiento.
