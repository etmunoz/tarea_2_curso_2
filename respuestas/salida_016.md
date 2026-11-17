<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_016.md`  
> **Objetivo:** 016 · Respuesta — chat con ruteo por turno, ver ruteo y enviar por correo (paridad con el Taller 1)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1944 · **Última modificación:** 20261117 1948
<!--/encabezado-grupo-->

# 016 · Funcionalidades del chat (ruteo por turno + correo)

**Prompt:** [`../prompts_ejecutados/prompt_016.md`](../prompts_ejecutados/prompt_016.md)

> ⚠️ **Método:** publicado en la VPS (web6). Se aplica al **reiniciar `t2c2-api` y `t2c2-web`**.

---

## 1. Ruteo por turno (bug de acumulación) — `src/api/app.py`

El panel derecho mostraba la ruta de **toda** la conversación porque el estado del coordinador
(checkpointer `InMemorySaver` por `thread_id`, con `ruta: Annotated[list, operator.add]`) **acumula**
los pasos entre turnos. Arreglo en `POST /consulta`:

```python
st = _coordinador().get_state(cfg)
prev = len((getattr(st, "values", {}) or {}).get("ruta", []))
res = _coordinador().invoke({...}, cfg)
ruta = (res.get("ruta") or [])[prev:]   # SOLO los pasos de este turno
```

Los demás campos (`elegido`, `motivo`, `origen`, `respuesta`) son plano/sobre-escritos, no acumulan.

## 2. Enviar por correo (re-incorporado) — gateway + BFF + frontend

- **Gateway (`app.py`):** `GET /destinatarios` y `GET /correo` (allowlist/estado) y `POST /enviar`
  (despacho), todos protegidos por API_KEY. El envío usa `src/canales/correo.enviar(...)` → allowlist +
  ruta + gráfico del grafo.
- **BFF (`web.py`):** proxies `/api/destinatarios`, `/api/correo`, `/api/enviar` (añaden la API_KEY
  server-side).
- **Frontend (`web.py`, PAGINA):** modal de correo (Para desde la allowlist, Asunto, Mensaje) + botón
  **✉️ Enviar por correo** en cada respuesta (visible solo si el correo está configurado); el mensaje
  del turno incluye su **pregunta, agente y ruta**.

## 3. Ver ruteo (re-ver)

Cada respuesta mantiene su botón **🧭 Ver ruteo** que re-pinta el ruteo de **ese** turno (ahora correcto
por #1).

## 4. Verificación (tras reinicio) — ✅

`app.py` y `web.py` compilan. Probado en vivo contra el gateway (servicios `active`):

```
CONSULTA 1 (sesión S)  -> Agente de Meteorología | ruta(4): guardia_entrada, supervisor, agente_local, guardia_salida
CONSULTA 2 (MISMA sesión S) -> Agente Administrador | ruta(4): guardia_entrada, supervisor, agente_local, guardia_salida
```
→ **La ruta ya NO se acumula**: el segundo turno devuelve 4 pasos (no 8). Bug resuelto.

```
GET /correo  -> {configurado: True, destinatarios: ['etmunoz@gmail.com']}
POST /enviar a nadie@noexiste.xyz -> {ok:false, error:"destinatario no está en la allowlist…"}
```
→ Endpoints de correo operativos; allowlist gatillando (no envía fuera de la lista).

## 5. Estado

- ✅ **Verificado en producción:** ruteo por turno, estado de correo y allowlist del envío.
- ✅ Chat con el diseño del T1 + ver ruteo + enviar por correo (paridad con el Taller 1).
- ✅ Bitácora **000–016** en el repo.
