<!--encabezado-grupo-->
> **Archivo:** `respuestas/salida_018.md`  
> **Objetivo:** 018 · Respuesta — multiusuario con login por sesión, autogestión de correo, admin y eventos al monitor  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 2102 · **Última modificación:** 20261117 2102
<!--/encabezado-grupo-->

# 018 · Respuesta — Multiusuario + sesiones + autogestión de correo

**Prompt:** [`../prompts_ejecutados/prompt_018.md`](../prompts_ejecutados/prompt_018.md)

> ⚠️ **Método:** publicado en la VPS (web6). Se aplica al **reiniciar `t2c2-api` y `t2c2-web`**.

---

## 1. Almacén de usuarios — `src/config/usuarios.py`

SQLite con claves **hasheadas** (PBKDF2-HMAC-SHA256, 120k iteraciones, salt por usuario). Funciones:
`crear`, `seed` (crea los usuarios con la clave inicial única y `debe_cambiar=1` si la tabla está vacía),
`verificar` (tiempo constante), `debe_cambiar`, `es_admin`, `cambiar_clave` (quita el flag),
`resetear_clave` (admin; vuelve a exigir cambio), `listar`. **Probado** (seed, verificar, cambio, reset,
roles).

## 2. Login por sesión — `src/canales/web.py` (reemplaza el Basic Auth)

- **`/login`** (form) → valida contra el almacén; crea sesión y **cookie `t2sid`**; redirige a `/` o a
  `/cambiar-clave` si corresponde.
- **`/cambiar-clave`**: **obligatorio** al primer ingreso (`debe_cambiar=1`); el usuario define su clave.
- **`/logout`**: cierra la sesión y limpia la cookie.
- **`/usuarios`** (solo admin, **ezequiel**): tabla de usuarios + **resetear** la clave de cualquiera.
- **Seguridad:** cookie **HttpOnly + SameSite=Lax + Secure**; **caducidad 8 h**; token
  `secrets.token_urlsafe`; **anti-fuerza-bruta** (máx 6 intentos / 5 min + espera). Las claves nunca
  llegan al navegador.

## 3. Flujo separado por usuario

El BFF añade el header **`X-Usuario`** a las llamadas al gateway; `POST /consulta` **namespacea el hilo**
(`usuario:sesion`) → cada persona tiene su propia memoria/conversación, visible por separado.

## 4. Autogestión de correo (§7)

- Gateway: `GET /mi-correo` (correo del usuario), `POST /registrar-correo` (lo guarda en la allowlist con
  `nombre=usuario`). BFF proxies `/api/mi-correo`, `/api/registrar-correo`.
- Frontend: al entrar, si el usuario **no tiene correo**, la UI le da la **bienvenida con instrucciones**
  y un campo para **registrar su email**; si ya lo tiene, lo muestra.

## 5. Eventos de usuario al monitor

- `src/memoria/bd.py`: tabla **`eventos`** + `registrar_evento` / `eventos`.
- El BFF registra **login, logout, cambio_clave y reset_admin**.
- El **monitor** muestra la sección **"Eventos de usuario (sesiones)"** (fecha, usuario, evento).

## 6. Entrega de credenciales

`~/usuarios_setup.txt` (chmod 600) con: las líneas para `/etc/t2c2.env`
(`WEB_USUARIOS=ezequiel,gustavo,fabio,cristobal,jose`, `WEB_ADMIN=ezequiel`, `CLAVE_INICIAL=<única>`) y el
listado de usuarios + la clave inicial a repartir. La clave inicial es **única** y **cada uno la cambia
al primer ingreso**.

## 7. Estado — VERIFICADO EN PRODUCCIÓN ✅

Tras agregar `WEB_USUARIOS`/`WEB_ADMIN`/`CLAVE_INICIAL` a `/etc/t2c2.env` y reiniciar, verificado desde
la VPS contra la URL pública:

```
usuarios sembrados: cristobal(user), ezequiel(admin), fabio(user), gustavo(user), jose(user) — debe_cambiar=1
GET /login               -> 200
GET / sin sesión         -> 302 -> /login
POST /login clave MALA   -> 401                      (rechazo)
POST /login clave OK     -> 302 -> /cambiar-clave    (fuerza el cambio obligatorio)
GET / con sesión         -> 302 -> /cambiar-clave
GET /cambiar-clave       -> "Hola, gustavo"
GET /api/yo (pendiente)  -> 409                       (bloqueado hasta cambiar la clave)
eventos: {usuario: gustavo, evento: login}           (registrado)
monitor: sección "Eventos de usuario" presente
```

→ **Login por sesión, rechazo de credenciales, cambio obligatorio, gating y eventos al monitor
funcionan.** (No se alteró la clave de ningún usuario real: solo se probó el flujo.)
