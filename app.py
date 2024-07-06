from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy #sqlalchemy --> conexion DB
from flask_cors import CORS #CORS deja que se acceda al sv y DB
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, delete #Tipos de dato
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

@app.route('/verificar_evento_duplicado')
def verificar_evento_duplicado():
    nombre_crear = request.args.get('nombre')
    print(nombre_crear)
    tarea = Tareas.query.filter_by(nombre=nombre_crear).first()
    rutina = Rutina.query.filter_by(nombre=nombre_crear).first()

    if tarea:
        return jsonify({'existetarea': True})
    if rutina:
        return jsonify({'existerutina': True})
    return jsonify({'existe': False})



@app.route('/eliminar_de_agenda')
def eliminar_de_agenda():
    #Borrar elimina el registro correspondiente en Agenda y en Tareas
    nombre_borrar = request.args.get('nombre')
    tarea = Tareas.query.filter_by(nombre=nombre_borrar).first()
    rutina = Rutina.query.filter_by(nombre=nombre_borrar).first()

    if tarea:
        db.session.query(Agenda).filter_by(fkt=tarea.id).delete()
        db.session.commit()

        db.session.delete(tarea)
        db.session.commit()
        return jsonify({'eliminado': True})
    if rutina:
        db.session.query(Agenda).filter_by(fkr=rutina.id).delete()
        db.session.commit()
        
        db.session.delete(rutina)
        db.session.commit()
        return jsonify({'eliminado': True})
    return jsonify({'eliminado': False})

@app.route('/modificar_evento', methods=['POST'])
def modificar_evento():
    nombre_viejo = request.form['nombre_viejo']
    nombre_nuevo = request.form['nuevo_nombre']
    descripcion = request.form['descripcion']
    horainicio = request.form.get('horai', '')
    horafin = request.form.get('horaf', '')
    if horafin == '':
        hora = horainicio
    else:
        hora = f"{horainicio}-{horafin}"

    dias_form = request.form.getlist('dia')
    dias = '-'.join(dias_form)

    tarea = Tareas.query.filter_by(nombre=nombre_viejo).first()
    rutina = Rutina.query.filter_by(nombre=nombre_viejo).first()
    if tarea:
        if len(dias_form) > 1:
            return jsonify({'exito': False})
        if nombre_nuevo:
            tarea.nombre = nombre_nuevo
        if descripcion:
            tarea.descripcion = descripcion
        if hora:
            tarea.hora = hora
        if dias:
            tarea.dia = dias
        db.session.commit()
    
    elif rutina:
        if len(dias_form) < 2:
            return jsonify({'exito': False})
        if nombre_nuevo:
            rutina.nombre = nombre_nuevo
        if descripcion:
            rutina.descripcion = descripcion
        if hora:
            rutina.hora = hora
        if dias:
            rutina.dia = dias
        db.session.commit()
    else:
        return jsonify({'existe': False})
    return jsonify({'exito': True})

if __name__ == '__main__':
    app.run(debug=True)