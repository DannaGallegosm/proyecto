import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from flask import send_from_directory



app = Flask(__name__)
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)


@app.route('/')
def login():
    return render_template('sitio/index.html')

@app.route('/login', methods=['POST'])
def login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    print("_usuario")
    print(_password)

    if _usuario=="admin" and _password=="2468":
       session['login'] =True
       session['usuario'] ="administrador"
       return redirect("/admin")

    return render_template ('sitio/index.html', mensaje="Usuario y Contraseña incorrectas")


@app.route('/admin')
def inicio():
    return render_template('sitio/admin.html')


@app.route('/clientes')
def clientes():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`")
    clientes=cursor.fetchall()
    conexion.commit()
    print(clientes)


    return render_template('sitio/clientes.html', clientes=clientes)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'), archivocss)

@app.route('/clientes/guardar', methods=['post'])
def clientes_guardar():
    nombre = request.form['txtNombre']
    celular = request.form['txtCelular']
    direccion = request.form['txtDireccion']
    cantidad = request.form['txtCantidad']
    fecha = request.form['txtFecha']

    sql= "INSERT INTO `clientes` (`id`, `nombre`, `celular`, `direccion`, `cantidad`, `fecha`) VALUES (NULL, %s,%s,%s,%s,%s);"
    datos =(nombre,celular,direccion,cantidad,fecha)
    conexion=mysql.connect()
    cursor =conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    print(nombre)
    print(celular)
    print(direccion)
    print(cantidad)
    print(fecha)
    return redirect('/clientes')



@app.route('/clientes/borrar', methods=['post'])
def clientes_borrar():
    _id = request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor =conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id =%s",(_id))
    conexion.commit()
    clientes=cursor.fetchall()
    conexion.commit()
    print(clientes)

    conexion=mysql.connect()
    cursor =conexion.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (_id))
    conexion.commit()
    return redirect('/clientes')

@app.route('/clientes/editar', methods=['post'])


@app.route('/ventas')
def ventas():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `datos_ventas`")
    ventas=cursor.fetchall()
    conexion.commit()
    print(ventas)
    return render_template('sitio/ventas.html', ventas=ventas)

@app.route('/datosventas')
def datosventas():


    return render_template('sitio/datosventas.html')


@app.route('/datosventas/guardar', methods=['post'])
def datosventas_guardar():
    _fecha=request.form['txtFecha']
    _nombre=request.form['txtNombre']
    _celular=request.form['txtCelular']
    _direccion=request.form['txtDireccion']
    _amarillos=request.form['txtAmarillos']
    _verdes=request.form['txtVerdes']
    _rojos=request.form['txtRojos']
    _total=request.form['txtTotal']

    sql= "INSERT INTO `datos_ventas` (`id`, `fecha`, `nombre`, `celular`, `direccion`, `amarillos`, `verdes`, `rojos`, `total`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s);"
    datos=(_fecha,_nombre,_celular,_direccion,_amarillos,_verdes,_rojos,_total)

    conexion=mysql.connect()
    cursor =conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_fecha)
    print (_nombre)
    print (_celular)
    print (_direccion)
    print (_amarillos)
    print (_verdes)
    print (_rojos)
    print (_total)

    return redirect('/ventas')

@app.route('/ventas/borrar', methods=['post'])
def ventas_borrar():
    _id = request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `datos_ventas` WHERE id =%s",(_id))
    venta=cursor.fetchall()
    conexion.commit()
    print(venta)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM datos_ventas WHERE id=%s",(_id))
    conexion.commit()

    return redirect('/ventas')

@app.route('/inventario/borrar', methods=['post'])
def inventario_borrar():
    _id = request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `inventario` WHERE id =%s",(_id))
    inventario=cursor.fetchall()
    conexion.commit()
    print(inventario)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM inventario WHERE id=%s",(_id))
    conexion.commit()

    return redirect('/inventario' )


@app.route('/inventario')
def inventario():
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `inventario`")
    inventario=cursor.fetchall()
    conexion.commit()
    print(inventario)
    return render_template('sitio/inventario.html', inventario=inventario)

    

@app.route('/inventario/guardar', methods=['post'])
def inventario_guardar():

    fecha = request.form['txtFecha']
    amarillos = request.form['txtAmarillos']
    rojos = request.form['txtRojos']
    verdes = request.form['txtVerdes']
    total = request.form['txtTotal']

    sql= "INSERT INTO `inventario` (`id`, `fecha`, `amarillos`, `rojos`, `verdes`, `total`) VALUES (NULL, %s,%s,%s,%s,%s);"
    datos =(fecha,amarillos,rojos,verdes,total)
    conexion=mysql.connect()
    cursor =conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    print(fecha)
    print(amarillos)
    print(rojos)
    print(verdes)
    print (total)

    return redirect('/inventario')

@app.route('/editclientes', methods=['POST'])
def editclientes():
    _id = request.form['txtID']
    print(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id=%s", (_id))
    clientes=cursor.fetchall()
    conexion.commit()

    return render_template ("sitio/editclientes.html", cliente=clientes[0])

@app.route('/actualizarclientes', methods=['POST'])
def actualizarclientes():

    _id = request.form['txtId']
    _nombre = request.form['txtNombre']
    _celular = request.form['txtCelular']
    _direccion = request.form['txtDireccion']
    _cantidad = request.form['txtCantidad']
    _fecha = request.form['txtFecha']

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("UPDATE clientes SET nombre=%s, celular=%s, direccion=%s, cantidad=%s, fecha=%s  WHERE id=%s", (_nombre,_celular,_direccion,_cantidad,_fecha,_id))
    conexion.commit()
    return redirect('/clientes')


if __name__=='__main__':
    app.secret_key="Danna123"
    app.run(debug=True)

    
