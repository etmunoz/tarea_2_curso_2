<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_020.md`  
> **Objetivo:** 020 · Respuesta — chat e historial por usuario; tutorial para usuarios nuevos  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2143 · **Última modificación:** 20261117 2143
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

## 2. Estado

- ✅ Código publicado en web6; compila.
- ⏳ Pendiente: **reiniciar `t2c2-web`** (sudo) y entrar como un usuario nuevo para ver el tutorial.
