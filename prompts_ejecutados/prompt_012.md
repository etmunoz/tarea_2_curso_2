<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_012.md`  
> **Objetivo:** 012 · Activar los servicios t2c2-* y verificar el sistema end-to-end (consultas reales)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1857 · **Última modificación:** 20261117 1857
<!--/encabezado-grupo-->

# 012 · Activación de servicios + verificación end-to-end

**Pedido del usuario (verbatim):**

> «nos falta configurar los proxy»
> (y, tras encender los servicios por sudo) la verificación del sistema en marcha.
> «recuerda dejar todo esto en prompts y salidas, no puede quedar nada indocumentado»

**Contexto:** con `/etc/t2c2.env` completo (Gemini + SMTP verificados en el registro 011), el usuario
instaló y habilitó los servicios con `administrator`:

```bash
sudo sh -c 'cp /var/www/clients/client1/web6/home/etmkuseretmk2/tarea_2_curso_2/deploy/systemd/t2c2-*.service /etc/systemd/system/'
sudo systemctl daemon-reload
sudo systemctl enable --now t2c2-langgraph t2c2-fichas t2c2-api t2c2-web t2c2-monitor
```
*(Nota: el `cd` al home de web6 fallaba por permisos; la copia se hizo con `sudo sh -c` para que root
expandiera el glob y leyera el home de web6.)*

**Alcance de este registro:** verificar desde la VPS que los 5 servicios quedaron `active`, que el
gateway responde (`/salud`, 200/401), y ejecutar **consultas reales** para comprobar el ruteo y las
respuestas end-to-end (meteorología real y administrador). Dejar toda la evidencia documentada.

**Restricción:** la publicación con proxy (ISPConfig) queda para el usuario (sudo); aquí solo se activa
y verifica el backend local (127.0.0.1).
