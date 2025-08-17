# Reflex UI Code History — Efemérides de programación y tecnología

Este proyecto es una aplicación web construida con Reflex (Python) que muestra efemérides diarias relacionadas con programación, tecnología y emprendimiento. La UI principal simula una terminal e incluye una breve “secuencia de arranque” estilo boot al ingresar a la página.


## Requisitos previos
- Python 3.12 o superior (según `pyproject.toml`)
- Un gestor de paquetes para Python, por ejemplo:
  - uv (recomendado) o
  - pip
- Acceso a internet para instalar dependencias

Dependencias clave (se instalan automáticamente):
- reflex (>= 0.8.6)
- sqlalchemy (>= 2.0)
- pydantic-settings (>= 2.2)
- openai (>= 1.30) [opcional, para generación con IA]

La base de datos por defecto es SQLite y se crea en `app.db` en la raíz del proyecto.


## Instalación

Puedes elegir entre uv o pip. A continuación, se muestran ambos flujos.

### Opción A: usando uv (recomendado)
1) Crear y activar entorno virtual (opcional pero recomendable):
   - uv gestiona entornos automáticamente; si prefieres explícito:
     - `uv venv`
     - Linux/macOS: `source .venv/bin/activate`
     - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
2) Instalar el proyecto (editable) y dependencias:
   - `uv pip install -e .`

### Opción B: usando pip
1) Crear y activar entorno virtual:
   - Linux/macOS:
     - `python -m venv .venv`
     - `source .venv/bin/activate`
   - Windows (PowerShell):
     - `python -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
2) Instalar dependencias del proyecto declarado en `pyproject.toml`:
   - `pip install -e .`


## Configuración (.env opcional)
El proyecto soporta configuración por variables de entorno y/o archivo `.env` en la raíz (gracias a pydantic-settings). Variables disponibles (todas opcionales):

- Base de datos
  - `DATABASE_URL` — DSN. Por defecto: `sqlite:///app.db`
  - `SQL_ECHO` — `1/true/yes` para imprimir SQL; por defecto `0` (no)
  - `POOL_PRE_PING` — `1/true/yes` (por defecto) para validar conexiones
  - `POOL_SIZE`, `MAX_OVERFLOW`, `POOL_RECYCLE` — enteros opcionales

- IA (para scripts que generan texto)
  - `OPENAI_API_KEY` — clave para el SDK oficial de OpenAI
  - `OPENAI_MODEL` — por defecto `gpt-4o-mini`

- Otros
  - `TZ` — zona horaria (e.g. `America/Mexico_City`) útil para programar el script diario

Si no configuras nada, el sistema usa SQLite local `app.db` y valores razonables por defecto.


## Arranque (desarrollo)
1) Inicializar Reflex (solo la primera vez en tu máquina):
   - `reflex init`
   - Nota: según tu instalación, el binario puede aparecer como `reflex` o `rx`. Usaremos `reflex` en esta guía.
2) Iniciar el servidor de desarrollo:
   - `reflex run`
3) Abre el navegador en:
   - `http://localhost:3000`

Durante el arranque verás la UI tipo terminal y, en la parte superior de la página de inicio, una “secuencia de arranque” (boot) descriptiva (ver abajo).


## Arranque (producción, básico)
Existen varias estrategias. Una opción genérica con Reflex es exportar y servir con un servidor ASGI/WSGI o plataforma estática/funciones.

1) Exportar el proyecto:
   - `reflex export`
2) Sigue las instrucciones que imprime Reflex tras el export para el modo de despliegue elegido (por ejemplo, servir con `uvicorn` si corresponde, o desplegar a un servicio compatible).

Consulta la documentación oficial de Reflex para opciones de despliegue más avanzadas.


## Base de datos
- Los modelos ORM (SQLAlchemy) están en `reflex_UI_code_history/database/models.py`.
- La inicialización de tablas se realiza automáticamente al importar el paquete `reflex_UI_code_history.database` gracias a `init_db()`.
- Por defecto se crea/usa `app.db` (SQLite) en la raíz del repo; puedes cambiar a Postgres/MySQL pasando `DATABASE_URL` en `.env`.


## Secuencia de arranque (UI)
La página de inicio incluye un componente `boot_sequence_box()` (en `reflex_UI_code_history/components/boot_sequence.py`) que muestra una secuencia tipo boot dentro de la UI estilo terminal:

1. Iniciando sistema de efemérides de programación y tecnología...
2. Conectando con la base de datos ... [OK]
3. Cargando datos históricos ... [OK]
4. Sistema listo. Descubre la historia de la programación, tecnología y emprendimiento tecnológico día a día... [OK]


## Script: generar efeméride de mañana
El script `generate_tomorrow_efemeride.py` crea una efeméride para el día siguiente y la guarda en la base de datos, evitando duplicados por fecha (`display_date`).

Uso manual:

```bash
python generate_tomorrow_efemeride.py
```

### Ejecución automática en segundo plano (dentro de Reflex)
La app inicia un scheduler en segundo plano (APScheduler) al arrancar el backend de Reflex, que ejecuta diariamente la generación para el día siguiente.

- Módulo: `reflex_UI_code_history/scheduler.py`
- Inicio: se invoca `start_scheduler()` desde `reflex_UI_code_history/reflex_UI_code_history.py`.
- Programación por defecto: todos los días a las 23:59 hora local.
- Zona horaria: se lee de la variable `TZ` (e.g., `America/Mexico_City`).
- Variables opcionales para ajustar el horario:
  - `EFEMERIDE_CRON_HOUR` (por defecto `23`)
  - `EFEMERIDE_CRON_MINUTE` (por defecto `59`)

### Alternativa: cron del sistema (Linux)
Si prefieres usar cron del sistema, todos los días a las 23:59 hora local:

```cron
59 23 * * * /usr/bin/env bash -lc 'cd /ruta/al/proyecto && ./generate_tomorrow_efemeride.py >> cron_efemerides.log 2>&1'
```

Variables de entorno útiles para el script: `OPENAI_API_KEY`, `OPENAI_MODEL`, `TZ`.


## Historial de tareas realizadas con Junie (de la más antigua a la más reciente)

Nota: Para mantener un registro verificable, puedes reconstruir la lista desde git (si el historial está disponible) con alguno de estos comandos:

```bash
git log --reverse --pretty=format:"- %ad — %s" --date=short --author="Junie"
# o, si los commits mencionan a Junie en el mensaje:
git log --reverse --grep="Junie" --pretty=format:"- %ad — %s" --date=short
```

Entradas confirmadas en este repositorio:
- 2025-08-17 16:15 — Crear README.MD con la descripción del proceso de arranque de la aplicación y sección de tareas realizadas con Junie (este documento).

Si existen tareas anteriores realizadas por Junie, por favor facilita el listado (fecha, título y breve descripción) para incorporarlas aquí en orden cronológico.


## Solución de problemas
- Si el comando `reflex` no aparece, verifica que tu entorno virtual esté activo o prueba `rx` como alias.
- Si no se crea la base de datos:
  - Asegúrate de tener permisos de escritura en la raíz del proyecto.
  - Revisa `DATABASE_URL` en tu `.env`.
- Si la UI no muestra efemérides para hoy, la app usa un mensaje por defecto. Asegúrate de haber cargado datos en la tabla `efemerides` o ejecuta el script de generación.


## Créditos
- Framework: Reflex
- ORM: SQLAlchemy
- Gestión de configuración: pydantic-settings
- Asistente: Junie (JetBrains)

https://reflex.dev/blog/2024-10-8-self-hosting-reflex-with-docker
