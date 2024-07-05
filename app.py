from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #sqlalchemy --> conexion DB
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
    dias = db.Column(db.String)
    hora = db.Column(db.String)

class Agenda(db.Model): 
    __tablename__ = 'agenda'
    id = Column(Integer, primary_key=True)
    pendiente = db.Column(db.Boolean)
    fkt = db.Column(Integer, ForeignKey("tareas.id"))
    fkr = db.Column(Integer, ForeignKey("rutina.id"))
    tarea = relationship('Tareas', foreign_keys=[fkt])
    rutina = relationship('Rutina', foreign_keys=[fkr])

@app.route('/agenda/', methods=['GET'])
def conseguir_agenda():
    pendientes = Agenda.query.filter_by(pendiente=True).all()
    pendientes_dic = {}

    for pendiente in pendientes:
        if pendiente.tarea:
            nombre = pendiente.tarea.nombre
            hora = pendiente.tarea.hora
            dia = pendiente.tarea.dia
        elif pendiente.rutina:
            nombre = pendiente.rutina.nombre
            hora = pendiente.rutina.hora
            dia = pendiente.rutina.dias


        hora_inicio= hora.strip()

        if dia not in pendientes_dic:
            pendientes_dic[dia] = {}

        if hora_inicio not in pendientes_dic[dia]:
            pendientes_dic[dia][hora_inicio] = []

        pendientes_dic[dia][hora_inicio].append(nombre)
        
    return jsonify(pendientes_dic)

@app.route('/crear_tarea/', methods=['POST'])
def crear_tarea():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        horainicio = request.form['horai']
        horafin = request.form.get('horaf', '')
        if horafin == '':
            hora = horainicio
        else:
            hora = f"{horainicio}-{horafin}"

        dias_form = request.form.getlist('dia')
        dias = '-'.join(dias_form)

        tarea = Tareas(nombre=nombre, descripcion=descripcion, dia=dias, hora=hora)
        db.session.add(tarea)
        db.session.commit()

        tarea_id = tarea.id
        estado = True

        agenda = Agenda(fkt=tarea_id, pendiente=estado)
        db.session.add(agenda)
        db.session.commit()
    
    return jsonify({'mensaje': 'todo bien'})

@app.route('/crear_rutina/', methods=['POST'])
def crear_rutina():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        horainicio = request.form['horai']
        horafin = request.form.get('horaf', '')
        if horafin == '':
            hora = horainicio
        else:
            hora = f"{horainicio}-{horafin}"

        dias_form = request.form.getlist('dia')
        dias = '-'.join(dias_form)

        rutina = Rutina(nombre=nombre, descripcion=descripcion, dias=dias, hora=hora)
        db.session.add(rutina)
        db.session.commit()

        rutina_id = rutina.id
        estado = True

        agenda = Agenda(fkr=rutina_id, pendiente=estado)
        db.session.add(agenda)
        db.session.commit()
    
    return jsonify({'mensaje': 'todo bien'})

@app.route('/verificar_tarea_duplicada/', methods=['GET'])
def verificar_tarea():
    nombre = request.args.get('nombre')
    tarea = Tareas.query.filter_by(nombre=nombre).first()
    if tarea:
        return jsonify({'existe': True})
    else:
        return jsonify({'existe': False})

@app.route('/verificar_rutina_duplicada/', methods=['GET'])
def verificar_rutina():
    nombre = request.args.get('nombre')
    tarea = Rutina.query.filter_by(nombre=nombre).first()
    if tarea:
        return jsonify({'existe': True})
    else:
        return jsonify({'existe': False})

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