# HotelSec PolicyForge AI - Guion breve de grabacion

Autor: Pablo Cortes. Version: 0.4.0. Revision: 15/10/2026.

Lee solo LEER. PANTALLA son acciones silenciosas. En las alternativas, lee solamente la que describa el resultado real.

Duracion prevista: 12-14 minutos orientativos, incluidas acciones; comprobar que el MP4 real dura al menos 10 minutos. No acredita duracion del archivo ni minutos reales.

## Requisitos del video
- MP4 de al menos 10 minutos. El enunciado recomienda no superar 20, aunque no fija un máximo estricto.
- Resolución mínima 720p; recomendada 1080p. La pantalla debe leerse y el audio oírse con claridad.
- Presentación, requisitos originales y cambios, arquitectura, recorrido funcional, errores/seguridad y limitaciones.
- Mostrar el producto real obtenido del código entregado. Las diapositivas son solo apoyo; la mayoría del vídeo debe mostrar la app.
- Los cortes para eliminar esperas deben identificarse en pantalla. No cortar para ocultar fallos.
- Datos ficticios y sistemas propios. No grabar contraseñas, claves, cookies, archivos .env ni credenciales del VPS.
- Subir a YouTube no listado o servicio equivalente con permiso para cualquiera con el enlace. Probar en incógnito.
- Después de grabar, anotar los minutos exactos de cada requisito y poner el enlace en portada y comentario de entrega. Los tiempos de este guion NO son esa evidencia.

## Preparacion antes de REC
- Ensaya una vez. Lee solo LEER; PANTALLA indica qué pulsar, no se pronuncia. Usa el guion en el móvil u otro monitor que no estés grabando. Los anexos son de consulta: no se leen en el vídeo.
- Entiende antes sesiones, CSRF, propietario, scoring, snapshots y fallback. El enunciado permite asistencia IA, pero exige comprender lo entregado.
- Abre la app pública, el repo en la rama practica3, VS Code con este proyecto, la memoria previa al vídeo y una ventana de incógnito.
- En VS Code deja abiertas solo README.md, docker-compose.production.yml, backend/app/db.py y docs/practica3/evidence/closeout-verification.json. No abras .env, inspect ni configuración efectiva con secretos.
- Prepara un correo ficticio nuevo, por ejemplo video-pablo-1510-01@example.org. Si ya existe, cambia el sufijo. Crea la cuenta al grabar B04, con contraseña privada y única de 12-128 caracteres. No muestres la contraseña.
- Guarda esa contraseña de forma privada para poder iniciar sesión, exportar datos y borrar la cuenta de demo al terminar. No actives el icono de mostrar contraseña.
- Comprueba que backend/.venv/Scripts/python.exe existe antes de mostrar los comandos del anexo. Ejecútalos desde la raíz del proyecto en PowerShell. No son comandos del SSH de Hetzner.
- El bloque IA es opcional en este recorrido y puede consumir crédito: una petición puede hacer hasta tres llamadas. Esta preparación no ejecuta llamadas de pago. Si no quieres gastar, usa la alternativa expresamente sin nueva prueba IA.
- Si muestras IA real, usa el texto coherente del caso mejorado. No vuelvas a enviar una contradicción con IA una y otra vez: podría gastar cuota/crédito.
- Antes de REC copia los dos textos de ejemplo a una nota sin secretos y deja listo el comando de seguridad en una terminal PowerShell local. Cierra notificaciones y pestañas personales. Graba 15 segundos de prueba de audio y pantalla.
- El grupo sigue sin confirmar. Añade el número real a tu presentación cuando lo sepas; no digas grupo01 ni inventes compañeros. El guion base identifica correctamente tu trabajo individual.
- La instalación por una persona externa aún está pendiente. Si no se ha hecho al grabar, usa la frase de limitación incluida, no una afirmación de éxito.

## Datos exactos de la demostracion

