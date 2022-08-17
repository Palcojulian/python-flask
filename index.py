from flask import Flask, request, url_for, redirect, abort, render_template
import mysql.connector

app = Flask(__name__)

conex = mysql.connector.connect(
    host = 'localhost',
    user = 'julian',
    password = 'julian',
    database = 'prueba'
)

cursor = conex.cursor(dictionary=True)


@app.route('/read', methods=['GET', 'POST'])
def read():
    cursor.execute('select * from usuario')
    usuarios = cursor.fetchall()
    return render_template('read.html', usuarios = usuarios)
    

@app.route('/create', methods=['GET', 'POST'])
def create():
    if  request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        edad = request.form['edad']
        sql = 'insert into usuario (email, username, edad) values (%s, %s, %s)'
        values = (email, username, edad)
        cursor.execute(sql, values)
        conex.commit()

        return redirect(url_for('read'))

    return render_template('create.html')




@app.route('/')
def index():
    return 'Pagina Principal'

@app.route('/pagina2/<int:id_pagina>')
def pagina2(id_pagina):
    return 'Pagina 2 que recibe un id: ' + str(id_pagina)

#GET, POST, PUT, PATCH, DELETE
@app.route('/pagina3', methods=['GET', 'POST'])
def pagina3():
    if request.method == 'GET':
        return 'Pagina 3 Metodo GET '
    else:
        return 'pagina 3 Metodo diferente a GET '


#--------------------------------------------------------------------------------
#Manera de enviar informacion de un formulario mediante "curl"
#$ curl -d "nombre=esteban&apellido=guegue" -X POST http://localhost:5000/pagina4 
# request.form-> Manera de enviar datos en un formulario, el ejemplo se hace con curl
# url_for -> Manera de crear una url, si desemos redireccionarnos a otra pagina

@app.route('/pagina4', methods=['POST'])
def pagina4():
    print(url_for('pagina2',id_pagina=5))  #Se llama la función, y si el esta tiene parametros se la añadimos despues de una coma
    print(request.form)                       
    print(request.form['nombre'])
    print(request.form['apellido'])
    return 'Pagina 4'
#--------------------------------------------------------------------------------

# url_for -> Indicamos la direccion de la pagina
# redirect -> Hace que la pagina se redirigida de acuerdo a la url que indicamos

@app.route('/pagina5', methods=['POST', 'GET'])
def pagina5():
    return redirect(url_for('pagina2', id_pagina=6))
    
#-------------------------------------------------------
# render_template -> forma de abrir un archivo html
@app.route('/pagina6')
def pagina6():
    #abort(401) #Manera de mostrar errores con "abort"
    return render_template('index.html')


#Manera de traer o mostrar objetos json
@app.route('/pagina7')
def pagina7():
    return {
        'username':'palcojulian',
        'email':'palco@gmail.com',
        'edad': 21,
        'direccion':'mondomo'
    }

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', mensaje='Hola mundo')