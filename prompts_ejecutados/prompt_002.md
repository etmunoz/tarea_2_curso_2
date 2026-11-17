<!--encabezado-grupo-->
> **Archivo:** `prompts_ejecutados/prompt_002.md`  
> **Objetivo:** 002 · Publicar la Tarea 2 directo en la VPS (espacio nuevo, sin pisar otros proyectos): paso 2 (copiar base T1 + renombrar agentes locales), fichas de identidad funcional y agente_administrador  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261117 1508 · **Última modificación:** 20261117 1508
<!--/encabezado-grupo-->

# 002 · Publicar T2 directo en la VPS + renombre + fichas + agente_administrador

**Pedido del usuario (consolidado de esta sesión, verbatim de los mensajes clave):**

> «sigue con lo definido en el prompt. No repliques la repo en la VPS sino que anda publicando
> directamente tú en la VPS, con cuidado de no pisar nada de los otros proyectos que están en paralelo.»
>
> «acuérdate que mejor no utilizar web1 quizás mejor otro, ya que ese está con otro proyecto, así como
> con lucecita se hizo web5»
>
> «Dale, sigue con fichas y agente_administrador, y registra prompt_002/salida_002»

**Alcance de este registro:**

1. Crear un **espacio nuevo y aislado** en la VPS para la Tarea 2 (no web1/T1 ni web5/lucecita) y
   **publicar directo ahí** (no replicar el repo de GitHub, que solo tiene documentación).
2. Ejecutar el **paso 2** del `prompt_000.md`: copiar la base del T1 y **renombrar los 7 agentes a
   `agente_<funcionalidad>` LOCALES** (dirs + `langgraph.json` + `fichas.py` + imports + tests).
3. Actualizar **`fichas.py`** a la **identidad funcional** de cada agente (§4 del prompt_000).
4. Crear el **8º agente, `agente_administrador`** (recepción/orientación) y registrarlo en
   `langgraph.json`.

**Restricciones aplicadas:** no pisar los proyectos en paralelo; a web1 solo lectura; sin `sudo`; no
dejar servicios pesados corriendo (RAM ajustada, sin swap).
