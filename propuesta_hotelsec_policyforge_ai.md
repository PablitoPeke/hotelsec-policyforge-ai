# HotelSec PolicyForge AI

## Propuesta de proyecto para la Practica 1 de Ciberseguridad con Inteligencia Artificial

### Presentacion del proyecto

Mi proyecto se llama HotelSec PolicyForge AI. La idea consiste en desarrollar una plataforma web de ciberseguridad orientada a hoteles, alojamientos turisticos y pequenas empresas del sector turistico de Lanzarote.

El objetivo principal es que una empresa pueda introducir informacion sobre su situacion actual, sus sistemas tecnologicos, sus procesos con datos personales y sus medidas de seguridad, y que la plataforma genere automaticamente un diagnostico inicial de madurez, un mapa de riesgos, recomendaciones priorizadas y un paquete de politicas de seguridad adaptadas al negocio.

No quiero que sea simplemente una herramienta que genere documentos con IA. Mi objetivo es crear una solucion funcional que ayude a una pyme turistica a entender sus riesgos reales y a empezar a organizar su seguridad de una forma practica, visual y comprensible.

### Justificacion

He elegido este proyecto porque el sector turistico depende cada vez mas de sistemas digitales: reservas online, plataformas externas, TPV, correo electronico, redes WiFi para clientes, sistemas de facturacion, camaras, cerraduras inteligentes y aplicaciones en la nube.

En el caso de hoteles y alojamientos de Lanzarote, muchos negocios son pequenas o medianas empresas que no siempre tienen un departamento interno de ciberseguridad. Sin embargo, tratan datos personales de clientes, documentos de identidad, datos de pago, informacion de reservas y comunicaciones con proveedores.

Esto hace que esten expuestos a riesgos como phishing, ransomware, robo de credenciales, fuga de datos personales, mala gestion de copias de seguridad, accesos compartidos, WiFi mal segmentada o incumplimientos basicos del RGPD.

Por eso mi propuesta es crear una herramienta que actue como un primer asistente de ciberseguridad y cumplimiento. La plataforma no sustituye a una auditoria profesional, pero si permite obtener un punto de partida claro, ordenado y accionable.

### Linea de trabajo

El proyecto encaja dentro de la linea de Normativa y Cumplimiento de la practica. Concretamente, combina varias ideas del enunciado:

- Generador de politicas de seguridad con IA.
- Simulador de auditoria de ciberseguridad.
- Gestor de riesgos de seguridad con IA.
- Generador de planes de continuidad y respuesta a incidentes.
- Recomendador basico de medidas alineadas con RGPD e ISO 27001.

### Problema que resuelve

El problema principal es que muchas pymes turisticas no saben por donde empezar en ciberseguridad. Pueden tener antivirus o copias de seguridad, pero no disponen de politicas internas, no conocen su nivel de madurez, no tienen un plan de respuesta ante incidentes y no saben priorizar que medidas implantar primero.

HotelSec PolicyForge AI resuelve este problema creando un proceso guiado:

1. La empresa completa un analizador de perfil.
2. La herramienta calcula una puntuacion de madurez.
3. Se identifican riesgos tecnicos, organizativos y normativos.
4. La IA genera politicas adaptadas al caso concreto.
5. El sistema crea un plan de accion priorizado.
6. Se genera un informe PDF profesional.
7. El dashboard permite consultar el historial y la evolucion.

### Usuarios objetivo

Los usuarios principales serian:

- Hoteles pequenos y medianos.
- Apartahoteles.
- Villas turisticas.
- Hostales y pensiones.
- Empresas de alquiler vacacional.
- Pequenas agencias turisticas.
- Consultores o proveedores IT que dan soporte a este tipo de empresas.

### Funcionamiento general

El funcionamiento de la plataforma se basa en un formulario avanzado que recoge informacion de la empresa. A partir de esos datos, el backend aplica un motor de reglas para calcular riesgos y niveles de madurez. Despues, un motor de IA genera textos adaptados: politicas internas, recomendaciones, resumen ejecutivo y plan de accion.

El resultado final se muestra en un dashboard web y tambien se puede descargar como informe PDF.

### Campos del analizador de empresa

El analizador no se limita a preguntar el sector y el numero de empleados. Incluye campos especificos para el contexto hotelero:

#### Perfil del negocio

- Nombre del hotel o alojamiento.
- Municipio de Lanzarote.
- Tipo de alojamiento.
- Numero de habitaciones o unidades.
- Numero de empleados fijos.
- Numero de empleados temporales.
- Temporada alta y baja.
- Existencia o no de proveedor informatico externo.

#### Sistemas tecnologicos

