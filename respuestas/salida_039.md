<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_039.md`  
> **Objetivo:** 039 · Respuesta — confirmación de nombre + health check post-hardening  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1205 · **Última modificación:** 20261119 1205
<!--/encabezado-grupo-->

# 039 · Respuesta — Confirmación de nombre + health check

**Prompt:** [`../prompts_ejecutados/prompt_039.md`](../prompts_ejecutados/prompt_039.md)

---

## 1. Confirmación de nombre

El administrador usa el login como nombre tentativo pero lo **confirma la primera vez** y recién lo
guarda; si ya hay `nombre` en el perfil, no pregunta. Solo cambio de prompt.

**Verificado en vivo** (usuario `fabio`, sin nombre guardado): saludo → *"¡Buenas!… (Por cierto, Fabio,
¿te llamo así o prefieres otro nombre?)"* (confirma, no asume); «sí, así está bien» → *"Perfecto,
guardado"* → `perfil = {nombre:'Fabio'}`. Perfil de prueba limpiado luego.

## 2. Health check post-hardening (todo OK)

| Capa | Resultado |
|---|---|
| Servicios | `t2c2-langgraph/-fichas/-api/-web/-monitor` → **active** (5/5) |
| Puertos internos | langgraph **200**, api **200**, web **200**, monitor **401** (protegido) |
| Público HTTPS | login **200**, monitor **401**, `/api/consulta` sin cookie **401**, **HSTS** presente |
| Egress externo | Gemini, Open-Meteo, UniProt, er-api, Wikipedia → **200**; **Redis ping True** |
| End-to-end (6 agentes) | meteo, bio, reiki, viajes, cocina, admin → **OK** |

**Conclusión:** el hardening **no bloqueó** puertos internos ni el egress; el sistema está operativo.
Evidencia: `evidencias/EVIDENCIAS.md` (Anexo 12).

## 3. Estado

- ✅ Health check OK. Cambio de nombre desplegado (requiere `restart t2c2-langgraph` para verificar en
  vivo). Bitácora **039**.
