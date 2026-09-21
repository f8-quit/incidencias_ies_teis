# MANUAL DE INSTALACIÓN DE LA APP WEB

## Decisiones de proyecto

| Elemento | Decisión | Versión | Justificación |
|---|---|---|---|
| Sistema Operativo | Ubuntu | 24.04 | Entorno Linux real |
| Servidor Web | Apache | 2 | Sencillez y popularidad |
| Base de datos | MySQL | 2 | Experiencia previa |
| Lenguaje servidor | Python | 3 | Uso muy extendido |
| Framework | Flask | 3 | Sencillez y pensado para uso web |
| Control de versiones | Git | 2 | Uso muy extendido |
| Documentación | Markdown | - | Muy utilizado con GitHub |

## ¿Qué hace un servidor web?

Un servidor web es un programa que recibe peticiones de los navegadores y devuelve páginas o recursos web.

## Proceso de instalación/puesta en marcha

1. Actualización del sistema:

```bash
sudo apt update && sudo apt upgrade
```

2. Instalación de Git:

```bash
sudo apt install git
```

3. Instalación de VSCode + plugins:
    - Markdown All in One.

4. Instalación de Apache2:

```bash
sudo apt install apache2 -y
```

5. Cambio de permisos de la carpeta `/var/www/html`:

```bash
sudo chown -R $USER:$USER /var/www/html
sudo chmod -R u=rwX,go=rX /var/www/html
```

6. Creación del directorio `/var/www/incidencias_ies_teis`.

7. Creación del archivo de configuración en `/etc/apache2/sites-available/incidencias_ies_teis.conf`:

```bash
sudo nano /etc/apache2/sites-available/incidencias_ies_teis.conf
```

Dentro del archivo se añade la configuración del VirtualHost:

```apache
<VirtualHost *:80>
    ServerName incidencias_ies_teis
    DocumentRoot /var/www/incidencias_ies_teis

    <Directory /var/www/incidencias_ies_teis>
        Require all granted
    </Directory>
</VirtualHost>
```

Con esta configuración se indica a Apache el nombre del sitio y el directorio donde se encuentran los archivos de la página web.

8. Desactivación del sitio por defecto de Apache:

```bash
sudo a2dissite 000-default.conf
```

9. Activación del sitio `incidencias_ies_teis`:

```bash
sudo a2ensite incidencias_ies_teis.conf
```

10. Comprobación de la sintaxis de la configuración de Apache:

```bash
sudo apache2ctl configtest
```

11. Recarga de Apache:

```bash
sudo systemctl reload apache2
```

12. Comprobación de los sitios habilitados:

```bash
ls /etc/apache2/sites-enabled/
```

Resultado:

```text
incidencias_ies_teis.conf
```

13. Comprobación de los archivos y directorios principales de Apache:

```bash
ls /etc/apache2/
```
14. Configuración del nombre local para acceder desde el navegador.

Para poder acceder a la página web mediante:

`http://incidencias_ies_teis`

se modifica el archivo `/etc/hosts`:

```bash
sudo nano /etc/hosts
````

Añadiendo la siguiente línea:

```text
127.0.0.1 incidencias_ies_teis
```

El archivo queda de la siguiente forma:

```text
127.0.0.1 localhost
127.0.1.1 pc-xx
127.0.0.1 incidencias_ies_teis

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

De esta forma, el nombre `incidencias_ies_teis` queda asociado a la dirección local `127.0.0.1`.


15. Instalar MySQL Server

```
sudo apt install mysql-server
```

16. Acceso a MySQL como administrador:

```bash
sudo mysql
```

Al acceder correctamente aparece el prompt de MySQL:

```text
mysql>
```

17. Creación de la base de datos `incidencias`:
```sql
CREATE DATABASE incidencias;
```

Resultado:

```text
Query OK, 1 row affected
```

18. Creación del usuario `incidencias` para conexiones desde `localhost`:

```sql
CREATE USER 'incidencias'@'localhost' IDENTIFIED BY 'incidencias';
```

Resultado:

```text
Query OK, 0 rows affected
```

Durante la práctica se creó por error un usuario llamado `f8-quit`:

```sql
CREATE USER "f8-quit";
```

Como no era el usuario correcto, se eliminó:

```sql
DROP USER "f8-quit";
```

19. Asignación de todos los privilegios de la base de datos `incidencias` al usuario creado:

```sql
GRANT ALL PRIVILEGES ON incidencias.* TO 'incidencias'@'localhost';
```

Resultado:

```text
Query OK, 0 rows affected
```