- PMS hotelero.
- Channel manager.
- Motor de reservas web.
- Plataformas externas como Booking, Expedia o Airbnb.
- TPV fisico y pagos online.
- Software de facturacion.
- Correo corporativo.
- Almacenamiento en la nube.
- Web propia.
- CRM o base de datos de clientes.

#### Seguridad actual

- Uso de doble factor de autenticacion.
- Uso de gestor de contrasenas.
- Politica de contrasenas.
- Existencia de cuentas compartidas.
- Frecuencia de copias de seguridad.
- Pruebas de restauracion de backups.
- Antivirus o EDR.
- Firewall.
- Actualizaciones de sistemas.
- Separacion entre WiFi de clientes y red interna.

#### Datos personales y RGPD

- Datos personales tratados.
- Documentos de identidad o pasaportes.
- Datos de pago.
- Datos de menores.
- Tiempo de conservacion de la informacion.
- Cesion de datos a terceros.
- Contratos con encargados de tratamiento.
- Registro de actividades de tratamiento.
- Protocolo de brechas de seguridad.

#### Riesgo operativo

- Impacto si cae el sistema de reservas.
- Impacto si se pierde acceso al correo.
- Impacto si hay ransomware.
- Capacidad de operar sin internet.
- Procedimiento manual de check-in y check-out.
- Persona responsable ante incidentes.
- Tiempo de respuesta del proveedor IT.

#### Personal y concienciacion

- Formacion en phishing.
- Instrucciones para empleados temporales.
- Revocacion de accesos al finalizar contratos.
- Uso de dispositivos personales.
- Uso de WhatsApp o mensajeria para datos de clientes.

#### Instalaciones e IoT

- Camaras CCTV.
- Cerraduras electronicas.
- Domotica.
- Termostatos inteligentes.
- Tablets de recepcion.
- Kioscos de check-in.
- Sistemas de control horario.

### Funcionalidades principales

#### 1. Dashboard principal

El dashboard mostrara la informacion mas importante de forma visual:

- Puntuacion global de madurez.
- Nivel de riesgo general.
- Riesgos criticos detectados.
- Numero de politicas generadas.
- Tareas pendientes.
- Ultimos analisis realizados.
- Estado del plan de accion.

#### 2. Evaluador de madurez

La herramienta calculara una puntuacion de 0 a 100. Esta puntuacion se dividira por areas:

- Identidad y accesos.
- Proteccion de datos.
- Copias de seguridad.
- Seguridad de red.
- Seguridad de dispositivos.
- Concienciacion del personal.
- Respuesta a incidentes.
- Continuidad del negocio.

#### 3. Mapa de riesgos

El sistema generara un mapa de riesgos con niveles bajo, medio, alto y critico. Cada riesgo tendra:

- Descripcion.
- Causa probable.
- Impacto.
- Probabilidad.
- Nivel de prioridad.
- Medida recomendada.

#### 4. Generador de politicas con IA

La IA generara politicas adaptadas al perfil de la empresa. Las politicas iniciales seran:

- Politica de contrasenas.
- Politica de copias de seguridad.
- Politica de uso de dispositivos.
- Politica de teletrabajo.
- Politica de WiFi para huespedes.
- Politica de uso del PMS y sistemas de reservas.
- Politica de proveedores externos.
- Politica de respuesta a incidentes.
- Politica de tratamiento de datos personales.
- Politica de uso aceptable de correo y mensajeria.

#### 5. Recomendaciones RGPD e ISO 27001

La herramienta ofrecera recomendaciones basicas relacionadas con RGPD, LOPDGDD e ISO 27001, siempre dejando claro que se trata de una ayuda inicial y no de una certificacion oficial.

Ejemplos de recomendaciones:

- Revisar contratos con proveedores que tratan datos.
- Crear un protocolo de notificacion de brechas.
- Documentar el registro de actividades de tratamiento.
- Aplicar doble factor en cuentas criticas.
- Separar la red WiFi de clientes de la red interna.
- Probar periodicamente las copias de seguridad.

#### 6. Plan de accion priorizado

El sistema generara un plan de accion dividido por plazos:

- Acciones inmediatas.
- Acciones a 30 dias.
- Acciones a 90 dias.
- Mejoras recomendadas a medio plazo.

Cada accion incluira prioridad, dificultad, impacto y responsable sugerido.

#### 7. Generador de informe PDF

El informe PDF sera uno de los entregables mas importantes de la herramienta. Incluira:

- Resumen ejecutivo.
- Perfil del hotel.
- Resultado del analisis.
- Puntuacion de madurez.
- Mapa de riesgos.
- Politicas generadas.
- Recomendaciones normativas.
- Plan de accion.
- Conclusiones.

#### 8. Historial de analisis

La plataforma guardara los analisis realizados por cada empresa. Esto permitira comparar la evolucion de la madurez de seguridad a lo largo del tiempo.

