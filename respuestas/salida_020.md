<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_020.md`  
> **Objetivo:** 020 · Respuesta — chat e historial por usuario; tutorial para usuarios nuevos  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2143 · **Última modificación:** 20261117 2147
<!--/encabezado-grupo-->

# 020 · Respuesta — Chat/historial por usuario

**Prompt:** [`../prompts_ejecutados/prompt_020.md`](../prompts_ejecutados/prompt_020.md)

> ⚠️ **Método:** publicado en la VPS (web6). Se aplica al **reiniciar `t2c2-web`**.

---

## 1. Qué se arregló

En `src/canales/web.py` (PAGINA):

- El hilo y el historial pasan a **claves por usuario**: `t2_thread_<usuario>` y
  `t2_hist_<usuario>_<thread>` (antes eran globales por navegador → se mezclaba lo de todos).
- Nueva función **`iniciarUsuario(u)`**: fija el hilo del usuario (o crea uno nuevo), limpia el chat y
  **restaura su propia conversación**.
- **`onboarding()`** ahora, tras leer `/api/yo`, llama a `iniciarUsuario(usuario)` **antes** de decidir:
  si el usuario no tiene conversación propia → **muestra el tutorial de bienvenida** (+ registro de
  correo); si la tiene → la restaura.
- "🔄 Nueva conversación" crea un hilo nuevo del **usuario actual**.

Efecto: cada usuario (ezequiel, gustavo, …) entra a **su propio chat**; un usuario nuevo ve el **tutorial
inicial**, y ya no aparece la conversación de otra sesión.

`web.py` **compila**.

## 2. Verificación (tras reiniciar `t2c2-web`) — ✅

Probado con un **usuario de prueba temporal** (creado y eliminado, sin tocar usuarios reales):

```
t2c2-web active
POST /login (sin cambio obligatorio) -> 302 -> /
GET / con sesión                      -> 200
piezas en la página: iniciarUsuario, t2_thread_, t2_hist_, mdToHtml, onboarding, micbtn  (todas ✔)
GET /api/yo -> {"usuario": "_vtest", "admin": false}
```

→ La página del chat sirve con la lógica **por usuario** (hilo/historial propios), el render Markdown y
la bienvenida; la identidad viene de la sesión. Cada usuario entra a su propio chat; uno nuevo verá el
tutorial.

## 3. Estado

- ✅ **Verificado en producción.** Bitácora **000–020** en el repo.
