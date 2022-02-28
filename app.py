#Importaciones
import json
import random
from sqlalchemy import Integer, String
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms import validators
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import Flask
from flask import redirect
from flask import url_for
from flask import render_template
from flask import request
from flask import session

datos=json.load(open('.data.json'))

#Datos para la conexion con SQL Server
s = datos.get('server','')
b = datos.get('database','')
u = datos.get('user','')
c = datos.get('password','')
d = datos.get('driver','')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mssql+pyodbc://{0}:{1}@{2}/{3}?driver={4}'.format(u,c,s,b,d)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=datos.get('correo','')
app.config['MAIL_PASSWORD']=datos.get('cc','')

db = SQLAlchemy(app)
mail = Mail()

class Producto (db.Model):
    __tablename__ = 'INVENTARIO_WEB'
    codigo=db.Column(String(50),primary_key=True)
    descripcion=db.Column(String(150))
    stock=db.Column(Integer())
    reserva=db.Column(Integer())
    clase=db.Column(String(50))
    subclase=db.Column(String(50))
    laboratorio=db.Column(String(50))
    precio=db.Column(Integer())
    costo=db.Column(Integer())
    lote=db.Column(String(50))
    bodega=db.Column(String(50))
    ubicacion=db.Column(String(50))

class Usuario(db.Model):
    __tablename__ = 'USERS_WEB'
    correo=db.Column(String(50),primary_key=True)
    nombre=db.Column(String(50))
    apellido=db.Column(String(50))
    usuario=db.Column(String(50))
    contraseña=db.Column(String(110))
    
class Formulario_login(FlaskForm):
    usuario = StringField("Usuario",[validators.data_required(message='Dato requerido')])
    contraseña = PasswordField("Contraseña",validators=[DataRequired()])
    
class Formulario2(FlaskForm):
    nombre = StringField("Nombre",[validators.data_required(), validators.length(min=3,max=25)])
    apellido = StringField("Apellido",[validators.data_required(), validators.length(min=3,max=25)])
    usuario = StringField("Usuario",[validators.data_required()])
    correo = EmailField("Correo",[validators.data_required()])

db.init_app(app)
mail.init_app(app)
app.secret_key=datos.get("clave","")

@app.route('/', methods=['GET','POST'])
def Login():
    formulario = Formulario_login()
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('Login'))
    else:
        if request.method == 'POST' and formulario.validate_on_submit():
            usuario= formulario.usuario.data
            contraseña = formulario.contraseña.data
            query = Usuario.query.filter(Usuario.usuario == usuario)
            for resultado in query :
                if check_password_hash(resultado.contraseña,contraseña):
                    session['username'] = usuario
                    return redirect(url_for('Buscador'))
                else:
                    return redirect(url_for('Login'))
        else:
            return render_template('login.html',form=formulario)

@app.route('/registro',methods=['GET','POST'])
def Registro():
    formulario = Formulario2()
    if request.method == 'POST' and formulario.validate:
        nombre = formulario.nombre.data
        apellido = formulario.apellido.data
        usuario = formulario.usuario.data
        correo = formulario.correo.data
        aleatorio = str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
        contraseña = generate_password_hash(aleatorio,'pbkdf2:sha256')
        usuario_nuevo = Usuario( nombre=nombre, apellido=apellido, usuario=usuario, correo=correo, contraseña=contraseña)
        msg = Message("Se ha registrado con exito",sender=app.config['MAIL_USERNAME'],recipients=[correo])
        msg.html = render_template('email.html', clave=aleatorio)
        mail.send(msg)
        db.session.add(usuario_nuevo)
        db.session.commit()
        return redirect(url_for('Login'))
    else:
        return render_template('registro.html',form=formulario)

#PAGINA 3: BUSCADOR / REALIZA LA CONSULTA A LA BASE DE DATOS Y RENDERIZA LA TABLA
@app.route('/busqueda')
@app.route('/busqueda/<int:pagina>')
def Buscador(pagina=1):
    if 'username' in session:
        per_page = 25
        productos2 = Producto.query.add_columns(Producto.codigo,Producto.descripcion,Producto.bodega,Producto.stock,Producto.reserva,Producto.lote).order_by(Producto.descripcion).paginate(pagina,per_page,False)
        return render_template('buscador.html',productos=productos2,normal=True,page=productos2.page,pages=productos2.pages,prev=productos2.has_prev,next=productos2.has_next)
    else:
        return redirect(url_for("Login"))

#PAGINA 3: BUSCADOR / TOMA LA ENTRADA DEL USUARIO PARA BUSCAR Y MOSTRAR COINCIDENCIAS
@app.route('/busqueda/buscar', methods=['POST'])
@app.route('/busqueda/buscar/<int:pagina>', methods=['GET','POST'])
@app.route('/busqueda/buscar/<string:anterior>/<int:pagina>', methods=['GET','POST'])
def Buscar(pagina=1,anterior=''):
    if request.method == 'POST':
        entrada = request.form['entrada']
        productos2 = Producto.query.add_columns(Producto.codigo,Producto.descripcion,Producto.bodega,Producto.stock,Producto.reserva,Producto.lote).filter(Producto.descripcion.like(''+entrada+'%')).order_by(Producto.descripcion).paginate(pagina,25,False)
        return render_template('buscador.html',productos=productos2,pagina=pagina,normal=False,entrada=entrada,page=productos2.page,pages=productos2.pages,prev=productos2.has_prev,next=productos2.has_next)
    if request.method == 'GET':
        productos2 = Producto.query.add_columns(Producto.codigo,Producto.descripcion,Producto.bodega,Producto.stock,Producto.reserva,Producto.lote).filter(Producto.descripcion.like(''+anterior+'%')).order_by(Producto.descripcion).paginate(pagina,25,False)
        return render_template('buscador.html',productos=productos2,pagina=pagina,normal=False,entrada=anterior,page=productos2.page,pages=productos2.pages,prev=productos2.has_prev,next=productos2.has_next)

#PAGINA 4: DETALLE / MUESTRA EL RESTO DE DATOS DEL PRODUCTO SELECCIONADO EN EL BUSCADOR
#DEBO CAMBIAR LA PRIMARY KEY POR EL LOTE, EN CASO DE NO TENER LOTE BUSCAR POR CODIGO
@app.route('/detalle/<string:codigo>')
@app.route('/detalle/<string:codigo>/<string:lote>')
def Mostrar_detalle(codigo,lote=""):
    if 'username' in session:
        if lote != 'SL' and lote != "":
            producto2 = Producto.query.filter(Producto.lote==lote).first()
            return render_template('detalle.html',producto=producto2)
        else:
            producto2 = Producto.query.filter(Producto.codigo==codigo).first()
            return render_template('detalle.html',producto=producto2)
    else:
        return redirect(url_for('Login'))

if __name__ == '__main__':
    app.run(debug=True,port=5000)