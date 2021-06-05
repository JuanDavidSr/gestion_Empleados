from flask import Flask
from flask import render_template, request, redirect, url_for,flash
from flaskext.mysql import MySQL 
from flask import send_from_directory
from datetime import datetime
import os
from conexion import conexion
from werkzeug.utils import validate_arguments

@conexion.app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
   return send_from_directory(conexion.app.config['carpeta'],nombreFoto)

@conexion.app.route('/')
def index():   
    sql="SELECT * FROM empleados"
    conn=conexion.mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados= cursor.fetchall()

    conn.commit()
    return render_template('empleados/index.html', empleados =empleados )

@conexion.app.route('/destroy/<int:id>')
def destroy(id):
    sql="SELECT foto FROM empleados WHERE id=%s"
    conn= conexion.mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,id)
    fila= cursor.fetchall()

    os.remove(os.path.join(conexion.app.config['carpeta'],fila[0][0]))
    sql="DELETE FROM empleados WHERE id=%s"
    cursor.execute(sql,id)
    conn.commit()
    return redirect('/')

@conexion.app.route('/edit/<int:id>')
def edit(id):
    sql="SELECT * FROM empleados WHERE id=%s"
    conn=conexion.mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,id)
    empleados= cursor.fetchall()
    conn.commit
    
    return render_template('empleados/edit.html',empleados=empleados)


@conexion.app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    _cedula = request.form['txtCedula']
    _estado= request.form['txtEstado']
    id=request.form['txtID']
    sql="UPDATE empleados SET  nombre =%s,cedula =%s, correo=%s, estado=%s Where id=%s"

    if  _nombre=='' or _correo=='' or _foto=='' or _cedula=='' or _estado== '':
        flash('Recuerda deber llenar todos los datos')
        return redirect('edit/'+id)

    datos = (_nombre,_cedula,_correo,_estado,id)
    conn=conexion.mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!= '':
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)
        
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        fila= cursor.fetchall()

        os.remove(os.path.join(conexion.app.config['carpeta'],fila[0][0]))
        cursor.execute("UPDATE empleados SET  foto=%s WHERE id=%s", (nuevoNombreFoto,id))
        conn.commit()

    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')
 

@conexion.app.route('/create')
def create():
  return render_template('empleados/create.html')

@conexion.app.route('/sueldos')
def sueldos():
    
  return render_template('empleados/sueldo.html')

@conexion.app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    _cedula= request.form['txtCedula']
    _estado = request.form['txtEstado']

    conn=conexion.mysql.connect()
    cursor = conn.cursor()
    
    if  _nombre=='' or _correo=='' or _foto=='' or _cedula=='' or _estado== '':
        flash('Recuerda deber llenar todos los datos')
        return redirect(url_for('create'))

    if(_cedula != ''):
        validate="SELECT cedula FROM empleados WHERE cedula = %s"
        validacion=cursor.execute(validate,_cedula)
        if(validacion != 0):
            flash('Esta cedula ya se encuentra registrada en el sistema')
            return redirect(url_for('create'))
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!= '':
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+ nuevoNombreFoto)
    
    
    sql="INSERT INTO `empleados`(`id`, `nombre`, `cedula`, `correo`, `foto`, `estado`) VALUES (null,%s,%s,%s,%s, %s)"
    datos = (_nombre,_cedula,_correo,nuevoNombreFoto,_estado)
    cursor.execute(sql,datos)
    

    conn.commit()

    return redirect('/')

@conexion.app.route('/filter',methods=['POST'])
def filter():    
    _filtEstado = request.form['FiltEstado']
   
    if(_filtEstado != ''):
        sql="SELECT * FROM `empleados` WHERE `estado` = '" + _filtEstado+ "'"
    

    if(_filtEstado == '' ):
        sql="SELECT * FROM empleados"
    conn=conexion.mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados= cursor.fetchall()
    conn.commit()
    return render_template('empleados/index.html', empleados =empleados )

@conexion.app.route('/search',methods=['POST'])
def search():    
    _filtEstado = request.form['searchName']
    sql="SELECT * FROM `empleados` WHERE `nombre` = '" + _filtEstado+ "'"
    if(_filtEstado == ''):
        sql="SELECT * FROM empleados"
    conn=conexion.mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados= cursor.fetchall()
    conn.commit()
    return render_template('empleados/index.html', empleados =empleados )
    
if __name__ == '__main__': 
    conexion.app.run(debug= True)