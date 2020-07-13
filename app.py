#!/usr/bin/env python
import csv
from datetime import datetime

from flask import Flask, render_template, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap

from forms import LoginForm, SaludarForm, RegistrarForm, ConsultaxPais, ConsultaxEdad, ConsultaxFecha, AgregarNuevoCliente, AgregarNuevoProducto
from wtforms import SelectField


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'un string que funcione como llave'


#  -------------- AUTOR --------------- #
@app.route('/Sobre')
def sobre():
    return render_template('sobre.html')



                
@app.route('/')
def index():
    return render_template('index.html', fecha_actual=datetime.utcnow())


@app.route('/saludar', methods=['GET', 'POST'])
def saludar():
    formulario = SaludarForm()
    if formulario.validate_on_submit():  # POST valida el ingreso 
        print(formulario.usuario.name)
        return redirect(url_for('saludar_persona', usuario=formulario.usuario.data))
    return render_template('saludar.html', form=formulario)


@app.route('/saludar/<usuario>')
def saludar_persona(usuario):
    return render_template('usuarios.html', nombre=usuario)



@app.errorhandler(404)
def no_encontrado(e): # Cuando no encuentra la pagina devuelve template 404 recurso no encontrado
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_interno(e): # Cuando sucede un error que no contempla ninguna opcion devuelve template 500 error en el servidor
    return render_template('500.html'), 500


@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        with open('usuarios') as archivo: #abre el csv
            archivo_csv = csv.reader(archivo)  #lee el csv
            registro = next(archivo_csv)
            while registro:
                if formulario.usuario.data == registro[0] and formulario.password.data == registro[1]:  #si valida el usuario y pass 
                    flash('Bienvenido')   
                    session['username'] = formulario.usuario.data  
                    return render_template('ingresado.html')  # devulve el template "ingresado corerctamente"
                registro = next(archivo_csv, None)
            else:
                flash('Revisá nombre de usuario y contraseña') # si no valida las credenciales le aparece el mensaje
                return redirect(url_for('ingresar')) # y lo redirecciona al inicio para que vuelva a ingresar
    return render_template('login.html', formulario=formulario) #lo redirecciona a loguearse 


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    formulario = RegistrarForm() 
    if formulario.validate_on_submit():
        if formulario.password.data == formulario.password_check.data:
            with open('usuarios', 'a+', newline='') as archivo:  #abre el archivo de usuario y lee y agrega una linea en el primer renglo vacio 
                archivo_csv = csv.writer(archivo) #abrir el csv en modo escribir 
                registro = [formulario.usuario.data, formulario.password.data] 
                archivo_csv.writerow(registro) #escribe una linea de resgistro
            flash('Usuario creado correctamente')  
            return redirect(url_for('ingresar')) #te redirecciona al inicio para ingresar
        else:
            flash('Las contraseñas no coinciden')
    return render_template('registrar.html', form=formulario)  #si no valida el submit te direcciona a la pagina de registrar




@app.route('/secret', methods=['GET']) #contraseña
def secreto():
    if 'username' in session:
        return render_template('private.html', username=session['username'])
    else:
        return render_template('sin_permiso.html') #valida contraseña y de estar mal te deuelve el mensaje sin permiso


@app.route('/logout', methods=['GET']) 
def logout():
    if 'username' in session:
        session.pop('username')  #borra el usuario en sesion para desloguearlo
        return render_template('logged_out.html')
    else:
        return redirect(url_for('index')) #te vuelve al ingreso





#CLIENTES#

@app.route('/clientes')
def clientes():
    if 'username' in session:   
        with open('clientes.csv','r',encoding='utf-8') as planillaClientes: #abre el archivo csv
            planilla_csv = csv.reader(planillaClientes) #lo lee
            encabezado_csv = next(planilla_csv)
            return render_template('clientes.html', encabezado_csv=encabezado_csv, planilla_csv=planilla_csv) #devuleve la info de clientes con el encabezado
    else:
        return render_template('sin_permiso.html') #si no logra acceder te devuleve la url sin permiso

#PRODUCTOS#

@app.route('/producto')
def producto():
    if 'username' in session:   
        with open('productos.csv','r',encoding='utf-8') as planillaProducto: #abre el archivo prodcutos csv
            planilla_csv = csv.reader(planillaProducto) 
            encabezado_csv = next(planilla_csv)
            return render_template('producto.html', encabezado_csv=encabezado_csv, planilla_csv=planilla_csv) #lo muestra
    else:
        return render_template('sin_permiso.html') #si no puede acceder te devuelve la url sin permiso




#Consulta clientes por pais#

