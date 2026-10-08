# Verificación realizada

Probado con Django 5.2.18 y una base SQLite aislada destinada solo a pruebas.

- Cinco pruebas automáticas aprobadas: CRUD web y persistencia, validaciones, restricción de precio en BD, CSRF y registros inexistentes, filtros.
- Comprobación de configuración Django sin incidencias en el entorno de pruebas.
- Migración inicial generada.

No se ejecutó conexión real con MySQL/MariaDB en este entorno: no hay servidor instalado y faltan dependencias nativas para compilar mysqlclient. La configuración normal de la aplicación usa MySQL. Completar instalación, migrate y demostración CRUD en el XAMPP del computador de presentación antes de entregar.

La participación Git y la defensa deben realizarse personalmente; se incluyen guías, no evidencia fabricada.