20. Aplicación de los cambios en los privilegios:

```sql
FLUSH PRIVILEGES;
```

Resultado:

```text
Query OK, 0 rows affected
```

21. Comprobación de que la base de datos se creó correctamente:

```sql
SHOW DATABASES;
```

Resultado:

```text
+--------------------+
| Database           |
+--------------------+
| incidencias        |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

Inicialmente se probó por error:

```sql
SHOW DATABASE;
```

pero MySQL devolvió un error de sintaxis, ya que el comando correcto es `SHOW DATABASES;`.

22. Comprobación de los usuarios existentes en MySQL:

```sql
SELECT user, host FROM mysql.user;
```

Resultado:

```text
+------------------+-----------+
| user             | host      |
+------------------+-----------+
| debian-sys-maint | localhost |
| incidencias      | localhost |
| mysql.infoschema | localhost |
| mysql.session    | localhost |
| mysql.sys        | localhost |
| root             | localhost |
+------------------+-----------+
```

De esta forma se comprueba que existe el usuario `incidencias@localhost`.

Durante la comprobación también se probaron:

```sql
SHOW USERS;
SHOW USER;
```

pero ambos comandos devolvieron un error de sintaxis.

23. Comprobación de los privilegios del usuario actual:

```sql
SHOW GRANTS;
```

Este comando muestra los privilegios del usuario con el que está abierta la sesión. En este caso, `root@localhost`.

24. Comprobación de los privilegios asignados al usuario `incidencias`:

```sql
SHOW GRANTS FOR 'incidencias'@'localhost';
```

Resultado:

```text
+----------------------------------------------------------------------+
| Grants for incidencias@localhost                                     |
+----------------------------------------------------------------------+
| GRANT USAGE ON *.* TO `incidencias`@`localhost`                      |
| GRANT ALL PRIVILEGES ON `incidencias`.* TO `incidencias`@`localhost` |
+----------------------------------------------------------------------+
```

Con esta comprobación se verifica que el usuario `incidencias` tiene todos los privilegios sobre la base de datos `incidencias`.

Durante la primera comprobación se escribió por error `incidecias` en lugar de `incidencias`:

```sql
SHOW GRANTS FOR 'incidecias'@'localhost';
```

MySQL indicó que no existían privilegios definidos para ese usuario porque el nombre estaba mal escrito.

25. Selección de la base de datos `incidencias`:

```sql
USE incidencias;
```

Resultado:

```text
Database changed
```

Con este comando se selecciona la base de datos `incidencias` para trabajar sobre ella.

26. Creación de la tabla `registro`:

```sql
CREATE TABLE registro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aula VARCHAR(30),
    descripcion TEXT,
    usuario VARCHAR(20),
    estado VARCHAR(30)
);
```

Resultado:

```text
Query OK, 0 rows affected
```

La tabla `registro` queda formada por los siguientes campos:

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `INT` | Identificador único de cada registro. Se incrementa automáticamente y actúa como clave primaria. |
| `aula` | `VARCHAR(30)` | Almacena el aula relacionada con la incidencia. |
| `descripcion` | `TEXT` | Almacena la descripción de la incidencia. |
| `usuario` | `VARCHAR(20)` | Almacena el usuario relacionado con la incidencia. |
| `estado` | `VARCHAR(30)` | Almacena el estado actual de la incidencia. |

27. Inserción de datos de prueba en la tabla `registro`:

Se añaden dos incidencias para comprobar que la tabla funciona correctamente.

Primera incidencia:

```sql
INSERT INTO registro (aula, descripcion, usuario, estado)
VALUES ('Taller1', 'PC 24 no arranca', 'ifpereira', 'ABIERTA');
```

Resultado:

```text
Query OK, 1 row affected
```

Segunda incidencia:

```sql
INSERT INTO registro (aula, descripcion, usuario, estado)
VALUES ('Taller2', 'Monitor 2 no funciona', 'isfariña', 'ABIERTA');
```

Resultado:

```text
Query OK, 1 row affected
```

28. Comprobación de los registros almacenados:

```sql
SELECT * FROM registro;
```

Resultado:

```text
+----+---------+-----------------------+-----------+---------+
| id | aula    | descripcion           | usuario   | estado  |
+----+---------+-----------------------+-----------+---------+
|  1 | Taller1 | PC 24 no arranca      | ifpereira | ABIERTA |
|  2 | Taller2 | Monitor 2 no funciona | isfariña  | ABIERTA |
+----+---------+-----------------------+-----------+---------+
2 rows in set
```

Con esta consulta se comprueba que los dos registros se han insertado correctamente y que el campo `id` se ha generado automáticamente mediante `AUTO_INCREMENT`.

28. Instalación de Python y de las herramientas necesarias para crear entornos virtuales:

```bash
sudo apt install python3 python3-pip python3-venv -y
```

29. Creación del entorno virtual de Python:

Desde el directorio del proyecto se crea un entorno virtual llamado `venv`:

```bash
python3 -m venv venv
```

Después se activa:

```bash
source /var/www/incidencias_ies_teis/venv/bin/activate
```

Al activar el entorno virtual, las dependencias de Python que se instalen quedarán asociadas al proyecto.

30. Instalación de Flask y del conector de MySQL para Python:

```bash
pip install flask
```

```bash
pip install mysql-connector-python
```

Para comprobar los paquetes instalados:

```bash
pip list
```

Se guardan las dependencias del proyecto en el archivo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

31. Creación del archivo `.gitignore`:

Se crea un archivo llamado `.gitignore` para evitar subir al repositorio archivos que no deben formar parte del proyecto.

Contenido:

```gitignore
venv/
**/__pycache__/
*.pyc
.env
```

32. Rutina de trabajo con Flask:

Cada vez que se vaya a trabajar con la aplicación:

```bash
cd /var/www/incidencias_ies_teis
source venv/bin/activate
python app.py
```

El comando:

```bash
python app.py
```

lanza la aplicación Flask.

Al terminar la ejecución se detiene con:

```text
Ctrl + C
```

Después se sale del entorno virtual:

```bash
deactivate
```

33. Creación de la primera aplicación Python/Flask:

Se crea el archivo `app.py` con el siguiente contenido:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "<h1>Incidencias IES Teis</h1>"

if __name__ == "__main__":
    app.run(debug=True)
```

