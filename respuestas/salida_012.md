<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_012.md`  
> **Objetivo:** 012 · Respuesta — puesta en marcha de los servicios t2c2-* y verificación end-to-end (consultas reales)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1857 · **Última modificación:** 20261117 1857
<!--/encabezado-grupo-->

# 012 · Puesta en marcha + verificación end-to-end

**Prompt:** [`../prompts_ejecutados/prompt_012.md`](../prompts_ejecutados/prompt_012.md)

> ⚠️ **Método:** servicios activados por el usuario (sudo); verificación hecha por mí desde la VPS (web6).

---

## 1. Servicios activos

Se instalaron y habilitaron los 5 servicios (`systemctl enable --now`):

```
t2c2-langgraph  active     (:2025, 8 agentes A2A — OK en ~2 s)
t2c2-fichas     active     (vigilante de agent cards)
t2c2-api        active     (:8796, gateway FastAPI + API_KEY)
t2c2-web        active     (:8797, BFF chat + voz)
t2c2-monitor    active     (:8798, backoffice)
```

## 2. Seguridad del gateway (evidencia 200/401)

```
GET /salud                 -> {"estado":"ok"}
GET /agentes  SIN API_KEY  -> 401
GET /agentes  CON API_KEY  -> 200
```

## 3. Consultas REALES end-to-end (FastAPI → coordinador → agente local → herramienta)

**Consulta 1 — "¿Qué clima hará hoy en Valdivia?"**
- `elegido`: **Agente de Meteorología**
- `ruta`: `guardia_entrada → supervisor → agente_local → guardia_salida`
- respuesta (datos **REALES** de Open-Meteo):
  > [Agente de Meteorología] Valdivia hoy — actual **16,5 °C**, mín **12,5**, máx **18,7**,
  > **Chubascos débiles**, precipitación **8,4 mm**.

**Consulta 2 — "¿Qué agentes hay y qué puede hacer cada uno?"**
- `elegido`: **Agente Administrador**
- `ruta`: `guardia_entrada → supervisor → agente_local → guardia_salida`
- respuesta: saludo en español + listado de los agentes y sus funciones.

→ Queda demostrada la cadena completa: **gateway FastAPI (API_KEY) → coordinador (Gemini decide la
ruta) → agente local vía A2A (langgraph :2025) → herramienta real → respuesta formateada en español**,
con ruteo correcto por tipo de consulta (meteorología vs meta/administrador).

## 4. Estado

- ✅ **Sistema en marcha y verificado end-to-end** en la VPS (local, 127.0.0.1).
- ✅ Correo real ya verificado (registro 011); Gemini válido.
- ⏳ **Falta solo la publicación con proxy** (ISPConfig) de `tarea2curso2.etmk.cl` (→ :8797) y
  `monitortarea2curso2.etmk.cl` (→ :8798) + Let's Encrypt + force-HTTPS, para el acceso por web público.

## 5. Próximos pasos

1. **Proxies** de los dos subdominios (directivas Apache ya entregadas).
2. **Evidencias de rúbrica** por la web: chat, voz, correo, 200/401 en el monitor (capturas).
