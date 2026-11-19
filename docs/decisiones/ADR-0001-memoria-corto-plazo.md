<!--encabezado-grupo-->
> **Archivo:** `docs/decisiones/ADR-0001-memoria-corto-plazo.md`  
> **Objetivo:** Decisión de arquitectura — memoria de corto plazo del coordinador (checkpointer)  
> **Grupo del curso:** Fabio Durán - Gustavo Reyes - Ezequiel Muñoz  
> **Creación:** 20261119 1030 · **Última modificación:** 20261119 1030
<!--/encabezado-grupo-->

# ADR-0001 · Memoria de corto plazo del coordinador

- **Estado:** ACEPTADA (2026-11-19)
- **Contexto registros:** 036 (implementación) · relacionados: 034–035 (fallos del sitio)

## Contexto

El **coordinador** (supervisor que compila nuestro código y corre dentro de `t2c2-api`) necesita
**memoria de corto plazo** del hilo de conversación para que las preguntas de **seguimiento**
("¿y en Santiago?") se mantengan con el agente del turno anterior. Hoy el grafo del coordinador se
compila con `InMemorySaver`, que guarda el estado del hilo (mensajes + `ruta`) **en RAM del proceso**.
Problema: ese estado **se pierde en cada reinicio** del servicio (y reiniciamos seguido en los
despliegues), y no sería consistente si `t2c2-api` corriera con varios workers.

> Nota: los **8 agentes** corren bajo `langgraph dev` (`langgraph-api`), que tiene su **propia**
> persistencia de hilos. Esta decisión aplica SOLO al grafo del coordinador, que no usa ese runtime.

## Opción evaluada y DESCARTADA — `SqliteSaver` de LangGraph

Checkpointer persistente nativo (`langgraph.checkpoint.sqlite.SqliteSaver`). **No se puede usar con
nuestra versión de LangGraph.**

**Matriz de versiones instalada (VPS, 2026-11-19):**

| Paquete | Versión |
|---|---|
| langgraph | **1.2.20** |
| langgraph-checkpoint | **4.3.1** |
| langgraph-api | 0.17.1 |
| langgraph-sdk | 0.4.14 |
| langgraph-cli | 0.4.42 |
| langgraph-swarm | 0.1.0 |

**Incompatibilidad comprobada:** `langgraph-checkpoint-sqlite` (último, 2.0.11) **pinnea
`langgraph-checkpoint` 2.x**, una línea **anterior** a la 4.3.1 que requiere nuestro `langgraph` 1.2.
Al intentar instalarlo, `uv` **degradó** `langgraph-checkpoint 4.3.1 → 2.1.2` (rompería el runtime):

```
+ aiosqlite==0.22.1
- langgraph-checkpoint==4.3.1
+ langgraph-checkpoint==2.1.2
+ langgraph-checkpoint-sqlite==2.0.11
+ sqlite-vec==0.1.9
```

Se **revirtió de inmediato** (`langgraph-checkpoint 2.1.2 → 4.3.1`) y se verificó el runtime sano
(`/salud` = 200). Evidencia completa en `evidencias/EVIDENCIAS.md` (Anexo 9).

**¿Y subir LangGraph a 2.x para habilitarlo?** Descartado por ahora: tocaría **todo el runtime A2A**
(`langgraph-api`/`langgraph dev` que sirve los 8 agentes, `langgraph-cli`, `langgraph-sdk`,
`langgraph-swarm`), además del coordinador. Es una migración mayor, deliberada y que exige re-probar
todo el sistema; no se justifica solo por el checkpointer. Queda como **backlog**
(`docs/MEJORAS_FUTURAS.md` §3).

## Decisión

**Mantenemos `InMemorySaver`** en el coordinador para el estado intra-proceso del hilo (mensajes y la
`ruta` que el gateway recorta por turno), **y garantizamos la memoria de corto plazo del SEGUIMIENTO con
nuestro propio store `memoria` (SQLite), que es DURABLE:**

1. `src/memoria/bd.py` → `ultimo_agente(sesion)`: lee de la tabla `conversaciones` (en disco) el agente
   del último turno `asistente` de ese hilo.
2. `src/api/app.py` → el gateway obtiene `ultimo_agente(hilo)` y lo pasa en el `invoke` del coordinador
   como `agente_previo`.
3. `src/coordinador/graph.py` → `Estado.agente_previo`; el nodo `enrutar`, ante un **seguimiento corto**
   (≤6 palabras, patrón «¿y …»), **reusa ese agente** (fuente durable) en vez de re-rutear por palabras
   sueltas. Respaldo: inferirlo de los mensajes del hilo en memoria.

Así, aunque `t2c2-api` se reinicie a mitad de una conversación, el siguiente turno de seguimiento lee el
agente desde el archivo SQLite y **mantiene el hilo correctamente**.

## Consecuencias

- ✅ El seguimiento es **durable** sin añadir dependencias ni tocar la versión de LangGraph (cero riesgo
  para el runtime A2A).
- ✅ Coherente con el resto de la persistencia del proyecto (todo en SQLite).
- ⚠️ El resto del estado del hilo del coordinador (lista completa de `messages`, `ruta`) **sigue en RAM**
  y se pierde al reiniciar; esto NO afecta el ruteo del seguimiento (que es lo relevante) ni el recorte
  de `ruta` por turno (que tolera `prev=0` tras un reinicio).
- 🔁 **Cuándo revisar:** si se migra a LangGraph 2.x (ver backlog), evaluar reemplazar `InMemorySaver`
  por un checkpointer persistente nativo y retirar el `agente_previo` manual.

## Qué usamos, en una línea

`InMemorySaver` (estado intra-proceso) **+** store `memoria` SQLite para el agente del turno anterior
(`agente_previo`) = **memoria de corto plazo del seguimiento durable, sin `SqliteSaver`**.