| Campo | Valor |
|---|---|
| Nombre del alojamiento | Hotel Demo Lanzarote - Video |
| Municipio / Tipo | Tías / Hotel |
| Habitaciones / fijos / temporales | 40 / 12 / 8 |
| Frecuencia de backups inicial | No se realizan |
| Temporada alta / Respuesta IT | Todo el año / 24 horas |
| Sistemas | PMS en la nube, Microsoft 365, TPV |
| Categorías de datos | Reservas, facturación |
| Conservación prevista | 180 días ficticios; no es una recomendación legal ni el borrado de la app |
| Gobierno y continuidad | Plan de continuidad: No. Resto: Sin confirmar |
| Contexto inicial | No usamos MFA y no hacemos copias. |
| Permiso de OpenAI al inicio | Desmarcado |
| Mejora posterior | MFA y gestor: Sí; backups: Diaria; restauración, actualización y WiFi separada: Sí |
| Texto para nueva prueba IA, si decides hacerla | El correo del hotel usa doble factor. Las copias de seguridad se realizan a diario y se prueba su restauración. |

## Recorrido rapido: tres evaluaciones como maximo

1. **Inicial:** rellenar el hotel, provocar la contradiccion MFA, elegir Usar texto y guardar SIN IA.
2. **Mejorada:** reevaluar el mismo hotel, BORRAR el texto antiguo y activar las seis mejoras, SIN IA.
3. **IA opcional:** partir de la mejorada, pegar el texto coherente y autorizar una sola peticion; puede consumir credito.

Para el PDF con la accion completada, abrir la evaluacion INICIAL, no la mejorada.
No leer esta hoja ni todos los anexos en voz alta. Los tiempos son una referencia; no corras para seguirlos.

**Casillas marcadas al empezar:**
- Proveedor IT externo
- Usa PMS o channel manager
- Ofrece WiFi a huéspedes
- Acepta pagos con tarjeta
- Usa doble factor (marcado intencionadamente para la contradicción)
- Comparte cuentas
- Tiene antivirus/EDR
- Usa cámaras, domótica o IoT
- Proveedores con acceso remoto

**Casillas desmarcadas al empezar:**
- Guarda documentación de huéspedes
- Usa gestor de contraseñas
- PMS con usuarios individuales
- Proceso de baja de empleados
- Prueba restauración de backups
- Sistemas actualizados
- WiFi de huéspedes separada
- TPV/red de pagos aislada
- IoT/CCTV en red separada
- Acceso remoto de proveedores controlado
- Plan de respuesta a incidentes
- Protocolo de brechas RGPD
- Registro RGPD de tratamientos
- Formación contra phishing

---

## B01 | 00:00-00:35 previsto | Presentación

Requisitos: RE-01, RE-02

### PANTALLA - NO LEER
1. Mostrar la app en la pantalla de acceso, sin escribir contraseñas todavía.
2. Si conoces tu grupo al grabar, añadir su número real tras decir tu nombre.

### LEER

Hola, soy Pablo Cortes y presento HotelSec PolicyForge AI, mi proyecto individual para hoteles de Lanzarote. La aplicación ayuda a conocer sus riesgos de ciberseguridad y por dónde empezar a mejorar.

Voy a mostrar un caso completo: crear una cuenta, analizar un hotel, comparar una mejora y descargar su informe. Todos los datos son ficticios.


---

## B02 | 00:35-01:05 previsto | Punto de partida y requisitos

Requisitos: RE-01, RE-03

### PANTALLA - NO LEER
1. Mostrar el repositorio GitHub, rama practica3, y brevemente docs/practica3/06_estado_entrega.md.
2. Volver a la app antes de entrar en explicaciones largas.

### LEER

Parto de la Práctica 1, que obtuvo un nueve sobre diez, sin comentarios del profesor. En esta versión he completado el acceso por cuenta, el guardado, el historial, el plan de mejora y el PDF.

También he unido el texto libre con el formulario. Esta matriz relaciona los requisitos con el código y las pruebas.


---

## B03 | 01:05-02:05 previsto | Arquitectura y decisiones

Requisitos: RNF-01, RNF-03, RNF-07, RE-03

### PANTALLA - NO LEER
1. En la memoria, localizar el diagrama de arquitectura desde el índice y señalar pantalla, API y base de datos. No recorrer toda la memoria.
2. En el explorador de VS Code señalar frontend/src, backend/app y docker-compose.production.yml, sin abrir .env.
3. Abrir en otra pestaña https://178-105-149-202.sslip.io/api/v1/health. Mostrar la versión que realmente responda y volver a la app.

### LEER

