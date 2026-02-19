Sentinel Asset Manager

Sistema de Gestión de Activos de Ciberseguridad en Tiempo Real

Sentinel Asset Manager es una solución Fullstack diseñada para centralizar, visualizar y monitorear el inventario de infraestructura crítica. Permite a los equipos de seguridad identificar activos (Servidores, IoT, Workstations) y priorizar su atención basándose en niveles de riesgo dinámicos.

Este proyecto implementa una arquitectura desacoplada (API First) y simulación de escaneo de vulnerabilidades en tiempo real.

---

Características Principales

- Tablero en Tiempo Real: Visualización instantánea del estado de los activos mediante Short Polling.
- Gestión de Inventario (CRUD): Registro, lectura y clasificación de servidores.
- Simulación de Amenazas: Script de automatización (auto_scanner.py) que simula cambios de estado y detección de nuevos activos sin intervención humana.
- Arquitectura Limpia: Separación estricta entre lógica de negocio, modelos de datos y capas de presentación.

---

Stack Tecnológico

Backend
- Python & FastAPI: Para una API rápida, asíncrona y autodocumentada.
- SQLAlchemy (ORM): Abstracción de base de datos.
- Pydantic: Validación estricta de datos (Schemas).
- SQLite: Base de datos ligera para portabilidad.

Frontend
- Vue.js 3: Framework reactivo progresivo.
- Vite: Entorno de desarrollo ultrarrápido.
- Axios: Cliente HTTP para comunicación con el Backend.

---

Decisiones Técnicas y Arquitectura

 1. Base de Datos Agnóstica (SQLAlchemy + SQLite)
Para este MVP se implementó SQLite debido a su alta portabilidad (no requiere servidores dedicados). Sin embargo, gracias al uso del ORM SQLAlchemy, el sistema es completamente agnóstico a la base de datos.

Escalabilidad: Si el proyecto requiriera migrar a PostgreSQL o MySQL en un entorno de producción, solo sería necesario actualizar la cadena de conexión en database.py sin tocar una sola línea de la lógica de negocio.

 2. Integridad de Datos (Pydantic Schemas)
En ciberseguridad, la calidad del dato es crítica. Se definieron contratos estrictos en schemas.py utilizando Pydantic. Esto asegura que la API rechace automáticamente cualquier dato basura (ej. una IP mal formateada o un tipo de dato incorrecto) antes de que llegue a la base de datos.

 3. Estrategia de Tiempo Real
Para la actualización del Dashboard se implementó Short Polling (consultas cada 2 segundos).

Trade-off: Esta decisión se tomó por ser robusta y fácil de implementar con Vue.js para la escala actual. En un escenario con miles de usuarios concurrentes, la arquitectura está preparada para migrar hacia WebSockets y así reducir la carga del servidor con una conexión bidireccional.

---

 Instalación y Despliegue

Sigue estos pasos para ejecutar el proyecto en tu entorno local.

 Prerrequisitos
- Python 3.10+
- Node.js & npm

 1. Configuración del Backend

Navega a la carpeta raíz del proyecto y crea el entorno virtual para aislar las dependencias:

 bash
Crear entorno virtual

python -m venv venv

 Activar entorno (Windows)

.\venv\Scripts\activate

 Activar entorno (Mac/Linux)
source venv/bin/activate

-----

Instalar las dependencias necesarias dentro del env (FastAPI, Uvicorn, SQLAlchemy, Security Libs):

pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose[cryptography] requests

-----

Ejecutar el servidor Backend:

Bash
cd backend
uvicorn app.main:app --reload


El servidor iniciará en: http://127.0.0.1:8000/docs#/

-----
 
 Configuración del Frontend

En una nueva terminal, navega a la carpeta del frontend:

cd frontend
npm install
npm run dev
La aplicación web estará disponible en: http://localhost:5173

-----

Este proyecto incluye un robot que simula un escáner de vulnerabilidades en la red. Este script inyecta datos y actualiza los niveles de riesgo de los servidores aleatoriamente para demostrar la reactividad del sistema.

Para correr la simulación:

Asegúrate de tener el Backend encendido.

Abrir una nueva terminal en la raíz del proyecto.

Ejecuta:

Bash
 Recuerda tener el entorno virtual activo
  python auto_scanner.py

Verás en la consola cómo se detectan y actualizan activos, y el Frontend reflejará estos cambios en tiempo real.


------

estructura del proyecto:

SENTINEL-INVENTORY/
├── auto_scanner.py      # Script de automatización y caos
├── backend/
│   ├── app/
│   │   ├── main.py      # Endpoints y lógica de rutas
│   │   ├── models.py    # Modelos de Base de Datos (Tablas)
│   │   ├── schemas.py   # Contratos de validación (Pydantic)
│   │   ├── database.py  # Conexión a DB
│   │   └── auth.py      # Lógica de seguridad
│   └── database.db      # DB generada automáticamente
├── frontend/            # Aplicación Vue.js
└── README.md            # Documentación



Desarrollado por Paul Nicolas Henao Nuñez
Ingeniero en ciencias de la computación e inteligencia artificial