### Arquitectura propuesta

La arquitectura general sera:

Usuario / Hotel
    ->
Frontend Web
    ->
Formulario de analisis
    ->
Backend API
    ->
Motor de reglas + Motor IA
    ->
Base de datos
    ->
Dashboard + Informe PDF

### Stack tecnico propuesto

#### Frontend

Para el frontend utilizare:

- React con Vite.
- TypeScript.
- Tailwind CSS.
- React Router.
- React Hook Form.
- Zod para validacion de formularios.
- Recharts para graficas del dashboard.
- Lucide React para iconos.
- Axios o TanStack Query para comunicacion con la API.

El frontend tendra una interfaz clara, con formularios por pasos, dashboard visual, tablas de riesgos y botones para generar o descargar informes.

#### Backend

Para el backend utilizare:

- Python.
- FastAPI.
- Pydantic para validacion de datos.
- SQLAlchemy como ORM.
- Alembic para migraciones.
- JWT para autenticacion.
- Passlib o bcrypt para cifrado de contrasenas.

FastAPI encaja bien porque permite crear una API rapida, documentada automaticamente con Swagger y facil de conectar con servicios de IA.

#### Base de datos

La base de datos recomendada sera:

- PostgreSQL.

Guardara usuarios, empresas, respuestas del analizador, puntuaciones, riesgos, politicas generadas e informes.

Como mejora futura se podria anadir pgvector para guardar embeddings y permitir busqueda semantica sobre politicas, normativa o documentos.

#### Inteligencia Artificial

Para la parte de IA utilizare:

- OpenAI API o un modelo local mediante Ollama.
- Prompts estructurados por tipo de documento.
- Plantillas para politicas.
- Motor de reglas previo para evitar que todo dependa del modelo.
- Posible RAG en una segunda fase con documentacion de INCIBE, AEPD, ISO 27001 o NIST.

La IA se usara para generar lenguaje natural adaptado al caso de la empresa, pero las puntuaciones y riesgos principales se apoyaran en reglas controladas para que el resultado sea mas consistente.

#### Generacion de PDF

Para los informes PDF utilizare:

- ReportLab o WeasyPrint.

El objetivo es generar un informe con portada, tablas, resumen ejecutivo, resultados, recomendaciones y plan de accion.

#### Despliegue

El despliegue se realizara en:

- Hetzner Cloud VPS.
- Docker.
- Docker Compose.
- Nginx como reverse proxy.
- Certbot / Let's Encrypt para HTTPS.
- Dominio o subdominio propio.

La aplicacion quedara accesible desde internet, cumpliendo el requisito obligatorio de despliegue en servidor real.

#### Repositorio y control de versiones

El codigo estara en GitHub. La estructura recomendada sera:

- frontend/
- backend/
- docker-compose.yml
- docs/
- README.md
- .env.example

Se usaran commits claros y organizados por fases:

- configuracion inicial,
- frontend base,
- backend API,
- base de datos,
- motor de scoring,
- integracion IA,
- generacion PDF,
- despliegue.

#### Seguridad de la propia herramienta

La plataforma tambien debe protegerse correctamente. Para ello incorporare:

- HTTPS.
- Autenticacion con JWT.
- Hash seguro de contrasenas.
- Variables de entorno para secretos.
- Validacion de entradas.
- Control basico de roles.
- Rate limiting en endpoints sensibles.
- Logs de actividad.
- Copias de seguridad de la base de datos.

### Roadmap para la Practica 2

Para una segunda fase planteo estas mejoras:

1. Integrar fuentes oficiales de INCIBE y AEPD mediante RAG.
2. Crear un modulo de simulacion de incidentes.
3. Anadir evaluacion de proveedores externos.
4. Incorporar comparativas mensuales de madurez.
5. Crear un modulo de formacion para empleados.
6. Anadir recomendaciones por presupuesto.
7. Implementar multiidioma: espanol, ingles y aleman.
8. Integrar escaneo basico de dominio web.
9. Mejorar el sistema de evidencias para auditoria.
10. Crear alertas automaticas para tareas pendientes.

### Conclusion

HotelSec PolicyForge AI es una propuesta realista y alineada con los requisitos de la practica. Combina desarrollo web, inteligencia artificial, ciberseguridad, normativa, gestion de riesgos, generacion documental y despliegue real.

La herramienta tiene un caso de uso concreto: ayudar a hoteles y pymes turisticas de Lanzarote a conocer su nivel inicial de ciberseguridad y obtener politicas y recomendaciones adaptadas a su situacion.

Considero que es un proyecto adecuado para la Practica 1 porque permite construir una version funcional en el plazo disponible y, al mismo tiempo, deja margen para ampliar la herramienta en una Practica 2 con funcionalidades mas avanzadas.