La arquitectura tiene tres partes. React y TypeScript muestran la pantalla. FastAPI recibe y valida los datos. PostgreSQL guarda las cuentas y evaluaciones; Alembic controla los cambios de sus tablas.

La puntuación usa reglas. OpenAI es opcional para interpretar texto y personalizar contenido, y ReportLab genera el PDF. Docker Compose organiza los servicios en Hetzner y Caddy publica la web con HTTPS.

Aquí consulto la versión del servidor. El código está en GitHub y la dirección usa sslip.io; no es un dominio propio.


---

## B04 | 02:05-02:45 previsto | Registro y privacidad

Requisitos: RF-11, RNF-05

### PANTALLA - NO LEER
1. Pulsar Crear cuenta. Nombre: Pablo Demo. Introducir el correo ficticio y tu contraseña privada, siempre oculta.
2. Pulsar el botón Crear cuenta del formulario y esperar al Dashboard.
3. Si ensayaste con esa cuenta, entrar por Acceder; no fingir que es un registro nuevo.

### LEER

Creo una cuenta de demostración. Cada usuario tiene sus propios hoteles y análisis. La contraseña se guarda como un hash Argon2, no en texto plano, y la sesión utiliza una cookie HttpOnly.

Para esta evaluación no necesito datos reales de huéspedes ni tarjetas: solo describir los sistemas y las medidas de seguridad.


---

## B05 | 02:45-04:05 previsto | Formulario del hotel ficticio

Requisitos: RF-01, RNF-02, RNF-05

### PANTALLA - NO LEER
1. Abrir Nuevo análisis. Escribir Hotel Demo Lanzarote - Video, Tías, Hotel, 40 habitaciones, 12 empleados fijos y 8 temporales. Completar el resto con la ficha inicial del guion; no explicar cada casilla en voz alta.
2. Backups: No se realizan. Dejar Usa doble factor marcado a propósito; las demás casillas siguen la lista inicial. Mantener OpenAI desmarcado.
3. En Contexto adicional pegar: No usamos MFA y no hacemos copias.
4. Para enseñar un error, cambiar solo Habitaciones a 0 y pulsar Analizar y guardar. Mostrar el aviso del navegador y volver a 40. Esta prueba de interfaz no demuestra por sí sola la validación del servidor.

### LEER

El ejemplo es un hotel de cuarenta habitaciones, doce empleados fijos y ocho temporales. Indico sus sistemas y controles; si no conozco una medida, puedo dejarla sin confirmar.

Pongo cero habitaciones para enseñar la validación del navegador y después lo corrijo a cuarenta.

Ahora dejo marcado el doble factor, pero escribo que no lo usamos. Es una contradicción intencionada. De momento no envío datos a OpenAI.


---

## B06 | 04:05-04:45 previsto | Contradicción y análisis único

Requisitos: RF-12, RNF-02

### PANTALLA - NO LEER
1. Pulsar Analizar y guardar. Esperar al diálogo Datos contradictorios.
2. Señalar uses_mfa: formulario true, texto false. No hace falta leer el identificador en inglés.
3. Pulsar Usar texto. Esperar al Dashboard. Si no aparece el diálogo, revisar la casilla MFA y el texto: no leer una confirmación ficticia.

### LEER

Aquí aparece la contradicción. Elijo Usar texto, así que el análisis considerará que no hay doble factor y mantendrá el resto del formulario.

La descripción complementa el mismo análisis, no genera uno separado. En este ejemplo la detección usa reglas locales, no OpenAI.


---

## B07 | 04:45-05:25 previsto | Dashboard, madurez y riesgos

Requisitos: RF-02, RF-03, RF-07

### PANTALLA - NO LEER
1. Mostrar Madurez, Riesgos, Acciones completadas y Analisis guardados.
2. Bajar a puntuaciones por área y señalar un riesgo relacionado con copias o accesos.
3. Mostrar el distintivo Fallback reglas. No leer una puntuación preescrita: los números reales son los de pantalla.

### LEER

El dashboard muestra la madurez, los riesgos y el progreso. Por ejemplo, no hacer copias genera una recomendación para proteger y recuperar la información.

La puntuación sale de reglas, no de una opinión de la IA. Evalúa lo que declara el hotel; no inspecciona sus equipos. Aquí el resumen usa el respaldo por reglas.


---

