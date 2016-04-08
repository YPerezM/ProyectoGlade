__author__ = 'yago'

import sqlite3
from gi.repository import Gtk

class Animales:
    #Ficheros glade
    ficheroLogin="VentanaLogin.glade"
    fichero = "VentanaPrincipal.glade"
    fichero2 = "VentanaInserccion.glade"
    fichero3 = "VentanaBase.glade"
    fichero4 = "VentanaEliminacion.glade"
    #Builder para las interfaces
    builderLogin = Gtk.Builder()
    builder = Gtk.Builder()
    builder2 = Gtk.Builder()
    builder3 = Gtk.Builder()
    builder4 = Gtk.Builder()
    #Se agregan los archivos a los constructores de la interfaz
    builderLogin.add_from_file(ficheroLogin)
    builder.add_from_file(fichero)
    builder2.add_from_file(fichero2)
    builder3.add_from_file(fichero3)
    builder4.add_from_file(fichero4)
    #Contenedores de las ventanas
    VentanaLogin = builderLogin.get_object("VentanaLogin")
    VentanaPrincipal = builder.get_object("VentanaPrincipal")
    ventanaInserccion = builder2.get_object("VentanaInserccion")
    ventanaBase = builder3.get_object("VentanaBase")
    ventanaEliminacion = builder4.get_object("VentanaEliminacion")
    VentanaPrincipal.show_all()



    def IniciarBase(self):
        """Cursor para recorrer base de datos y conexion a ella"""
        self.con = sqlite3.connect("animales.dat")
        self.cursor = self.con.cursor()
        self.cursor.execute ("""CREATE TABLE IF NOT EXISTS campos(ANIMAL TEXT NOT NULL, RAZA TEXT NOT NULL, NOMBRE TEXT NOT NULL)""" )
        self.con.commit()


    def buscar(self, busqueda):
        """Recogemos el codigo de la caja de texto"""
        nombre = self.BoxBusqueda.get_text()
        #Buscamos el codigo recogido en la base de datos
        self.cursor.execute("Select * from campos where nombre='"+nombre+"'")
        #Recorremos el cursor y mostraremos si existe
        for animal in self.cursor:
            self.BoxBanimal.set_text(str(animal[0]))
            self.BoxBraza.set_text(str(animal[1]))
            self.BoxBnombre.set_text(str(animal[2]))


    def introducirAnimal(self, introducir):
        """Metodo de introduccion de nuevos animales a la base"""
        animal = self.BoxAnimal.get_text()
        raza = self.BoxRaza.get_text()
        nombre = self.BoxNombre.get_text()
        #self.limpiarIntroducir(self)
        #Introducimos valores en la tabla
        self.cursor.execute("insert into campos values('" + animal + "','" + raza + "','" + nombre + "')")
        #Importante efectuar commits en cada modificacion para asegurarnos la integridad de los datos en la misma
        self.con.commit()



    def Eliminar(self, eliminado):
        """Metodo eliminar de la base de datos"""
        #Recoje el codigo al igual que la funcion buscar; la diferencia es que esta ejecute un delete pasando como parametro el codigo
        CajaEliminar = self.CajaEliminar.get_text()
        self.cursor.execute("delete from campos where nombre ='" + CajaEliminar + "'")
        #Importante efectuar commits en cada modificacion para asegurarnos la integridad de los datos en la misma
        self.con.commit()
        #Borramos la caja de Eliminar ya usada
        self.CajaEliminar.set_text("")


    def on_Entrada_clicked(self, login):
        nombre = self.UsuarioLogin.get_text();
        contrasenha2 = self.ContrasenhaLogin.get_text();
        if nombre == "root" and contrasenha2 == "castelao":
            Animales()
            self.VentanaLogin.destroy()

        else:
            self.popup("Prueba otra vez")


    def popup(self, texto):
        window = Gtk.Window(title="Warning")
        label = Gtk.Label(texto)
        label.set_padding(15,15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()



    def click_volverConsulta(self, vuelta):
        """Metodos para volver a la VentanaPrincipal"""
        #self.limpiarIntroducir(self)
        self.ventanaBase.hide()
        self.VentanaPrincipal.show_all()



    def volverIntroducir(self, vuelta):
        #self.click_limpiarConsulta(self)
        self.ventanaInserccion.hide()
        self.VentanaPrincipal.show_all()


    def volverEliminar(self, vuelta):
        #self.CajaEliminar.set_text("")
        self.ventanaEliminacion.hide()
        self.VentanaPrincipal.show_all()



    def click_introducir(self, entrada):
        """Metodos para transaccion de interfaces"""
        self.VentanaPrincipal.hide()
        self.ventanaBase.show_all()


    def click_consultar(self, consulta):
        self.VentanaPrincipal.hide()
        self.ventanaInserccion.show_all()


    def Eliminar_articulo(self,eliminado):
        self.VentanaPrincipal.hide()
        self.ventanaEliminacion.show_all()




    def __init__(self):
        """Entrada de ventana principal al arrancar la aplicacion y declaracion de los signals"""
        #Mostramos la ventana principal
        self.VentanaPrincipal.show_all();

        #Cajas de las ventanas
        self.BoxBusqueda=self.builder3.get_object("BoxBusqueda")
        self.BoxBanimal = self.builder3.get_object("BoxBanimal")
        self.BoxBraza = self.builder3.get_object("BoxBraza")
        self.BoxBnombre = self.builder3.get_object("BoxBnombre")
        self.BoxAnimal = self.builder2.get_object("BoxAnimal")
        self.BoxRaza = self.builder2.get_object("BoxRaza")
        self.BoxNombre = self.builder2.get_object("BoxNombre")
        self.CajaEliminar = self.builder4.get_object("CajaEliminar")
        self.UsuarioLogin=self.builderLogin.get_object("UsuarioLogin")
        self.ContrasenhaLogin=self.builderLogin.get_object("ContrasenhaLogin")


        #Manejadores; funciones definidas en Glade con su equivalencia en Python
        signals = {"BackConsulta":self.click_volverConsulta,
                  "onClick_Insertar":self.introducirAnimal,
                  "onClick_VEliminar":self.Eliminar_articulo,
                  "onClick_VAcceso": self.click_introducir,
                  "BackInserccion":self.volverIntroducir,
                  "onClick_VInserccion": self.click_consultar,
                  "BackEliminar":self.volverEliminar,
                  "click_buscar":self.buscar,
                  "Cerrar1":self.Terminar,
                  "Cerrar2":self.Terminar,
                  "Cerrar3":self.Terminar,
                  "Cerrar":self.Terminar,
                  "Eliminar":self.Eliminar,
                   "on_Entrada_clicked":self.on_Entrada_clicked}
        #Conectamos constructores a los manejadores
        self.builder.connect_signals(signals)
        self.builder2.connect_signals(signals)
        self.builder3.connect_signals(signals)
        self.builder4.connect_signals(signals)



        #Llamada del metodo IniciarBase, que lleva a cabo la conexion con la base y la creacion de la tabla campos
        self.IniciarBase()



    def Terminar(self,dos,tres):
        """Metodo para cerrar programa"""
        #Cerramos todas las ventanas y el main
        self.VentanaPrincipal.connect("delete-event", Gtk.main_quit)
        self.ventanaInserccion.connect("delete-event", Gtk.main_quit)
        self.ventanaBase.connect("delete-event", Gtk.main_quit)
        self.ventanaEliminacion.connect("delete-event", Gtk.main_quit)

        Gtk.main_quit()


Animales()
Gtk.main()

