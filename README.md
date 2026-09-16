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
````markdown
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

```

Solo una precisión técnica: para que funcione correctamente, el `ServerName` del VirtualHost de Apache debería coincidir también con `incidencias_ies_teis`.
```