## B08 | 05:25-06:00 previsto | Políticas y orientación normativa

Requisitos: RF-04, RF-05

### PANTALLA - NO LEER
1. Abrir Politicas y mostrar Orden de implantacion.
2. Recorrer dos políticas: contraseñas/accesos y copias. Mostrar objetivo, alcance, controles y revisión.
3. No afirmar que se usan políticas IA en este análisis por reglas.

### LEER

Se generan diez políticas. Muestro las de contraseñas y copias: incluyen objetivo, alcance, controles y revisión, no solo un título.

Las referencias de AEPD, INCIBE e ISO sirven de orientación. El documento no certifica cumplimiento legal y necesita revisión humana. En este análisis las políticas proceden de reglas.


---

## B09 | 06:00-06:45 previsto | Plan de mejora y persistencia

Requisitos: RF-06, RF-07, RF-09

### PANTALLA - NO LEER
1. Abrir Plan de mejora. Cambiar solo la primera acción a Completada y esperar a que se guarde.
2. Recargar con F5. Abrir Historial, localizar este análisis y usar el icono del ojo para abrirlo.
3. Volver a Plan de mejora y comprobar que esa acción sigue Completada. No borrar esta evaluación.

### LEER

El plan organiza las acciones por prioridad, plazo y responsable sugerido. Marco la primera como completada, recargo y vuelvo a abrir el análisis desde el historial para comprobar que se guarda.

Completar una acción no sube la puntuación: para reflejar medidas nuevas hay que reevaluar el hotel.


---

## B10 | 06:45-07:50 previsto | Historial y reevaluación

Requisitos: RF-09, RF-10, RF-02

### PANTALLA - NO LEER
1. Con el análisis inicial abierto, ir a Informe y pulsar Reevaluar alojamiento.
2. IMPORTANTE: vaciar Contexto adicional para que no siga negando MFA y copias. Mantener el mismo nombre y municipio.
3. Marcar MFA, gestor de contraseñas, restauración de backups, sistemas actualizados y WiFi separada. Cambiar Frecuencia de backups a Diaria. Mantener OpenAI desmarcado.
4. Analizar y guardar. Comprobar variación de madurez y dos registros en Historial.

### LEER

Ahora simulo una mejora del mismo hotel: activo doble factor, gestor de contraseñas, copias diarias, restauración, actualizaciones y WiFi separado.

Borro la descripción antigua porque ya no representa esta situación. Al guardar se crea otra evaluación; la anterior no se sobrescribe. Muestro las dos en el historial y comparo su puntuación.

La comparación usa los registros de la página cargada y refleja lo declarado, no una inspección técnica.


---

## B11 | 07:50-08:35 previsto | Informe PDF para el cliente

Requisitos: RF-08, RF-05, RF-06

### PANTALLA - NO LEER
1. En Historial abrir la evaluación MÁS ANTIGUA de este hotel, la que contiene la acción completada.
2. Abrir Informe y pulsar Descargar informe PDF. Abrir el PDF descargado.
3. Mostrar portada/resumen, perfil, riesgos, Plan de accion con Estado: Completada, políticas completas y referencias. Usar búsqueda del visor si es necesario.

### LEER

Abro la evaluación inicial y descargo su PDF. Incluye el perfil, las puntuaciones, los riesgos, las políticas y el plan con la acción que he completado.

Está pensado para que el cliente lo revise y comparta. Solo puedo descargar informes de mi cuenta, y el documento indica sus límites y el origen del contenido.


---

## B12 | 08:35-09:40 previsto | IA real o alternativa honesta

Requisitos: RF-04, RF-12, RF-13, RNF-06

### PANTALLA - NO LEER
1. Para probar IA con crédito: Historial > abrir la evaluación mejorada > Informe > Reevaluar alojamiento. No usar la evaluación inicial.
2. En Contexto adicional pegar: El correo del hotel usa doble factor. Las copias de seguridad se realizan a diario y se prueba su restauración. No cambiar las casillas mejoradas.
3. Marcar el permiso OpenAI y pulsar Analizar y guardar UNA vez. Puede consumir crédito y hasta tres llamadas. Si recortas la espera, identificar el corte en pantalla.
4. Mirar el origen del resumen y leer solo UNA de las tres alternativas. Si funciona el resumen, comprobar por separado Resumen / Políticas en la portada del PDF de esta nueva evaluación; no afirmar que todo usó IA por un único distintivo.
5. Si NO quieres una llamada nueva, no marcar OpenAI ni guardar otra evaluación. Mostrar el permiso y la evidencia histórica live-ai-check.json, sin abrir claves. Leer solo la tercera alternativa.

