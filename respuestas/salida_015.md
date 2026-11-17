<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_015.md`  
> **Objetivo:** 015 · Respuesta — chat rediseñado con el estilo del Taller 1 + auto-arranque confirmado  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1935 · **Última modificación:** 20261117 1935
<!--/encabezado-grupo-->

# 015 · Rediseño del chat (estilo Taller 1) + auto-arranque

**Prompt:** [`../prompts_ejecutados/prompt_015.md`](../prompts_ejecutados/prompt_015.md)

> ⚠️ **Método:** publicado en la VPS (web6). El diseño se aplica al **reiniciar `t2c2-web`**.

---

## 1. Rediseño del chat

Se reemplazó la `PAGINA` del BFF (`src/canales/web.py`) por el **diseño del Taller 1**, adaptado a T2:

- **Fondo *aurora*** animado, tipografías Inter + JetBrains Mono, **tema claro/oscuro** persistente.
- **Dos tarjetas:** **💬 Chat** (burbujas con avatar, indicador "escribiendo") y **🧭 Ruteo del
  coordinador** (agente elegido + **motivo**, antecedentes con el **origen**, y los **pasos de la ruta**
  con íconos).
- **Chips** de agentes (se cargan de `/api/agentes`), con `meta()` actualizado a los nombres de T2
  (Machine Learning, ML Bioinformática, Bioinformática, Reiki, Cocina Chilena, Meteorología, Viajes,
  Administrador).
- Botones: **🔄 nueva conversación**, **🎤 voz** (enlaza a `/voz`), **🌙/☀️ tema**, **🚪 salir**.
- **Clave de arquitectura:** el frontend habla con **`/api/consulta`** del BFF (que agrega la `API_KEY`
  server-side) — el navegador nunca ve la clave. Se quitaron los modales del T1 que no aplican
  (configurar URLs de agentes remotos; en T2 todo es local).

También se añadió **`motivo`** a la respuesta de `POST /consulta` (gateway) para el panel de ruteo.

`web.py` y `app.py` **compilan**.

## 2. Auto-arranque en reboot (como el T1) ✅

Verificado `systemctl is-enabled` de los 5 servicios → **todos `enabled`**:
```
t2c2-langgraph  enabled
t2c2-fichas     enabled
t2c2-api        enabled
t2c2-web        enabled
t2c2-monitor    enabled
```
→ Se **levantan solos** si la VPS se reinicia (los symlinks en `multi-user.target.wants` se crearon al
hacer `systemctl enable --now`). No requiere acción adicional.

## 3. Pendiente (acción del usuario)

- **Reiniciar** para aplicar el nuevo diseño y el `motivo` (requiere sudo; web6 no puede):
  ```bash
  sudo systemctl restart t2c2-api t2c2-web
  ```
- Luego verifico desde la VPS que la nueva UI se sirve y que una consulta muestra el ruteo.
