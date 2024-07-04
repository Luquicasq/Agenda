from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #//sqlalchemy --> conexion DB
from flask_cors import CORS #CORS deja que se acceda al sv y DB
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime #Tipos de dato
from sqlalchemy.orm import relationship #FKEY

app = Flask(__name__) #Se crea app de FLASK
cors = CORS(app, resources={r"/*": {"origins": "*"}}) #Se configura CORS
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://geetdb:fedorax@localhost/Final' #Conexion con DB
db = SQLAlchemy(app) #Instancia de SQLAlchemy + FLASK

class Tareas(db.Model): #Representa una table de la DB
    __tablename__ = 'tareas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    dia = db.Column(db.String)
    hora = db.Column(db.String)

class Rutina(db.Model): #Representa una table de la DB
    __tablename__ = 'rutina'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    dia = db.Column(db.String)
    hora = db.Column(db.String)

class Agenda(db.Model): 
    __tablename__ = 'agenda'
    id = Column(Integer, primary_key=True)
    pendiente = db.Column(db.Boolean)
    fkt = db.Column(Integer, ForeignKey("tareas.id"))
    fkr = db.Column(Integer, ForeignKey("rutina.id"))

@app.route('/crear_tarea/', methods=['POST'])
def crear_tarea():
    print("aaa")
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        horainicio = request.form['horai']
        horafin = request.form['horaf']
        hora = f"{horainicio}-{horafin}"

        dias_form = request.form.getlist('dia')
        dias = ', '.join(dias_form)

        tarea = Tareas(nombre=nombre, descripcion=descripcion, dia=dias, hora=hora)
        db.session.add(tarea)
        db.session.commit()

        tarea_id = tarea.id
        estado = True
        print(tarea_id)

        agenda = Agenda(fkt=tarea_id, pendiente=estado)
        db.session.add(agenda)
        db.session.commit()
    
    return jsonify({'mensaje': 'todo bien'})

@app.route('/modificar_tarea', methods=['POST'])
def modificar_tarea():
    tarea_id = request.form['tarea_id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    dia = request.form['dia']
    hora = request.form['hora']
    
    tarea = Tareas.query.get(tarea_id)
    if tarea:
        tarea.nombre = nombre
        tarea.descripcion = descripcion
        tarea.dia = dia
        tarea.hora = hora
        db.session.commit()
        return "Tarea modificada correctamente."
    else:
        return "No se encontró la tarea con ese ID."

@app.route('/modificar_rutina', methods=['POST'])
def modificar_rutina():
    rutina_id = request.form['rutina_id']
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    dia = request.form['dia']
    hora = request.form['hora']
    
    rutina = Rutina.query.get(rutina_id)
    if rutina:
        rutina.nombre = nombre
        rutina.descripcion = descripcion
        rutina.dia = dia
        rutina.hora = hora
        db.session.commit()
        return "Rutina modificada correctamente."
    else:
        return "No se encontró la rutina con ese ID."

@app.route('/formulario_modificar')
def formulario_modificar():
    return render_template('modificar.html')


if __name__ == '__main__':
    app.run(debug=True)