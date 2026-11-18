<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_020.md`  
> **Objetivo:** 020 · Chat e historial POR USUARIO (cada login arranca con su propio hilo; tutorial para usuarios nuevos)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2143 · **Última modificación:** 20261117 2143
<!--/encabezado-grupo-->

# 020 · Chat/historial por usuario + tutorial

**Pedido del usuario (verbatim):**

> «entré con mi usuario ezequiel y no tenía una sesión vacía, estaba lo que estaba antes y no me dio el
> tutorial inicial.»

**Causa:** el historial y el hilo del chat se guardaban **por navegador** (`sessionStorage` con una clave
global `t2_thread` / `t2_hist_<thread>`), no **por usuario**. Por eso al entrar ezequiel veía la
conversación previa (de pruebas anteriores) y, al no estar vacía, no se mostraba el tutorial de
bienvenida.

**Alcance:** hacer el chat **por usuario**:
- El hilo y el historial se guardan con claves **por usuario** (`t2_thread_<usuario>`,
  `t2_hist_<usuario>_<thread>`).
- Al cargar, se obtiene el usuario de la sesión (`/api/yo`) y se **inicializa su propio hilo**
  (restaura su conversación o, si es nueva, queda vacía → **muestra el tutorial** + registro de correo).
- "Nueva conversación" crea un hilo nuevo del usuario actual.

**Restricción:** solo `src/canales/web.py`; reinicio de `t2c2-web` por el usuario (sudo).