### LEER

La IA es opcional: complementa el formulario con el texto y puede personalizar políticas y resumen. La puntuación sigue usando reglas. El envío requiere permiso y tiene límites de uso, aunque no son un tope de gasto en dólares.


### LEER solo si el resumen actual indica modelo IA, no Fallback reglas

El resumen indica que ha usado IA y conserva los datos del formulario. En el PDF compruebo por separado el origen de las políticas. El contenido sigue necesitando revisión humana.


### LEER si has enviado la petición pero aparece Fallback reglas

Esta vez aparece el respaldo por reglas: el análisis continúa, pero no lo presento como éxito de la IA. La prueba real guardada del trece de octubre es histórica, no el resultado de este intento.


### LEER si NO haces una nueva llamada de pago

No hago una llamada de pago en esta grabación. Muestro el permiso y una prueba real guardada del trece de octubre, de la versión cero punto tres. La evaluación actual sigue usando reglas; esa evidencia no es una prueba en directo.


---

## B13 | 09:40-10:25 previsto | Mi cuenta y gestión de datos

Requisitos: RF-11, RNF-05

### PANTALLA - NO LEER
1. Mi cuenta > Perfil: poner Organización = Hotel Demo Lanzarote y Cargo = Responsable IT. Guardar, pulsar F5 y comprobar que siguen ahí.
2. En Seguridad señalar cambiar contraseña y sesiones. En Actividad mostrar los eventos. No cambiar la contraseña durante este recorrido.
3. En Mis datos señalar Descargar mis datos y borrado, sin ejecutarlos en el recorrido breve. Mostrar que el correo está desactivado. No borrar la cuenta que contiene la demostración.

### LEER

En Mi cuenta cambio mis datos y compruebo que se guardan. También puedo gestionar contraseña y sesiones, consultar actividad y exportar o borrar mis datos con confirmación de contraseña.

La exportación de datos es JSON; el informe para el hotel es PDF. Las funciones de correo están desactivadas porque todavía falta configurar el envío.


---

## B14 | 10:25-11:45 previsto | Errores y controles de acceso en acción

Requisitos: RF-11, RNF-02, RNF-03, RNF-05

### PANTALLA - NO LEER
1. Abrir ventana de incógnito SIN iniciar sesión y visitar https://178-105-149-202.sslip.io/api/v1/records. Mostrar la respuesta Inicia sesion para continuar. No muestra los registros de tu ventana normal.
2. En VS Code > Terminal > PowerShell, desde la raíz del proyecto, ejecutar el comando Seguridad en directo del anexo UNA vez.
3. Esperar el JSON real. Leer la confirmación SOLO si passed es true y cleanup contiene dos account_deleted. Si no, usar la frase de incidente y explicar el resultado.
4. El script usa dos cuentas TEMPORALES nuevas y sin IA; no borra tu cuenta del vídeo ni sus análisis. No abrir logs o archivos de cookies para demostrarlo.

### LEER

En incógnito intento consultar los análisis sin sesión. La API pide iniciar sesión y no muestra mis datos.

Ahora ejecuto una prueba sobre mi servidor, con dos cuentas temporales y sin IA. Comprueba el guardado, el PDF, la protección CSRF y que una cuenta no pueda leer, cambiar ni borrar análisis de otra. No basta con ocultar los botones: lo controla el servidor.


### LEER solo con passed true y dos account_deleted

La prueba termina correctamente y elimina sus dos cuentas temporales. Este resultado sí corresponde a la ejecución que acabo de mostrar.


### LEER si la comprobación no termina correctamente

La prueba no termina como esperaba. Mantengo el error visible y lo revisaré antes de entregar; no la doy por superada.


---

## B15 | 11:45-12:25 previsto | Pruebas, dependencias y repositorio

Requisitos: RNF-01, RNF-04, RNF-06, RE-03