@app.route('/ccxpais',methods=['GET', 'POST'])
def ConsultaClientexPais():
    if 'username' in session:
        formulario = ConsultaxPais()
        filtro = formulario.pais.data
        resultado = []
        if formulario.validate_on_submit():
            with open('clientes.csv', encoding='utf-8') as planillaClientes: #abre el csv clientes
                planilla_csv = csv.reader(planillaClientes) #la lee
                encabezado_csv = next(planilla_csv)
                cliente = next(planilla_csv, None)
                while cliente:          
                    if cliente[3].upper().startswith(filtro.upper()):  #filtra el cliente con la primera letra que ingreso el usuario y el upper transforma el vakor ingresado y el valor que toma del archivo en mayuscula 
                        resultado.append(cliente) #el valor lo guarda dentro del resultado 
                    cliente = next(planilla_csv, None) #se fija cual es la siguiente linea guarda el resultado y vuelve a hacer la busqueda (while)
                if resultado == []:  #si el resultado no es igual a todo lo anterior devuleve el flash
                    flash('No se encontraron resultados para su búsqueda')
                else:
                    return render_template('resccxpais.html', encabezado_csv=encabezado_csv, resultado=resultado) #si no nos direcciona a el template de clientes por pais
        return render_template('ccxpais.html', ccxpais=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html') #de otra forma si no lo encuentra te direcciona a la url sin permiso


#Consulta clientes por edad#

@app.route('/ccxedad',methods=['GET', 'POST'])
def ConsultaClientexEdad(): #Busca los clientes filtrando por la edad
    if 'username' in session:
        formulario = ConsultaxEdad()
        filtroMax = formulario.edad_max.data  #realiza un filtro de edad maxima 
        filtroMin = formulario.edad_min.data  #realiza un filtro por edad minima
        resultado = []
        if formulario.validate_on_submit():
            with open('clientes.csv', encoding='utf-8') as planillaClientes:  #abre el archivo de clientes csv
                planilla_csv = csv.reader(planillaClientes)
                encabezado_csv = next(planilla_csv)
                edad = next(planilla_csv, None)
                while edad:          
                    if (int(edad[1])>=int(filtroMin) and int(edad[1])<=int(filtroMax)): # Busca la edad dentro de la columna 1 del csv clientes
                        resultado.append(edad) #guarda el resultado 
                    edad = next(planilla_csv, None) #recorre la siguiente linea hasta llegar al final 
                if resultado == []:  #si el resultado es nulo devuleve el flash
                    flash('No existen resultados para su búsqueda')
                else:
                    return render_template('resccxedad.html', encabezado_csv=encabezado_csv, resultado=resultado) #si no devuleve el template de consulta por edad
        return render_template('ccxedad.html', ccxedad=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html') #si no encuentra resultados te direcciona a la url sin permiso

#Consulta clientes por fecha#

@app.route('/ccxfecha',methods=['GET', 'POST'])
def ConsultaClientexFecha(): #Filtra los clientes por fecha de alta
    if 'username' in session:
        formulario = ConsultaxFecha()
        filtro = formulario.fecha.data #trae la info del formulario
        resultado = []
        if formulario.validate_on_submit(): #valida el usuario
            with open('clientes.csv', encoding='utf-8') as planillaClientes: #abre clientes cvs
                planilla_csv = csv.reader(planillaClientes)
                encabezado_csv = next(planilla_csv)
                fecha = next(planilla_csv, None) #la lee hasta encontrar la bsuqueda
                while fecha:
                    if fecha[5].startswith(filtro): #realiza un filtro por fecha segun el primer caracter ingresado
                        resultado.append(fecha) #guarda el resultado
                    fecha = next(planilla_csv, None)
                if resultado == []: #si no encuntra lo que se busco devuleve el flash
                    flash('No existen resultados para su búsqueda')
                else:
                    return render_template('resccxfecha.html', encabezado_csv=encabezado_csv, resultado=resultado)
        return render_template('ccxfecha.html', ccxfecha=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')





#Agregar cliente#

@app.route('/agregarcliente',methods=['GET', 'POST'])
def AgrCliente(): #agrega un nuevo cliente a la BDD
    if 'username' in session:
        formulario = AgregarNuevoCliente()
        resultado = []
        if formulario.validate_on_submit(): #valida el usuario
            AgregarNuevo('cliente.csv',[formulario.nombre.data, formulario.edad.data, formulario.direccion.data, formulario.pais.data, formulario.dni.data, formulario.fecha_alta.data, formulario.mail.data, formulario.trabajo.data])
            flash('El cliente ha sido creado con exito')
            return redirect(url_for('clientes'))
        return render_template('agregarcliente.html', agregarcliente=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')




#Agregar producto#

@app.route('/agregarproducto',methods=['GET', 'POST'])
def AgrProducto():
    if 'username' in session:
        formulario = AgregarNuevoProducto()
        resultado = []
        if formulario.validate_on_submit():
            AgregarNuevo('productos.csv', [formulario.descripcion.data, formulario.codigo.data, formulario.precio.data, formulario.stock.data])
            flash('El producto ha sido agregado con exito')
            return redirect(url_for('producto'))
        return render_template('agregarproducto.html', agregarproducto=formulario, resultado=resultado)
    else:
        return render_template('sin_permiso.html')



#Modulo para agregar nuevo en productos y clientes

def AgregarNuevo(abrircsv, info):
    with open(abrircsv,'a+', encoding='utf-8') as archivo:
        archivo_csv = csv.writer(archivo)
        registro = info
        archivo_csv.writerow(registro)
    return archivo_csv



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)







