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