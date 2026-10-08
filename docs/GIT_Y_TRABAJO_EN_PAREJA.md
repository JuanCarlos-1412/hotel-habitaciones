# Git y participación de ambos integrantes

La pauta exige branches, commits y cambios propios. No inventar autores ni presentar todo el código generado como participación individual. Cada integrante debe revisar, entender y desarrollar mejoras reales en su parte, dejando evidencia identificable.

## Reparto propuesto

- Juan Carlos: modelo, conexión, migraciones, validaciones y demostración SQL. Puede agregar una regla de negocio acordada, sus pruebas y documentarla.
- Segundo integrante: vistas, templates, CSS y navegación. Puede implementar y probar una mejora propia, como paginación o un filtro por tipo.
- Ambos: integración, prueba con XAMPP y ensayo de defensa. Sustituir los nombres de ejemplo por los reales.

## Crear el repositorio una vez

Crear un repositorio vacío en GitHub, sin README inicial. Desde la carpeta del proyecto:

```powershell
git --version
git config --global user.name "Tu nombre real"
git config --global user.email "Tu correo de GitHub"
git init
git branch -M main
git add .
git commit -m "Agregar base del proyecto Hotel Aurora"
git remote add origin https://github.com/TU_USUARIO/hotel-habitaciones.git
git push -u origin main
```

Ese primer commit contiene una base preparada con asistencia; la participación posterior debe reflejar trabajo real. La URL se sustituye por la del repositorio creado. Nunca incluir `.env` o `.venv`.

## Trabajar desde un branch individual

Primer integrante:

```powershell
git switch -c juancarlos/backend
```

Realizar sus cambios, comprobar funcionamiento y revisar:

```powershell
git status
git diff
git add habitaciones/models.py habitaciones/forms.py habitaciones/migrations habitaciones/tests.py
git commit -m "Describir la mejora real realizada en backend"
git push -u origin juancarlos/backend
```

Segundo integrante, desde su computador:

```powershell
git clone https://github.com/TU_USUARIO/hotel-habitaciones.git
cd hotel-habitaciones
git config user.name "Nombre del segundo integrante"
git config user.email "Correo del segundo integrante"
git switch -c integrante2/interfaz
```

Hacer sus cambios y pruebas, luego:

```powershell
git diff
git add habitaciones/views.py habitaciones/templates habitaciones/static habitaciones/tests.py
git commit -m "Describir la mejora real realizada en interfaz"
git push -u origin integrante2/interfaz
```

Los nombres de archivos en `git add` se ajustan a lo que cada uno realmente modificó. Si `tests.py` fue modificado por ambos, resolver el conflicto conservando las pruebas necesarias.

## Integrar y mostrar evidencia

En GitHub abrir un Pull Request por branch hacia main, revisar y fusionar conservando los commits (evitar squash si necesitan mostrar todos los aportes). En cada computador:

```powershell
git switch main
git pull origin main
git branch -a
git log --all --graph --oneline --decorate
git shortlog -sn --all
git show ID_DEL_COMMIT
```

Guardar capturas del branch de cada integrante, sus commits, el diff y los Pull Requests. No ejecutar `git reset --hard` para resolver conflictos. Revisar los archivos con marcas de conflicto, corregirlos, probar y confirmar la resolución con `git add` y `git commit`.
