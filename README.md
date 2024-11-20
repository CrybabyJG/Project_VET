# Proyecto Integrador 4: Sistema Backend de clinica veterinaria desarrollado en django

## Integrantes:
- Mauricio Josué Mercado González. 💀
- Adhriell Sarid Medina Flores. 😋
- Maykel de Jesús Zuniga Dávila. 😤
## Instrucciones 📕
Este archivo contiene los pasos necesarios para poner en marcha el proyecto. Sigue cada paso para configurar tu entorno de desarrollo.

## Requisitos Previos 📋
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) instalado en tu sistema.
- [Python](https://www.python.org/downloads/) instalado en tu sistema.
- [Postman](https://www.postman.com/downloads/) para consumir las API.
- [Papertrail](https://papertrailapp.com/) para la visualización de los logs.
- [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver15) para la creación de la base de datos.

## Pasos de Configuración 🛠️

### 1. Crear un Entorno de Desarrollo en Conda
Primero, crea un entorno en Conda con Python 3.12:
```bash
conda create -n mi_entorno python=3.12
```
Activa el entorno de desarrollo creado:
```bash
conda activate mi_entorno
```
### 2. Instalar las Dependencias
Instala las dependencias necesarias para el proyecto:
```bash
pip install -r requirements.txt
```
### 3. Crear la Base de Datos
Crea una base de datos en SqlserverManagementStudio con el nombre que desees.
### 4. Crear una cuenta en Papertrail
Crea una cuenta en [Papertrail](https://papertrailapp.com/) para obtener tu Puerto y Host y visualizar los logs de la aplicación.
### 5. Configurar las Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:
```bash
DB_NAME = 'El nombre de tu base de datos'
DB_HOST = 'El host de tu base de datos'
HOST_PAPERTRAIL = 'El host de tu Papertrail'
PORT_PAPERTRAIL = 'El puerto de tu Papertrail'
```
### 6. Realiza las migraciones
Crea las migraciones de los modelos.
```bash
python manage.py makemigrations 
```
Aplica las migraciones.
```bash
python manage.py migrate
```
### 7. Ejecutar el Proyecto
Ejecuta el proyecto con la configuracion de desarrollo:
```bash
python manage.py runserver --settings=config.dev
```
### 8. Crear un superusuario
Crea un superusuario para acceder al panel de administración de Django `/admin` o usarlo para generar un token.
```bash
python manage.py createsuperuser
```
### 9. Genera un token
Genera un token con swagger para poder consumir las API según tu superusuario creado o un usuario con los permisos que hayas asignado en el panel de administración.
Puedes generar el token y encontrar la documentación de las API en la URL `/swagger`.
### 8. Consumir las API
Utiliza Postman para consumir las API, en la opción de autorización, selecciona bearer token e ingresa el token generado en el paso anterior