### PANTALLA - NO LEER
1. Mostrar closeout-verification.json: backend99/0/0, clon limpio y navegador, vulnerabilidades0, Gitleaks y CI.
2. Mostrar el README y el historial de commits de practica3.
3. En este bloque muestra evidencia guardada; no digas que ejecutas99tests en directo. El comando pytest del anexo sirve para ensayar antes o para otra comprobación fuera del recorrido base.
4. No mostrar una marca verde de Actions: el bloqueo de facturación sigue siendo una limitación registrada.

### LEER

Estas son evidencias guardadas: noventa y nueve pruebas superadas, instalación limpia, pruebas de navegador y revisión de dependencias y secretos. No estoy ejecutando toda la suite ahora ni afirmo que no pueda haber vulnerabilidades.

GitHub conserva el código, el README y los commits. Actions quedó bloqueado por facturación, así que no lo presento como pruebas automáticas superadas en GitHub.


---

## B16 | 12:25-13:20 previsto | Limitaciones, asistencia IA y cierre

Requisitos: RNF-05, RNF-07, RE-01, RE-02, RE-03

### PANTALLA - NO LEER
1. Mostrar la sección Limitaciones de la memoria y después volver al Dashboard.
2. Leer solo la alternativa de prueba externa que sea cierta al grabar.
3. No decir que ya existe tag final, enlace del vídeo o entrega al campus. Eso se cierra después de grabar.
4. Al terminar, detener grabación y comprobar el archivo MP4 real: duración, resolución y sonido.

### LEER

Es un autodiagnóstico académico, no una auditoría. Para venderlo faltarían correo real, MFA, copias externas y revisión independiente. El backup actual está en el mismo servidor.

He utilizado Codex como apoyo para desarrollo, pruebas y documentación. Está declarado en la memoria y me corresponde comprender y defender el trabajo. Las cuarenta horas son mi estimación aproximada.


### DECIR si todavía falta la prueba externa

Sigue pendiente que una persona ajena al grupo instale la app siguiendo el README. La prueba automatizada no sustituye esa comprobación.


### DECIR solo si ya hay un registro REAL de instalación externa

La instalación por una persona ajena al grupo queda registrada en la entrega, con su fecha y resultado.


### LEER AL FINAL DEL BLOQUE

Para cerrar la entrega añadiré el enlace y los minutos reales del vídeo a la documentación. Gracias.


---

## Comandos preparados

### Seguridad en directo, sin IA

En VS Code: Terminal > New Terminal > PowerShell, en la raíz del proyecto, NO dentro del SSH. Copia el bloque completo de tres líneas desde el Markdown y déjalo listo antes de B14. Pulsa Enter una vez. Crea y borra solo dos cuentas temporales. Busca passed: true y dos account_deleted; no declares éxito si faltan.

```powershell
backend/.venv/Scripts/python.exe scripts/verify_deployment.py `
  --url https://178-105-149-202.sslip.io `
  --confirm-test-data
