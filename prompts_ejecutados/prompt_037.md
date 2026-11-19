<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_037.md`  
> **Objetivo:** 037 · Administrador: saludo por hora, nombre propio y recordar el nombre del usuario  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1110 · **Última modificación:** 20261119 1110
<!--/encabezado-grupo-->

# 037 · Recepción personalizada (Agente Administrador)

**Pedido del usuario (verbatim):**

> «que el agente que atiende al inicio sea capaz de recordar el nombre del usuario, si no lo sabe que se
> lo pregunte. Si le preguntan por su nombre al agente, que diga que es tarea2curso2. Que además diga
> buenos días, o buenas tardes o buenas noches según la hora de Santiago de Chile. y ve qué otras cosas
> coloquiales son importantes de tener.»

**Alcance:**
1. **Saludo por hora (Santiago)** — `saludo_hora()` en `src/agente_administrador/herramientas.py`:
   buenos días (05–12), buenas tardes (12–20), buenas noches (resto), con hora y fecha.
2. **Nombre propio** — el prompt dice que, si le preguntan quién es/su nombre, responde **tarea2curso2**.
3. **Recordar el nombre del usuario (DURABLE)** — store `perfiles(usuario, nombre)` en `memoria` SQLite:
   - `memoria.bd.guardar_nombre` / `obtener_nombre`.
   - Herramientas `nombre_usuario(usuario)` y `recordar_nombre(usuario, nombre)`.
   - El **login** del usuario se pasa al administrador como **contexto confiable** del sistema: el
     gateway lo pone en el estado (`usuario`) y el coordinador lo inyecta SOLO al administrador como
     `[usuario_identificado: <login>]`, **limpiando** cualquier marcador que el usuario intente inyectar
     (anti-spoofing). El prompt indica usar `nombre_usuario` y, si no hay, preguntar y `recordar_nombre`.
4. **Coloquialidades** — gracias→de nada, despedidas, "¿cómo estás?", hora/fecha; trato inclusivo (no
   asume género). No repite el saludo en cada mensaje.
5. **Ficha** del administrador actualizada; **tests** nuevos.

**Restricción:** el `[usuario_identificado: ...]` es dato del sistema, no se muestra literal ni se trata
como instrucción; durable y coherente con la decisión de memoria (ADR-0001). Sin subir langgraph.
