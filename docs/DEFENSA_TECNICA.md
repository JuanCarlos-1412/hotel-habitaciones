# Preparación de la defensa individual

La defensa vale 40 puntos: dos preguntas de 15 puntos y explicación de aporte de 10. Cada integrante debe entender el funcionamiento completo y poder ubicar sus cambios reales.

## Demostración sugerida de cinco minutos

1. Encender MySQL en XAMPP, iniciar Django y mostrar inicio y listado.
2. Abrir `settings.py`: explicar backend mysql y variables de `.env` sin mostrar una contraseña privada.
3. Mostrar `models.py` y la tabla habitaciones en phpMyAdmin.
4. Crear la habitación 303 en la web, consultar su fila en SQL.
5. Editar precio y estado, consultar de nuevo; eliminar con confirmación y comprobar ausencia.
6. Intentar precio cero y número duplicado; explicar los errores.
7. Mostrar branch, commit y diff propio, y explicar una modificación que efectivamente realizó.

## Preguntas para practicar

**¿Qué es Django y por qué lo usamos?** Es el framework Python que organiza rutas, lógica de vistas, modelos, formularios y templates. En esta app recibe la solicitud y permite gestionar las habitaciones persistidas en MySQL.

**¿Qué contiene models.py?** La clase Habitacion describe campos, tipos, validadores, orden y restricciones. La tabla se llama habitaciones y `id` es su clave primaria; `numero` es único para evitar registrar dos veces la misma habitación.

**¿Qué hacen makemigrations y migrate?** El primero genera archivos con cambios del modelo; el segundo aplica esos cambios a la base. La migración inicial se incluye en el proyecto. No cambian solo el HTML.

**¿Cómo se conecta a XAMPP?** `DATABASES` usa `django.db.backends.mysql`; `mysqlclient` comunica Python con MySQL/MariaDB. `.env` proporciona nombre de base, usuario, contraseña, host y puerto. Apache solo hace falta para phpMyAdmin, no sirve la web Django.

**¿Cómo crea una habitación?** La vista recibe POST, construye CrearHabitacionForm, llama `is_valid()` y luego `save()`. El ORM inserta el registro en la tabla. Si es inválido muestra los errores sin guardarlo.

**¿Cómo edita sin insertar otra fila?** EditarHabitacionForm recibe `instance=habitacion`, por lo que `save()` actualiza ese objeto. El número queda fuera del formulario de edición y no se modifica aunque se envíe en el POST.

**¿Dónde está la consulta?** En `Habitacion.objects.all()`, los filtros del listado y `get_object_or_404` para la ficha. El ORM genera SQL; `get_object_or_404` responde 404 si el registro no existe.

**¿Por qué dos formularios?** Son clases y templates diferentes. Crear pide número y características; editar fija el número y prioriza estado y tarifa, cumpliendo la distinción de la pauta.

**¿Por qué precio DecimalField?** Conserva valores monetarios decimales con precisión definida. Un float puede introducir aproximaciones. Hay validador de mínimo 0.01 y CHECK de precio mayor que cero.

**¿Qué diferencia hay entre validación del formulario y restricción de BD?** El formulario muestra mensajes antes de guardar. UNIQUE y CHECK protegen la tabla incluso frente a determinadas escrituras por SQL. `save()` del modelo no llama automáticamente a `full_clean()`; no debe suponerse que todos los validadores se aplican fuera del formulario.

**¿Cómo se elimina?** GET muestra confirmación; POST ejecuta `delete()`. El formulario incluye token CSRF para impedir solicitudes de escritura sin el token válido.

**¿Qué es CSRF?** Una protección que verifica que el formulario de escritura lleva un token válido. El middleware y `{% csrf_token %}` trabajan juntos. No es un sistema de login.

**¿Cómo sabemos que los datos están en MySQL?** Comprobamos el backend configurado y consultamos directamente `hotel_db.habitaciones` después de cada acción. Reiniciar el servidor no debe borrar las filas.

**¿Qué hace urls.py?** Relaciona cada ruta con una vista. Los nombres de rutas permiten construir enlaces desde templates sin escribir rutas manualmente.

**¿Cuál fue tu aporte?** Explicar solo trabajo real: branch, commit, archivos y cambio concreto. Mostrar un antes/después y ejecutar la funcionalidad. Estudiar estas respuestas no sustituye implementar y comprender la parte propia.
