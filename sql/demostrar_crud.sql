-- Ejecutar en phpMyAdmin después de las migraciones.
USE hotel_db;
SHOW TABLES;
SHOW CREATE TABLE habitaciones;
-- C: crea una habitación para la demostración SQL. Usar otro número si ya existe.
INSERT INTO habitaciones (numero,tipo,capacidad,precio_noche,piso,estado,descripcion,creada,actualizada)
VALUES (909,'doble',2,60000,9,'disponible','Demostración SQL',NOW(),NOW());
-- R: comprueba también esta habitación en la web.
SELECT * FROM habitaciones WHERE numero=909;
-- U: actualiza y recarga la ficha web.
UPDATE habitaciones SET precio_noche=65000, estado='ocupada', actualizada=NOW() WHERE numero=909;
SELECT numero,precio_noche,estado FROM habitaciones WHERE numero=909;
-- D: ejecutar únicamente al terminar la demostración.
DELETE FROM habitaciones WHERE numero=909;
SELECT * FROM habitaciones WHERE numero=909;
-- Para verificar el CRUD WEB: consultar el número creado en la interfaz tras cada paso.
SELECT id,numero,tipo,capacidad,precio_noche,estado FROM habitaciones ORDER BY numero;
