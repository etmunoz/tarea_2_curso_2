<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_016.md`  
> **Objetivo:** 016 · Respuesta — chat con ruteo por turno, ver ruteo y enviar por correo (paridad con el Taller 1)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1944 · **Última modificación:** 20261117 1944
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

## 4. Verificación

`app.py` y `web.py` **compilan**. La verificación funcional (ruta por turno y endpoints de correo) se
hace tras el reinicio:
```bash
sudo systemctl restart t2c2-api t2c2-web
```
→ Se comprobará: dos consultas en la misma sesión devuelven **cada una su ruta corta** (no acumulada), y
`/api/enviar` despacha a un destinatario de la allowlist.

## 5. Estado

- ✅ Código publicado en web6; compila. Bitácora **000–016** en el repo.
- ⏳ Pendiente: reinicio (sudo) + verificación funcional.
