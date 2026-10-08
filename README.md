# Hotel Aurora — Django y MySQL

Aplicación académica de gestión de habitaciones para la Evaluación Sumativa 02 de Programación Backend. No requiere login. Incluye inicio, listado y filtros, ficha de detalle, formularios diferentes para crear y editar, y eliminación confirmada por POST.

## 1. Preparar Windows desde cero

1. Instalar Python 3.12 de 64 bits, marcar **Add Python to PATH**. Instalar VS Code y XAMPP.
2. Extraer este ZIP. En VS Code elegir **Archivo → Abrir carpeta → hotel_habitaciones**. La carpeta abierta debe contener `manage.py`.
3. Abrir **Terminal → Nueva terminal**. Los siguientes comandos están pensados para PowerShell:

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

No es necesario activar el entorno: usar su ejecutable evita el bloqueo de scripts de PowerShell. La instalación requiere Internet. No subir `.venv` ni `.env` a GitHub.

## 2. Preparar XAMPP y la base de datos

1. Abrir XAMPP Control Panel. Pulsar **Start** en MySQL y en Apache. Apache permite abrir phpMyAdmin; Django sirve la app por separado.
2. Abrir `http://localhost/phpmyadmin`. Seleccionar la pestaña SQL e introducir:

```sql
CREATE DATABASE IF NOT EXISTS hotel_db
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SELECT VERSION();
```

También puedes importar `sql/crear_base.sql`. Django 5.2 requiere MariaDB 10.5 o superior, o MySQL 8.0.11 o superior. Comprobar la versión real instalada; una instalación antigua de XAMPP puede necesitar actualización. No quitar la comprobación de versión de Django.

3. Abrir `.env`. La configuración de ejemplo usa usuario `root`, contraseña vacía y puerto `3306`, habituales en XAMPP local. Si tu instalación tiene otra contraseña o puerto, corregir esos valores. No añadir comillas al valor.
4. Ejecutar desde la carpeta de `manage.py`:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py cargar_demo
.\.venv\Scripts\python.exe manage.py runserver
```

5. Abrir **http://127.0.0.1:8000/**. Mantener la terminal abierta; detener con Ctrl+C. Para iniciar otro día basta encender MySQL y ejecutar `runserver`.

La migración inicial ya está incluida. Al modificar el modelo ejecutar `makemigrations habitaciones` y después `migrate`. No crear manualmente la tabla habitaciones: las migraciones son su fuente de definición. El comando `cargar_demo` es opcional y no sobrescribe habitaciones existentes.

## 3. Usar y demostrar el CRUD

- Crear: elegir **Nueva habitación**. Probar número 303, tipo doble, capacidad 2, precio 58000, piso 3 y estado disponible.
- Consultar: abrir el listado y la ficha. Buscar por número o filtrar por estado.
- Modificar: abrir **Editar**; cambiar precio a 62000 y estado a ocupada. La pantalla de edición tiene otro orden y no permite cambiar el número identificador.
- Eliminar: abrir **Eliminar**, revisar la confirmación y pulsar **Sí, eliminar habitación**. Abrir la página por GET no elimina.
- En phpMyAdmin seleccionar `hotel_db`, SQL y ejecutar tras cada acción:

```sql
SELECT * FROM habitaciones WHERE numero = 303;
```

Mostrar la fila tras crear, el nuevo precio tras editar y cero filas tras eliminar. Recargar phpMyAdmin y la web cuando corresponda. La persistencia debe demostrarse en tu MySQL real.

`sql/demostrar_crud.sql` agrega una demostración independiente de INSERT, SELECT, UPDATE y DELETE en la base. Ejecutar cada bloque de manera separada para observar el resultado también en la web. No ejecutar todo de una vez si quieres mostrar cada etapa.

## 4. Estructura y flujo

```text
hotel_habitaciones/
  manage.py
  requirements.txt
  .env.example
  hotel/
    settings.py       Conexión MySQL y configuración Django
    urls.py           Rutas principales
    wsgi.py           Entrada para servidor WSGI
    test_settings.py  Configuración aislada para pruebas
  habitaciones/
    models.py         Entidad Habitacion y restricciones
    forms.py          Formularios crear y editar
    views.py          Lógica CRUD
    urls.py           Rutas de habitaciones
    migrations/       Historial de esquema
    templates/habitaciones/  Páginas HTML
    static/habitaciones/     CSS local sin CDN
    management/commands/cargar_demo.py
    tests.py
  sql/
  docs/
