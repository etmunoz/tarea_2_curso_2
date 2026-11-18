<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_033.md`  
> **Objetivo:** 033 · Diagrama arquitectónico técnico vivo + protocolo de mantención  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261118 1300 · **Última modificación:** 20261118 1300
<!--/encabezado-grupo-->

# 033 · Arquitectura técnica (documento vivo)

**Pedido del usuario (verbatim):**

> «un prompt especial para que hagas un diagrama arquitectónico técnico de la app, para que se vea la
> complejidad actual de la app. Y lo mantienes en el tiempo con las evoluciones que hagamos.»

**Alcance:**
1. **`docs/ARQUITECTURA.md`** (nuevo): documento vivo con
   - **Prompt de mantención** (para Claude): regla de actualizar el diagrama en el mismo cambio, con
     fidelidad al código y validación de Mermaid.
   - **Diagrama Mermaid técnico** (flowchart): clientes → publicación proxy/HTTPS → servicios systemd
     (BFF, monitor, gateway FastAPI, coordinador supervisor, 8 agentes A2A, vigilante de fichas) →
     persistencia (SQLite + Redis) → servicios externos (Gemini, Redis cloud, Open-Meteo, UniProt,
     open.er-api, Wikipedia, SMTP), con las aristas de qué agente usa qué fuente.
   - Tablas de **componentes**, **agentes y fuentes**, **externos**, seguridad y despliegue.
2. **`AGENTS.md`** regla 9: mantener `docs/ARQUITECTURA.md` al día en cada evolución.
3. **`README.md`**: enlace al diagrama técnico.

**Restricción:** el diagrama describe lo que está en el código (no aspiracional); Mermaid validado
(7 subgraph / 7 end, sin `end` como id). Se mantiene con cada registro siguiente.
