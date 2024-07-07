--Nombre:
Agenda

--Descripción:
Agenda es una forma práctica de organizar las tareas pendientes a nivel semanal diseñada para personas, empresas o proyectos.

--Instalación:
Para hacer funcionar la aplicación hay que levantar una base de datos con postgresql con tres tablas: tareas, rutina y agenda:

tareas y agenda se crean así:
CREATE TABLE nombre_tabla (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(200),
    dia VARCHAR(200),
    hora VARCHAR(20)
);

agenda se crea así:
CREATE TABLE agenda (
    id SERIAL PRIMARY KEY,
    fkt INT,
    FOREIGN KEY (fkt) REFERENCES tareas(id)
    fkr INT,
    FOREIGN KEY (fkr) REFERENCES rutina(id)
);

También hay que instalar las dependencias con:
pip install -r requirements.txt

Con las dependencias ya instaladas y la base de datos corriendo el úlitmo paso es ejecutar app.py desde una terminar de python.

--Uso:
El uso es intuitivo, hay una pagina principal con la visualización de los eventos y 3 ventanas para crear mas, editar los existentes o borrarlos.