```

### Pruebas unitarias opcionales

PowerShell local; raíz del proyecto. Usa bases temporales, no la DB de producción. La suite tiene un aviso conocido de deprecación; no confundirlo con fallo.

```powershell
$env:PYTHONPATH="$PWD/backend"
backend/.venv/Scripts/python.exe -m pytest backend/tests -q
```

### Consultar versión pública

Navegador: respuesta pública de salud, no revela clave ni datos de usuarios.

```powershell
https://178-105-149-202.sslip.io/api/v1/health
```

## Frases ante incidencias

### Una espera larga

La petición sigue en curso. Si elimino esta espera en la edición, indicaré el corte en pantalla; no lo utilizaré para ocultar un error.

### Error inesperado

Este resultado no es el esperado y lo mantengo visible. No lo voy a presentar como una prueba superada. Tendré que revisar esta ejecución antes de cerrar la entrega.

### 429 o límite de uso

El servicio indica que se ha alcanzado un límite de peticiones. No voy a desactivarlo ni a repetir solicitudes continuamente. Espero a que corresponda o continúo por reglas, explicando la limitación.

### Comparativa no visible

En esta ejecución no aparece la comparación. Su alcance está limitado a la página de historial cargada; revisaré que ambas evaluaciones sean del mismo alojamiento y estén disponibles. No voy a inventar una variación.

### Error al registrar porque la cuenta existe

Esta cuenta ya se utilizó en el ensayo. Voy a acceder a ella o utilizar otra cuenta ficticia; no presentaré un acceso como si fuera un registro nuevo.

## Despues de grabar
1. Reproducir el MP4 completo. Medir duración real >=10min, resolución >=720p, audio y legibilidad. Los tiempos del guion no prueban duración.
2. Si hay un error real pendiente en el producto, corregirlo o documentar la limitación antes de entregar. No editarlo para aparentar un éxito.
3. Subir como no listado o con acceso mediante enlace y comprobar desde incógnito. Anotar URL, duración, resolución y formato reales.
4. Rellenar los minutos MM:SS donde realmente se ve cada requisito. Algunos pueden compartir bloque; usar el punto exacto de tu vídeo, no el inicio previsto de esta hoja.
5. Confirmar grupo e instalación por persona externa. Entregar esos datos y el enlace para actualizar memoria_content.json, delivery_metadata.json y matriz.
6. Regenerar y revisar la memoria final, crear tag v1.0-practica3 sobre el commit definitivo y comprobar el acceso al repo. No se crea el tag por generar este guion.
7. Adjuntar PDF y enlaces a vídeo y GitHub en la tarea del campus y en portada. Confirmar la hora de cierre del16/10; el enunciado no fija aquí una hora que podamos inventar.
8. Después de grabar y conservar las evidencias necesarias, borrar solo la cuenta ficticia del vídeo y sus datos. No borrar tu cuenta personal ni ejecutar down-v.

## Minutos REALES para la matriz

No rellenado: falta el MP4. Copiar el minuto observado, no el previsto.

| Requisito | Bloques orientativos | MM:SS real |
|---|---|---|
| RF-01 | B05 | Pendiente |
| RF-02 | B07, B10 | Pendiente |
| RF-03 | B07 | Pendiente |
| RF-04 | B08, B12 | Pendiente |
| RF-05 | B08, B11 | Pendiente |
| RF-06 | B09, B11 | Pendiente |
| RF-07 | B07, B09 | Pendiente |
| RF-08 | B11 | Pendiente |
| RF-09 | B09, B10 | Pendiente |
| RF-10 | B10 | Pendiente |
| RF-11 | B04, B13, B14 | Pendiente |
| RF-12 | B06, B12 | Pendiente |
| RF-13 | B12 | Pendiente |
| RNF-01 | B03, B15 | Pendiente |
| RNF-02 | B05, B06, B14 | Pendiente |
| RNF-03 | B03, B14 | Pendiente |
| RNF-04 | B15 | Pendiente |
| RNF-05 | B04, B05, B13, B14, B16 | Pendiente |
| RNF-06 | B12, B15 | Pendiente |
| RNF-07 | B03, B16 | Pendiente |
| RE-01 | B01, B02, B16 | Pendiente |
| RE-02 | B01, B16 | Pendiente |
| RE-03 | B02, B03, B15, B16 | Pendiente |

## Mini glosario para entender lo que dices

| Concepto | Explicacion |
|---|---|
| Frontend | La pantalla y los controles que utiliza el usuario. |
| Backend / API | El servidor que valida peticiones, aplica reglas y guarda/recupera resultados. |
| Snapshot | Una evaluación guardada; una reevaluación crea otra sin sobrescribirla. |
| Argon2 | Algoritmo de hash para contraseñas; no es cifrado reversible. |
| HttpOnly | La cookie no puede leerse desde JavaScript; no elimina todos los riesgos del navegador. |
| CSRF | Control que ayuda a rechazar cambios inducidos desde otro sitio. No sustituye comprobar propietario. |
| Fallback | Respaldo por reglas cuando no se usa o no responde correctamente la IA. |
| MFA | Autenticación con más de un factor; en el formulario describe al hotel, no una función MFA de la app. |
| Migración | Cambio versionado de tablas o índices mediante Alembic. |
| Cuota IA | Límite de peticiones, no un tope de dólares ni de llamadas internas. |
| PMS | Sistema de gestión del alojamiento; no hay integración real con un PMS en este proyecto. |

Lectura aproximada: 996 palabras, eligiendo una alternativa por bloque. El tiempo real depende de ritmo, acciones y esperas.

Fuente editable: docs/practica3/video_script.json. Regenerar MD/PDF con python scripts/generate_video_script.py.