La ruta `/` devuelve directamente un encabezado HTML desde Flask.

34. Activación de los módulos de Apache necesarios:

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo systemctl restart apache2
```

Con esto quedan activados los módulos `proxy` y `proxy_http` de Apache.

35. Migración del formulario HTML a Python/Flask:

Se crea una carpeta llamada `templates` y se mueve dentro de ella el archivo `index.html`.

La estructura del proyecto pasa a incluir:

```text
incidencias_ies_teis/
├── app.py
├── requirements.txt
├── venv/
└── templates/
    └── index.html
```

Se modifica `app.py` para que Flask devuelva el formulario utilizando `render_template`:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
```

36. Comprobación de que Flask devuelve el formulario:

Se abre en el navegador:

```text
http://incidencias_ies_teis:5000/
```

Al acceder a esta dirección se comprueba que el formulario `index.html` es devuelto por Flask.

37. Preparación del formulario para enviar los datos a Flask:

El formulario debe enviar los datos mediante `POST` a la ruta `/incidencia`:

```html
<form action="/incidencia" method="post">
```

Los valores se identifican mediante el atributo `name` de cada campo del formulario:

```text
nombre
email
tipo
prioridad
descripcion
```

38. Recepción de los datos del formulario:

Se añade `request` a las importaciones de Flask:

```python
from flask import Flask, render_template, request
```

Después se añade una nueva ruta en `app.py` para recibir los datos enviados por el formulario:

```python
@app.route("/incidencia", methods=["POST"])
def crear_incidencia():
    nombre = request.form["nombre"]
    email = request.form["email"]
    tipo = request.form["tipo"]
    prioridad = request.form["prioridad"]
    descripcion = request.form["descripcion"]

    print("Nombre: " + nombre)
    print("Email: " + email)
    print("Tipo: " + tipo)
    print("Prioridad: " + prioridad)
    print("Descripción: " + descripcion)

    return "Incidencia recibida"
```

El archivo `app.py` queda de la siguiente forma:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/incidencia", methods=["POST"])
def crear_incidencia():
    nombre = request.form["nombre"]
    email = request.form["email"]
    tipo = request.form["tipo"]
    prioridad = request.form["prioridad"]
    descripcion = request.form["descripcion"]

    print("Nombre: " + nombre)
    print("Email: " + email)
    print("Tipo: " + tipo)
    print("Prioridad: " + prioridad)
    print("Descripción: " + descripcion)

    return "Incidencia recibida"

if __name__ == "__main__":
    app.run(debug=True)
```

Cuando el formulario realiza una petición `POST` a `/incidencia`, Flask recoge los valores mediante `request.form` y los muestra en la terminal con `print()`.