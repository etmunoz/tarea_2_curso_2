<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_018.md`  
> **Objetivo:** 018 · Multiusuario con login por sesión (clave única + cambio obligatorio + admin) + flujo por usuario + autogestión de correo  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2102 · **Última modificación:** 20261117 2102
<!--/encabezado-grupo-->

# 018 · Multiusuario + sesiones + autogestión de correo

**Pedido del usuario (verbatim):**

> «hacer un ambiente separado por usuario, para que yo y mis compañeros podamos ver por separado y tener
> nuestro propio flujo … dar usuarios y claves a los profes Jose y Cristobal.»
> «que el mismo agente detecte si no tiene registrado un correo le solicite el registro y le ayude a
> guardar el mail … como también le de unas instrucciones preliminares.»
> «tener usuarios para ingresar que se llamen ezequiel, gustavo, fabio, cristobal y jose.»
> «que la clave sea única pero le pida al usuario cambiarla a la entrada; el usuario administrador puede
> cambiarle la clave a todos.»
> «ojo con todo lo que significa la seguridad de las sesiones, su caducidad, seguridad, etc.»
> «los usuarios que se conectan y los eventos de cambio de clave y su desconexión, también debe ir al
> monitor.»
> «me das el listado de usuarios y su clave inicial.»

**Alcance:**
1. **Login por sesión** en el BFF (reemplaza el Basic Auth único): usuarios **ezequiel, gustavo, fabio,
   cristobal, jose**; `ezequiel` = **admin**.
2. **Almacén de usuarios** (`src/config/usuarios.py`, SQLite): claves **hasheadas** (PBKDF2-HMAC-SHA256
   + salt), **clave inicial única** y **cambio obligatorio** al primer ingreso; **reset por admin**.
3. **Flujo separado por usuario:** el BFF pasa `X-Usuario` al gateway, que **namespacea el hilo** de la
   conversación por usuario (`usuario:sesion`) → memoria/monitor separados por persona.
4. **Autogestión de correo (§7):** al entrar, si el usuario no tiene correo registrado, la UI le da la
   **bienvenida con instrucciones** y le ayuda a **registrar su email** (queda en la allowlist asociado
   a su usuario). Endpoints `GET /mi-correo`, `POST /registrar-correo`.
5. **Panel de admin** (`/usuarios`): ezequiel puede **resetear la clave** de cualquiera.
6. **Seguridad de sesiones:** cookie **HttpOnly + SameSite=Lax + Secure**, **caducidad 8 h**, token
   aleatorio fuerte; **anti-fuerza-bruta** en el login (límite de intentos + espera). Claves nunca en el
   navegador ni en el repo.
7. **Eventos de usuario al monitor:** registrar **login, logout, cambio de clave y reset** (tabla
   `eventos` en memoria) y mostrarlos en el panel del monitor.

**Entrega al usuario:** `~/usuarios_setup.txt` (chmod 600) con las líneas de `/etc/t2c2.env`
(`WEB_USUARIOS`, `WEB_ADMIN`, `CLAVE_INICIAL`) y el listado de usuarios + la clave inicial a repartir.

**Restricción:** el reinicio de servicios lo hace el usuario (sudo); web6 no puede.