```

El navegador solicita una URL; Django ejecuta la vista correspondiente. La vista usa el formulario para validar un POST, usa el modelo mediante el ORM para consultar MySQL y entrega un template HTML o una redirección. Los templates utilizan rutas por nombre y protección CSRF en los formularios.

## 5. Modelo y validaciones

| Campo | Tipo | Regla |
|---|---|---|
| id | BigAutoField | Clave primaria automática |
| numero | Entero positivo | Único, 1 a 9999 |
| tipo | Texto con opciones | Individual, doble, suite o familiar |
| capacidad | Entero | 1 a 10 personas |
| precio_noche | Decimal de 10 dígitos y 2 decimales | Mayor que cero, CLP |
| piso | Entero | 0 a 100 |
| estado | Texto con opciones | Disponible, ocupada o mantenimiento |
| descripcion | Texto | Opcional, máximo 500 caracteres en formularios |
| creada / actualizada | Fecha y hora | Gestión automática |

Los campos obligatorios, tipos, opciones, límites y número repetido se validan con ModelForm. Hay restricciones CHECK y UNIQUE en la BD para proteger también valores esenciales al escribir directamente por SQL. La longitud de descripción se valida en formularios; un TEXT de MySQL no impone ese límite automáticamente. `save()` de un modelo no ejecuta por sí mismo `full_clean()`.

## 6. Verificar

Pruebas independientes, sin requerir MySQL (no sustituyen la demostración MySQL):

```powershell
.\.venv\Scripts\python.exe manage.py test --settings=hotel.test_settings
```

Pruebas contra MySQL, con el servidor iniciado y un usuario con permiso para crear y borrar la BD de pruebas `test_hotel_db`:

```powershell
.\.venv\Scripts\python.exe manage.py test
```

Django usa una base de pruebas separada; no usar `--keepdb` contra una BD de trabajo. Las pruebas cubren CRUD web con persistencia, validaciones, restricción de precio en BD, filtros, CSRF y 404.

## 7. Errores habituales

- `No module named django`: usar el Python de `.venv` e instalar requirements.
- `Unknown database hotel_db`: crear la BD antes de `migrate`.
- `Access denied`: revisar usuario y contraseña en `.env`; reiniciar runserver tras cambios.
- `Can't connect ... 10061`: iniciar MySQL; verificar el puerto de XAMPP y `.env`.
- `Table ... doesn't exist`: ejecutar `migrate` y confirmar la BD configurada.
- `mysqlclient` falla al instalar: usar Python 3.12 de 64 bits y pip actualizado. Si no hay wheel para tu plataforma, seguir https://github.com/PyMySQL/mysqlclient#install y sus requisitos de compilación; no modificar archivos internos de Django.
- Puerto 8000 ocupado: `manage.py runserver 8001` y abrir `http://127.0.0.1:8001/`.
- Archivo `.env` no visible: habilitar extensiones de archivo en Windows; evitar `.env.txt`.

## 8. Preparar la entrega

Leer `docs/GIT_Y_TRABAJO_EN_PAREJA.md`, `docs/DEFENSA_TECNICA.md` y `docs/CHECKLIST_PAUTA.md`. Git y la defensa requieren participación real de los integrantes; este ZIP no constituye evidencia de sus commits. Entregar código y migraciones sin entorno virtual ni contraseñas. No hace falta crear un superusuario.

Este proyecto usa el servidor de desarrollo local. No publicarlo en Internet con DEBUG activado y credenciales locales.

## Referencias

- Pauta suministrada: Evaluación Sumativa-02-Backend-B.docx.
- Django 5.2, bases de datos: https://docs.djangoproject.com/en/5.2/ref/databases/
- Formularios de modelo: https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/
- Migraciones: https://docs.djangoproject.com/en/5.2/topics/migrations/
