import tkinter as tk
from tkinter import *
from tkinter import messagebox as ms
from tkinter.ttk import *
import mysql.connector
import smtplib
import time
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from io import open
from win10toast import ToastNotifier

#La clase login es la que se encargara de crear el login
class login:
    def __init__(self):
        #Configuracion de la ventana raiz del Login
        self.db = "Database.db"
        self.login = tk.Tk()
        #self.login.overrideredirect(1)
        self.login.attributes('-alpha', 0.9)
        self.login.geometry("400x370+550+200")
        self.login.config(bg="#292929")
        self.login.iconbitmap("hIcon.ico")
        self.login.title("Acceder")
        self.login.resizable(0,0)
        image = tk.PhotoImage(file="Rectángulo redondeado 1.png")
        #Creando los estilos para los frames
        lstyle = Style()
        fstyle = Style()
        bstyle = Style()
        fstyle.configure('fstyle.TFrame', background="#292929")
        lstyle.configure('lstyle.TLabelframe', background="#292929", bd="red")
        lstyle.configure('lstyle.TLabelframe.Label', Foreground="#292929", background="#292929", font=("cambria", 15))
        bstyle.configure('fstyle.TButton', background="#292929")
        #Creando los estilos para los botones
        boton = Style()
        check = Style()
        check.configure('check.TCheckbutton', background="#292929", foreground="white")
        #Inicializando las variables con las que trabajara el login
        self.show = tk.IntVar()
        self.mostrar = False
        #logic
        try:
            doc = open("AutoFile.txt", "r")
            self.texto = doc.readline()
            doc.close()
            self.document = True
        except FileNotFoundError:
            self.document = False

        self.frames = Frame(self.login, style='fstyle.TFrame', width=350, height=310)
        self.frames.place(x=25, y=20)

        #Peticiones de entrada al usuario + Labels
        self.info = Label(text="Ingrese sus credenciales.", foreground="#ffffff", background="#292929", font=("cambria", 14))
        self.info.place(x=50, y=60)
        self.user = tk.Entry(self.login, width=25, font=("cambria",14), bg="#292929", fg="white")
        self.user.focus()
        self.user.config(insertbackground="white")
        self.user.place(x=50, y=125)
        self.password = tk.Entry(self.login, width=25, show="•", font=("cambria",14), bg="#292929", fg="white")
        self.password.config(insertbackground="white")
        self.password.place(x=50, y=175)
        self.user['foreground']="#cccccc"
        self.user.insert(0, "Nombre de usuario")
        self.password['foreground']="#cccccc"
        self.password.insert(0, "password")
        #Botones y su configuracion
        self.button = tk.Button(text="Entrar", image=image, command=lambda:self.callback("1"), bd=0, highlightthickness=0)
        self.button.place(x=125, y=280)
        passview = Checkbutton(text="Mostrar contraseña", variable=self.show, onvalue=1, offvalue=0, command=self.see, style='check.TCheckbutton').place(x=50, y=230)
        #Bindeo de teclas y mouse a funciones.
        self.login.bind("<Return>", self.callback)
        self.user.bind("<FocusIn>", self.UserfocusIn)
        self.user.bind("<FocusOut>", self.UserfocusOut)
        self.password.bind("<FocusIn>", self.PassfocusIn)
        self.password.bind("<FocusOut>", self.PassfocusOut)
        self.login.mainloop()

#Las funciones focus son las que se encargan de mostrar el grayed text en los textbox cuando el usuario no tiene el Focus
#sobre el textBox en especifico, aca hay un focusIN y un focusOut por cada textBox. Uno para el usuario, otro para la pass

    def UserfocusIn(self, event):
        if self.user.get() == "Nombre de usuario" or self.user.get() =="" :
            self.user.delete(0, "end")
            self.user['foreground']="white"
        else:
            pass

    def UserfocusOut(self, event):
        if self.user.get() == "Nombre de usuario" or self.user.get() =="":
            self.user.delete(0, "end")
            self.user['foreground']="#cccccc"
            self.user.insert(0, "Nombre de usuario")
        else:
            pass

    def PassfocusIn(self, event):
        if self.password.get() == "password":
            self.password.delete(0, "end")
            self.password['foreground']="white"

    def PassfocusOut(self, event):
        if self.password.get() == "password" or self.password.get() =="":
            self.password.delete(0, "end")
            self.password['foreground']="#cccccc"
            self.password.insert(0, "password")
        else:
            pass

    #La funcion see es la que se encarga de gestionar si la contraseña se mostrara masked o no
    def see(self):
        if self.mostrar == False:
            self.password['show']=""
            self.mostrar = True
        elif self.mostrar == True:
            self.password['show']="•"
            self.mostrar = False
    #La funcion checkQuery es lo que se encargara de dinamizar las consultas al servidor
    def checkQuery(self, query, parameters=()):
            self.dbb = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere')
            cursor = self.dbb.cursor()
            cursor.execute(query, parameters)
            resultados = cursor.fetchall()
            self.dbb.commit()
            return resultados

    def checkQueryC(self, query, parameters=()):
            self.dbb = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere')
            cursor = self.dbb.cursor()
            cursor.execute(query, parameters)
            self.dbb.commit()
    #La funcion retrieve es la columna vertebral del login, esta funcion se encarga de guardar todos los datos
    #del usuario en una tupla, ademas de realizar la confirmacion de si los datos ingresados por el Usuario
    #son los correctos.
    def retrieve(self):

        global datos
        query = "SELECT * FROM tbperfilusuarios where usuario = %s and password=%s"
        parameters = (self.user.get(), self.password.get())
        rows = self.checkQuery(query, parameters)
        for row in rows:
            if row[1] == parameters[0] and row[3] == parameters[1]:
                datos = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],row[11], row[12], row[13], row[14], row[15], row[16], row[17]]
                self.niveles()
                if self.document == False:
                    answer = ms.askquestion("Informacion", "¿Desea que muestren sus trabajos nuevos mientras no se ejecuta en primer plano?")
                    if answer == 'yes':
                        self.secondPlane()
                    else:
                        docu = open("AutoFile.txt", "w")
                        docu.write("false")
                        docu.close()
                else:
                    pass
                try:
                    if self.texto == 'true':
                        self.secondPlane()
                    else:
                        pass
                except AttributeError:
                    pass
                return True
            else:
                return False

#La funcion callback es la que se encarga de verificar lo que la funcion retrieve devuelve, si los datos que
#que retrieve devuelve resultan ser correctos, esta instanciara la clase window
    def callback(self, event):
        if self.retrieve() == True:
            self.info['foreground'] = "green"
            self.info['text'] = "Ha accedido correctamente"
            self.login.destroy()
            root = tk.Tk()
            ventana = window(root)
            root.mainloop()
        else:
            self.info['foreground'] = "red"
            self.info['text'] = "Ingrese los datos debidamente"

    def niveles(self):
        global datos
        level = datos[16]
        a=0
        while True:
            for i in range(100):
                #print(datos[17])
                if datos[17]<=0:
                    a = a + datos[17] + 3500
                    necesario = a/10
                    if level == i:
                        NextLevel = level + 1
                        query = "UPDATE tbperfilusuarios SET nivel = %s WHERE usuario = %s"
                        parameters = (NextLevel, datos[1])
                        neededQuery = "UPDATE tbperfilusuarios SET puntuacionRestante = %s WHERE usuario = %s"
                        needed = (necesario, datos[1])
                        nivel = NextLevel
                        #print(parameters)
                        self.checkQueryC(neededQuery, needed)
                        self.checkQueryC(query, parameters)
                        datos.append(NextLevel)
                        datos.append(necesario)
                else:
                    NextLevel = datos[16]
                    necesario = datos[17]
                    datos.append(NextLevel)
                    datos.append(necesario)

            if i==99:
                    break

    def secondPlane(self):
        archivo = open("AutoFile.txt", "w")
        archivo.write("true")
        archivo.close()
        plano = SegundoPlano()

#La clase perfil sera la que mostrara todo lo referente a la identidad del usuario en sesion.
class perfil:
    #el constructor de la clase perfil recibira 3 parametros: El self, haciendo referencia a la propia clase.
    #el foto, que lo que se encarga es de recibir un atributo de la clase window(la clase principal)
    #el atributo que recibe no es mas que el metodo PhotoImage de clase Tk que tiene la ventana principal
    #el parametro raiz, recibira el tk de la clase window (Esto fue una jugada rotisima de mi parte, no se ni explicarla)
    def __init__(self, foto, raiz):
        #Aca se esta configurando los datos de la ventana de perfil, aca no estoy creando una ventana raiz
        #al contrario que en Window y login, directamente estoy creando una ventana, una ventana afiliada
        #a la main de Tk(la clase que genera las ventanas principales), uso un Toplevel y no una instancia de tk
        #porque solo puede haber una Tk en todo el programa, una Tk se cierra y se abre otra.
        self.main = Toplevel()
        self.main.config(bg="#323232")
        self.main.geometry("1170x600+150-130")
        self.main.iconbitmap("hIcon.ico")
        self.main.title("H-work: Mi perfil")
        self.raiz = raiz
        #Aca estoy pasando a un atributo self, es decir a un atributo perteneciente a ESTA clase, y en este caso
        #estoy pasando el metodo PhotoImage que mencione arriba con la propia imagen ya dentro, estoy asignando
        #Ese metodo con su imagen a un atributo PROPIO de ESTA clase.
        self.imagen = foto
        #Creando los estilos de los frames
        self.frame1Style = Style()
        self.frame1Style.configure('frame1.TFrame', background="white")
        self.frame2Style = Style()
        self.frame2Style.configure('frame2.TFrame', background="#323232")


        #Creamdo la logica de gestion de datos que usara la clase perfil
        if datos[6]=="Development":
            self.leader = "Gabriel Martinez"
        elif datos[6]=="Management":
            self.leader = "Ezequiel Guzman"
        elif datos[6] == "Marketing Digital":
            self.leader = "Warlin Suriel"
        else:
            self.leader = 0

        if datos[1]=="Gabrielmartinez" and datos[6]=="Development":
            self.posicion = "Lider"
        elif datos[1]=="Ezequielgm677" and datos[6]=="Management":
            self.posicion = "Lider"
        elif datos[1]=="que va lidera warlin" and datos[6] == "Marketing Digital":
            self.posicion = "Lider"
        else:
            self.posicion = "Miembro"

        #Creacion de los Frames que usara la ventana
        self.frame1 = Frame(self.main, width=300, height=200, style='frame1.TFrame')
        self.frame1.place(x=5, y=5)
        self.frame2 = Frame(self.frame1, width=296, height=165, style='frame2.TFrame')
        self.frame2.place(x=2, y=2)
        self.frame3 = Frame(self.main, width=300, height=165, style='frame1.TFrame')
        self.frame3.place(x=5, y=210)
        self.frame4 = Frame(self.main, width=300, height=215, style='frame1.TFrame')
        self.frame4.place(x=5, y=380)
        self.framePrincipal = Frame(self.main, width=855, height=590, style='frame1.TFrame')
        self.framePrincipal.place(x=310, y=5)
        self.imageFrame = Frame(self.frame2, width=296, height=200, style='frame2.TFrame')
        self.imageFrame.place(x=50, y=5)
        #Creacion de todos los widgeds que estaran en el Frame principal
        Label(self.framePrincipal, text="En esta ventana se mostrara el progreso en forma de niveles y la puntuacion en forma de barra de progreso para\nasi representar todo el progreso individual.", background="white", font=("cambria", 12)).place(x=30, y=10)
        #Aca instancio la clase Treeview y le paso todos los parametros que necesita.

        self.table = Treeview(self.framePrincipal, height=17, column=("#1", "#2", "#3", "#4"))
        self.table.place(x=30, y=185)
        self.table.heading("#0", text="Objetivo", anchor="center")
        self.table.column("#0", width=300)
        self.table.heading("#1", text="Fecha de entrega", anchor="center")
        self.table.column("#1", width=120)
        self.table.heading("#2", text="Fecha de asignacion", anchor="center")
        self.table.column("#2", width=120)
        self.table.heading("#3", text="Asignado a", anchor="center")
        self.table.column("#3", width=130)
        self.table.heading("#4", text="Puntuacion", anchor="center")
        self.table.column("#4", width=120)
        Label(self.framePrincipal, text="Nivel actual: ", background="white", font=("cambria", 14)).place(x=30, y=80)
        self.nivelActual = Label(self.framePrincipal, text=datos[18], background="white", font=("cambria", 14))
        self.nivelActual.place(x=130, y=80)
        Label(self.framePrincipal, text="Progreso hasta el nivel maximo ", background="white", font=("cambria", 10)).place(x=30, y=130)
        Label(self.framePrincipal, text="Puntuacion total: ", background="white", font=("cambria", 14)).place(x=450, y=80)
        self.acumulacion = Label(self.framePrincipal, text=datos[15], background="white", font=("cambria", 14))
        self.acumulacion.place(x=590, y=80)
        Label(self.framePrincipal, text="Puntuacion restante para hasta el siguiente nivel: ", background="white", font=("cambria", 10)).place(x=450, y=130)
        self.ptsTotal = Label(self.framePrincipal, text=datos[19], background="white", font=("cambria", 10))
        self.ptsTotal.place(x=735, y=130)
        self.volver = Label(self.framePrincipal, text="Volver a la ventana principal", background="white", foreground="#016caf", font=("cambria", 11))
        self.volver.place(x=630, y=565)

        #Creacion de los widgeds que pertenecesaran al frame 3
        tk.Label(self.imageFrame, image=self.imagen, border=0).pack()
        Label(self.frame3, text="Datos en No.where",font=("cambria",13), background="white", foreground="#016caf").place(x=5, y=0)
        Label(self.frame3, text="Usuario:", background="white", font=("cambria",13)).place(x=5, y=30)
        Label(self.frame3, text=datos[1], background="white",font=("cambria",11)).place(x=69, y=32)
        Label(self.frame3, text="posición:", background="white",font=("cambria",13)).place(x=5, y=65)
        Label(self.frame3, text=datos[4], background="white",font=("cambria",11)).place(x=73, y=67)
        Label(self.frame3, text="Fecha de ingreso:", background="white",font=("cambria",13)).place(x=5, y=102)
        Label(self.frame3, text=datos[11], background="white",font=("cambria",11)).place(x=133, y=104)
        Label(self.frame3, text="ID:", background="white",font=("cambria",13)).place(x=5, y=137)
        Label(self.frame3, text=datos[0], background="white",font=("cambria",11)).place(x=30, y=139)
        #Creacion de los widgeds que pertenecesaran al frame 4
        Label(self.frame4, text="Datos de mi equipo", background="white",font=("cambria",13), foreground="#016caf").place(x=5, y=0)
        Label(self.frame4, text="Mi equipo:", background="white", font=("cambria",13)).place(x=5, y=30)
        Label(self.frame4, text=datos[6], background="white", font=("cambria",11)).place(x=85, y=32)
        Label(self.frame4, text="Líder de equipo:", background="white", font=("cambria",13)).place(x=5, y=65)
        Label(self.frame4, text=self.leader, background="white", font=("cambria",11)).place(x=125, y=67)
        Label(self.frame4, text="Cargo:", background="white", font=("cambria",13)).place(x=5, y=102)
        Label(self.frame4, text=datos[12], background="white", font=("cambria",11)).place(x=57, y=104)
        Label(self.frame4, text="Posición en el equipo:", background="white", font=("cambria",13)).place(x=5, y=137)
        Label(self.frame4, text=self.posicion, background="white", font=("cambria",11)).place(x=165, y=139)
        self.TeamWork = Label(self.frame4, text="Ver trabajos pendientes", background="white", font=("cambria",13), foreground = "#016caf")
        self.TeamWork.place(x=50, y=180)
        #creacion de btones
        self.cambiarLabel = Button(self.frame1, text = "Proximamente", command=lambda:self.changeImage(), width=30)
        self.cambiarLabel.place(x=55, y=170)
        #configuracion de la barra de Progreso Progressbar
        self.progreso = Progressbar(self.framePrincipal, maximum=385000)
        self.progreso.place(x=30, y=155, width=795)
        self.progreso.step(datos[15])
        #Bindeo de teclas y mouse a metodos de la clase
        self.TeamWork.bind("<Button-1>", self.getQueryTeam)
        self.volver.bind("<Button-1>", self.back)
        self.getQuery("34")

#El metodo checkQuert hace lo mismo que hacia en la clase login
    def checkQuery(self, query, parameters=()):
        self.db = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
        self.cursor = self.db.cursor()
        self.cursor.execute(query, parameters)
        self.resultado = self.cursor.fetchall()
        self.db.commit()
        return self.resultado

    def checkQueryC(self, query, parameters=()):
        self.db = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
        self.cursor = self.db.cursor()
        self.cursor.execute(query, parameters)
        self.db.commit()
#Si el metodo checkQuery es la columna del programa, el getQuery y sus variantes es el corazon, el metodo getQuery
#se encarga de crear un tipo de consulta y pasarsela al checkQuery para que la ejecute, luego que ese proceso esta hecho
#pasa los resultados de la consulta a la tabla.
    def getQuery(self, event):
        #rebuilding data
        self.TeamWork.bind("<Button-1>", self.getQueryTeam)
        self.TeamWork['text']="Ver trabajos pendientes"
        #table stuff
        save = self.table.get_children()
        for item in save:
            self.table.delete(item)
        #Query stuff
        self.receptor = datos[1]
        query = "SELECT * FROM tbobjetivos where estatus = %s and nombreUser =%s"
        parameters = ("En proceso", self.receptor)
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.table.insert('', 0, text=row[4], values=(row[6], row[8], row[1], row[10]))

#Variante del getQuery para tomar el equipo
    def getQueryTeam(self, event):
        #rebuilding data
        self.TeamWork.bind("<Button-1>", self.getQuery)
        self.TeamWork['text']="Mis trabajos pendientes"
        #table stuff
        save = self.table.get_children()
        for item in save:
            self.table.delete(item)
        #Query stuff
        query = "SELECT * FROM tbobjetivos WHERE equipo = %s and estatus = %s"
        parameters = (datos[6], "En proceso")
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.table.insert('', 0, text=row[4], values=(row[6], row[8], row[1], row[10]))
#Metodo que se encarga de destruir la ventana perfil y llamar a la ventana principal
    def back(self, event):
        self.main.destroy()
        self.raiz.deiconify()

#La clase window es la clase principal del programa, es todos los organos del programa
class window:
#El constructor de esta clase recibe dos parametros, el self y el root, el metodo root recibira una instancia de tk
    def __init__(self, root):
        #-Configuracion de la ventana raiz o sea del Tk
        self.raiz = root
        self.raiz.geometry("1170x600+150-130")
        self.raiz.resizable(0,0)
        self.raiz.title("H-work")
        self.raiz.iconbitmap("hIcon.ico")
        self.raiz.config(bg="#292929")
        self.plegue = self.raiz.deiconify()
        #Variables que se usaran a lo largo de toda la clase
        self.nombre = tk.StringVar()
        self.equipo = tk.StringVar()
        self.entry = tk.StringVar()
        self.titulo = tk.StringVar()
        self.buscar = tk.StringVar()
        self.val = tk.StringVar()
        self.radio = tk.IntVar()
        self.rows = 0
        self.editmode = False
        #Metodos de imagen que uso para llamarlas a lo largo del programa
        self.AdmImg = tk.PhotoImage(file="Admin.png")
        self.UserImg = tk.PhotoImage(file="Usuario.png")
        self.buscar = tk.PhotoImage(file="lupa.png")
        #este fue el que use para el perfil
        self.perfilImage = tk.PhotoImage(file="Elipse 2.png")
        #configuracion de los estilos de todos los widgeds de la clasehvgu
        Mframe = Style()
        frame = Style()
        LabFrame = Style()
        lframe = Style()
        button = Style()
        button2 = Style()
        lstyle = Style()
        radio = Style()
        Mframe.configure('Mframe.TFrame', background="#ffffff")
        lframe.configure('lframe.TFrame', background="#343a43")
        frame.configure('TFrame', background = "#abb2bf")
        lstyle.configure('lstyle.TLabelframe', background="#ffffff")
        lstyle.configure('lstyle.TLabelframe.Label', Foreground="#292929", background="#ffffff", font=("cambria", 10))
        LabFrame.configure('LabFrame.TFrame', background = "#292929")
        button.configure('bt.TButton',font=("time new roman", 12), background="white")
        button2.configure('bt2.TButton',font=("time new roman", 11), background="white")
        radio.configure('radio.TRadiobutton', background="#ffffff" )
        #-------Frames
        self.MainFrame = Frame(self.raiz, width = 860, height=570, style = 'Mframe.TFrame').place(x=290, y=15)
        self.MainFrame2 = Frame(self.raiz, width = 265, height=545, style = 'Mframe.TFrame').place(x=15, y=15)
        self.userFrame = Frame(self.raiz, width=300, height=110, style = 'LabFrame.TFrame').place(x=820, y=30)
        self.userData = Labelframe(self.raiz,text="Informacion de usuario", width=255, height=235, style = 'lstyle.TLabelframe')
        self.userData.place(x=20, y=320)
        self.infoData = Labelframe(self.MainFrame2 ,text= "Filtros", width=500, height=55, style = 'lstyle.TLabelframe')
        self.infoData.place(x=315, y=70)
        self.frame = Frame(width=813,height=367, style='Mframe.TFrame')
        self.frame.place(x=315, y=200)
        #Label(self.infoData, text="Para hacer una consulta desde el cuadro de busqueda solo debes ingresar el nombre del objetivo", foreground = "#292929", font=("cambria", 11), background="#ffffff").place(x=5, y=1)
        #-----Labels
        Label(self.userFrame, text="Datos", background="#292929", foreground = "#ffffff", font=("cambria", 13)).place(x=825, y=32)
        Label(self.userFrame, text="Usuario en sesion: ", background="#292929", foreground = "#ffffff", font=("cambria", 11)).place(x=825, y=60)
        Label(self.userFrame, text=datos[1], background="#292929", foreground = "#ffffff", font=("cambria", 11)).place(x=940, y=61)
        Label(self.userFrame, text="Equipo: ", background="#292929", foreground = "#ffffff", font=("cambria", 11)).place(x=825, y=87)
        Label(self.userFrame, text=datos[6], background="#292929", foreground = "#ffffff", font=("cambria", 11)).place(x=878, y=87)
        Label(self.userFrame, text="Cargo: ", background="#292929", foreground = "#ffffff", font=("cambria", 11)).place(x=825, y=113)
        Label(self.userFrame, text=datos[12], background="#292929", foreground = "#ffffff", font=("cambria", 11)).place(x=867, y=114)
        Label(self.userData, text="Nombre: ", background="#ffffff", foreground = "#292929", font=("cambria", 11)).place(x=5, y=10)
        Label(self.userData, text=(datos[2]+" "+datos[5]), background="#ffffff", foreground = "#292929", font=("cambria", 10)).place(x=61, y=12)
        Label(self.userData, text="Correo: ", background="#ffffff", foreground = "#292929", font=("cambria", 11)).place(x=5, y=40)
        Label(self.userData, text=(datos[7]), background="#ffffff", foreground = "#292929", font=("cambria", 10)).place(x=56, y=42)
        Label(self.userData, text="ID:", background="#ffffff", foreground = "#292929", font=("cambria", 12)).place(x=5, y=70)
        Label(self.userData, text=(datos[0]), background="#ffffff", foreground = "#292929", font=("cambria", 12)).place(x=26, y=70)
        Label(self.userData, text="Perfil:", background="#ffffff", foreground = "#292929", font=("cambria", 11)).place(x=5, y=100)
        Label(self.userData, text=(datos[4]), background="#ffffff", foreground = "#292929", font=("cambria", 10)).place(x=46, y=102)
        Label(self.userData, text="Nacionalidad:", background="#ffffff", foreground = "#292929", font=("cambria", 11)).place(x=5, y=130)
        Label(self.userData, text=(datos[8]), background="#ffffff", foreground = "#292929", font=("cambria", 10)).place(x=92, y=132)
        Label(self.userData, text="Telefono:", background="#ffffff", foreground = "#292929", font=("cambria", 11)).place(x=5, y=160)
        Label(self.userData, text=(datos[13]), background="#ffffff", foreground = "#292929", font=("cambria", 10)).place(x=67, y=162)
        PerfilLabel = Label(self.userData, text=("Ver mi perfil."), background="#ffffff", foreground = "#016caf", font=("cambria", 12))
        PerfilLabel.place(x=60, y=190)

        #Entry
        self.want = Label(self.MainFrame2, text="Buscar", foreground = "#292929", font=("cambria", 11), background="#ffffff")
        self.want.place(x=310, y=17)
        self.SearchBar = Entry(self.MainFrame2, width=51, textvariable=self.buscar, font=("cambria", 13))
        self.SearchBar.place(x=315, y=40)
        self.searchButton = Button(image=self.buscar, command=lambda:self.search())
        self.searchButton.place(x=790, y=40)

        #-----Button
        self.AdmButton = tk.Button(self.MainFrame2,border=0 , image = self.AdmImg, command=lambda:self.adminWindow()).place(x=22, y=20)
        self.Reportar = Button(self.MainFrame2, text="Reportar inconveniente", command=lambda:self.error())
        self.Reportar.place(x=315, y=152)
        self.enviar = Button(self.MainFrame2, text="Trabajo completado!", command=lambda:self.complete())
        self.enviar.place(x=455, y=152)
        self.completados = Button(self.MainFrame2, text="Trabajos completados", command=lambda:self.completed())
        self.completados.place(x=582, y=152)
        self.anotaciones = Button(self.MainFrame2, text="Ver descripcion", command=lambda:self.sipnosis())
        self.anotaciones.place(x=715, y=152)
        self.asigned = Button(self.MainFrame2, text="Trabajos que he asignado", width=20,style = "bt.TButton", command=lambda:self.asignedObjetive())
        self.asigned.place(x=50, y=285)
        Radiobutton(self.infoData, text="Objetivo", value=1, variable=self.radio, style='radio.TRadiobutton').place(x=5, y=5)
        Radiobutton(self.infoData, text="Equipo", value=2, variable=self.radio, style='radio.TRadiobutton').place(x=90, y=5)
        Radiobutton(self.infoData, text="Fecha de asignacion", value=3, variable=self.radio, style='radio.TRadiobutton').place(x=170, y=5)
        Radiobutton(self.infoData, text="Fecha de entrega", value=4, variable=self.radio, style='radio.TRadiobutton').place(x=310, y=5)
        Radiobutton(self.infoData, text="Todos", value=5, variable=self.radio, style='radio.TRadiobutton', command=lambda:self.getQuery()).place(x=430, y=5)
        #Tabla
        self.tabla = Treeview(self.frame, height=17, column=("#1", "#2", "#3", "#4"))
        self.tabla.heading("#0", text="Objetivo", anchor = "center")
        self.tabla.column("#0", width=230)
        self.tabla.heading("#1", text="Equipo", anchor = "center")
        self.tabla.column("#1", width=140)
        self.tabla.heading("#2", text="Fecha de entrega", anchor = "center")
        self.tabla.column("#2", width=140)
        self.tabla.heading("#3", text="Fecha de asignacion", anchor = "center")
        self.tabla.column("#3", width=140)
        self.tabla.heading("#4", text="Recompensa", anchor = "center")
        self.tabla.column("#4", width=150)
        self.tabla.grid(row=0, column=0)
        yscroll = Scrollbar(self.frame, command=self.tabla.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.tabla.config(yscroll=yscroll.set)
        self.getQuery()
        self.OldInfo()
        #bindings
        PerfilLabel.bind("<Button-1>", self.perfil)
        hilo = threading.Thread(target=self.Verificador)
        hilo.start()

        self.raiz.mainloop()

    def Verificador(self):
        while True:
            time.sleep(30)
            try:
                self.receptor = datos[1]
                bd = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
                bd.names="utf8"
                self.cursor = bd.cursor()
                self.parameters = ("En proceso", self.receptor)
                self.cursor.execute("Select * from tbobjetivos where estatus = %s and nombreUser =%s", self.parameters)
                self.residuo = self.cursor.fetchall()
                bd.commit()
                if self.residuo == self.oldResult:
                    pass
                elif self.residuo != self.oldResult and self.userW == True:
                    self.getQuery()
                    self.OldInfo()
            except TclError:
                self.Verificador()

    def OldInfo(self):
            self.receptor = datos[1]
            bdd = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
            bdd.names="utf8"
            self.cursor = bdd.cursor()
            self.parameters = ("En proceso", self.receptor)
            self.cursor.execute("Select * from tbobjetivos where estatus = %s and nombreUser =%s", self.parameters)
            self.oldResult = self.cursor.fetchall()
            bdd.commit()

    def perfil(self, event):
        self.raiz.withdraw()
        perfil0 = perfil(self.perfilImage, self.raiz)

    def adminWindow(self):
        if datos[4] == "Administrador":
            #Altering existing GUI
            self.UserButton = tk.Button(self.MainFrame2,border=0, image = self.UserImg, command=lambda:self.userWindow()).place(x=22, y=20)
            self.completeAd = Button(self.MainFrame2, text="Ver trabajos completados", width=20, style = "bt.TButton", command=lambda:self.getCompletedAdminQuery())
            self.completeAd.place(x=560, y=10)
            self.completados.destroy()
            self.enviar.destroy()
            self.anotaciones.destroy()
            self.Reportar.destroy()
            self.infoData.destroy()
            self.want.destroy()
            self.SearchBar.destroy()
            self.searchButton.destroy()
            self.asigned.destroy()
            #Creating data
            self.remitente = datos[1]
            self.asignDate = time.strftime("20%y-%m-%d")
            self.estado = "En proceso"
            self.completeDate = "None"
            #Creating new GUI
            self.frame = Labelframe(text="Asignar nuevo objetivo", width=498, height=172, style='lstyle.TLabelframe')
            self.frame.place(x=315, y=23)
            #-----Labels
            Label(self.frame, text="Receptor: ", background="#ffffff", font=("cambria", 12)).place(x=5, y=9)
            Label(self.frame,text="Equipo: ", background="#ffffff", font=("cambria", 12)).place(x=5, y=59)
            Label(self.frame,text="Titulo:", background="#ffffff", font=("cambria", 12)).place(x=210, y=7)
            Label(self.frame,text="Entrega: ", background="#ffffff", font=("cambria", 12)).place(x=210, y=57)
            Label(self.frame,text="Valor: ", background="#ffffff", font=("cambria", 12)).place(x=350, y=57)

            #-----Entrys
            self.username = Entry(self.frame, textvariable = self.nombre)
            self.username.focus()
            self.username.place(x=76, y=9)
            self.team = Entry(self.frame, textvariable = self.equipo)
            self.team.place(x=63, y=59)
            self.title = Entry(self.frame, textvariable = self.titulo)
            self.title.place(x=258, y=9)
            self.entrega = Entry(self.frame, textvariable = self.entry, width=10)
            self.entrega.place(x=273, y=59)
            self.valor = Entry(self.frame, textvariable = self.val, width=10)
            self.valor.place(x=400, y=59)
            self.descripcion = Button(self.MainFrame2, text="Asignar descripcion", width=17, style = "bt2.TButton", command=lambda:self.annotations())
            self.descripcion.place(x=325, y=150)
            self.objetive = Button(self.MainFrame2, text="Asignar objetivo", width=17, style = "bt2.TButton", command=lambda:self.setQuery())
            self.objetive.place(x=660, y=150)
            self.editButton = Button(self.MainFrame2, text="Editar objetivo", width=17, style = "bt.TButton", command=lambda:self.edit())
            self.editButton.place(x=486, y=150)
            self.describe = ""
            self.getAdminQuery()
        else:
            ms.showinfo("Aviso", "Usted no posee las credenciales para acceder a la version de administrador.")

    def userWindow(self):
        #buttons
        self.AdmButton = tk.Button(self.MainFrame2,border=0, image = self.AdmImg, command=lambda:self.adminWindow()).place(x=22, y=20)
        self.Reportar = Button(self.MainFrame2, text="Reportar inconveniente", command=lambda:self.error())
        self.Reportar.place(x=315, y=152)
        self.enviar = Button(self.MainFrame2, text="Trabajo completado!", command=lambda:self.complete())
        self.enviar.place(x=455, y=152)
        self.completados = Button(self.MainFrame2, text="Trabajos completados", command=lambda:self.completed())
        self.completados.place(x=582, y=152)
        self.anotaciones = Button(self.MainFrame2, text="Ver descripcion", command=lambda:self.sipnosis())
        self.anotaciones.place(x=715, y=152)
        self.asigned = Button(self.MainFrame2, text="Trabajos asignados", width=20,style = "bt.TButton", command=lambda:self.asignedObjetive())
        self.asigned.place(x=50, y=285)
        #entry
        self.want = Label(self.MainFrame2, text="Buscar", foreground = "#292929", font=("cambria", 11), background="#ffffff")
        self.want.place(x=310, y=17)
        self.SearchBar = Entry(self.MainFrame2, width=51, textvariable=self.buscar, font=("cambria", 13))
        self.SearchBar.place(x=315, y=40)
        self.searchButton = Button(image=self.buscar, command=lambda:self.search())
        self.searchButton.place(x=790, y=40)
        #frame
        self.infoData = Labelframe(self.MainFrame2 ,text= "Filtros", width=500, height=55, style = 'lstyle.TLabelframe')
        self.infoData.place(x=315, y=70)
        #radio
        Radiobutton(self.infoData, text="Objetivo", value=1, variable=self.radio, style='radio.TRadiobutton').place(x=5, y=5)
        Radiobutton(self.infoData, text="Equipo", value=2, variable=self.radio, style='radio.TRadiobutton').place(x=90, y=5)
        Radiobutton(self.infoData, text="Fecha de asignacion", value=3, variable=self.radio, style='radio.TRadiobutton').place(x=170, y=5)
        Radiobutton(self.infoData, text="Fecha de entrega", value=4, variable=self.radio, style='radio.TRadiobutton').place(x=310, y=5)
        Radiobutton(self.infoData, text="Todos", value=5, variable=self.radio, style='radio.TRadiobutton', command=lambda:self.getQuery()).place(x=430, y=5)
        #destroy
        self.completeAd.destroy()
        self.descripcion.destroy()
        self.editButton.destroy()
        self.frame.destroy()
        self.objetive.destroy()
        self.getQuery()

    def setQuery(self):
        if self.describe == "":
            ms.showinfo("Alerta", "Debe ingresar una descripcion para el objetivo")
        else:
            query = "INSERT INTO tbobjetivos VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            parameters = (self.username.get(), self.remitente, self.team.get(), self.title.get(), self.describe, self.entrega.get(), self.estado, self.asignDate, self.completeDate, self.val.get())
            self.editmode = False
            consulta = "SELECT * FROM tbperfilusuarios where usuario = %s"
            parametros = (self.username.get(),)
            rows = self.checkQuery(consulta, parametros)
            for row in rows:
                self.correo = row[7]
            self.fechaEntrega = self.entrega.get()
            self.tituloMail = self.title.get()
            self.asignante = self.username.get()
            self.sendEmail()
            self.sendEmailadm()
            self.checkQuery_complete(query, parameters)
            self.getAdminQuery()

    def sipnosis(self):
        data = self.tabla.item(self.tabla.selection())['values'][4]
        info = Toplevel()
        info.geometry("900x700+300-100")
        info.resizable(0,0)
        info.title("Descripcion")
        info.config(bg="#ffffff")
        Label(info, text="Descripcion", background="#ffffff").pack(pady=5, padx=5)
        infor = Text(info, width=110, height=37, font=("cambria", 11))
        infor.insert("insert", data)
        infor.config(state=DISABLED)
        infor.pack(pady=5, padx=5)

    def getAdminQuery(self):
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting the query
        query = "SELECT * FROM tbobjetivos where estatus = %s"
        parameters = ("En proceso",)
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8],row[10], row[5], row[0], row[1]))
        self.completeAd.destroy()
        self.completeAd = Button(self.MainFrame2, text="Ver trabajos completados", width=20, style = "bt.TButton", command=lambda:self.getCompletedAdminQuery())
        self.completeAd.place(x=50, y=285)

    def getCompletedAdminQuery(self):
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting the query
        query = "SELECT * FROM tbobjetivos where estatus = %s"
        parameters = ("cumplido", )
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8],row[10], row[5], row[0], row[1]))
        self.completeAd.destroy()
        self.completeAd = Button(self.MainFrame2, text="Ver trabajos en proceso", width=20, style = "bt.TButton", command=lambda:self.getAdminQuery())
        self.completeAd.place(x=50, y=285)

    def checkQuery(self, query, parameters=()):
        self.dbb = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
        self.dbb.names="utf8"
        cursor = self.dbb.cursor()
        cursor.execute(query, parameters)
        resultados = cursor.fetchall()
        self.dbb.commit()
        return resultados

    def checkQuery_complete(self, query, parameters=()):
        self.dbb = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
        self.dbb.names="utf8"
        cursor = self.dbb.cursor()
        cursor.execute(query, parameters)
        self.dbb.commit()

    def getQuery(self):
        self.userW = True
        #cosmetic
        self.asigned['text']="Trabajos que he asignado"
        self.asigned['command']=lambda:self.asignedObjetive()
        self.asigned['width']=22
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting the query
        self.receptor = datos[1]
        query = "SELECT * FROM tbobjetivos where estatus = %s and nombreUser =%s"
        parameters = ("En proceso", self.receptor)
        self.rows = self.checkQuery(query, parameters)
        for row in self.rows:
            self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8],row[10], row[5], row[0], row[1], row[2]))
        self.completados.destroy()
        self.completados = Button(self.MainFrame2, text="Trabajos completados", command=lambda:self.completed())
        self.completados.place(x=582, y=152)
        self.radio.set(5)
        self.completeSearch = True

    def complete(self):
        #Updating table's info
        ID = (self.tabla.item(self.tabla.selection())["values"][5])
        puntuacion = (self.tabla.item(self.tabla.selection())["values"][3])
        newParameter = "cumplido"
        parameters = (newParameter, ID)
        query = "UPDATE tbobjetivos SET estatus = %s WHERE ID = %s"
        self.completeDate = time.strftime("20%y-%m-%d, %H:%M:%S")
        self.obj = (self.tabla.item(self.tabla.selection())["values"][4])
        self.date = (self.tabla.item(self.tabla.selection())["values"][1])
        self.asignado = (self.tabla.item(self.tabla.selection())["values"][7])
        self.titulo = (self.tabla.item(self.tabla.selection())["text"])
        self.totalPoints = datos[15]
        self.levelUpNeed = datos[17]
        self.levelUpNeed = self.levelUpNeed - puntuacion
        self.totalPoints = self.totalPoints + puntuacion
        if self.levelUpNeed <= 0:
            self.levelUpNeed = 0
        neededParameters = (self.levelUpNeed, datos[1])
        UsuariosParameters = (self.totalPoints, datos[1])
        UsuariosQuery = "UPDATE tbperfilusuarios SET puntuacionAcumulada = %s where usuario = %s"
        neededQuery = "UPDATE tbperfilusuarios SET puntuacionRestante = %s where usuario = %s"
        self.checkQuery_complete(UsuariosQuery, UsuariosParameters)
        self.checkQuery_complete(neededQuery, neededParameters)
        self.checkQuery_complete(query, parameters)
        self.getQuery()
        self.completeMail()

    def completeMail(self):
            try:
                self.cuerpo = """<div id='cuerpo-email' style='width: 50%;
                                                                      border:1px solid black;
                                                                      border-radius:5px;
                                                                      padding:1%;
                                                                      margin-left:auto;
                                                                      margin-right: auto;
                                                                      width: 40%;
                                                                      font-family:arial;'>
                                      <ul style='list-style:none;'>
                                            <li><h2>Objetivo completado!</h2></li>
                                            <li><h3>El objetivo ha sido asignado por <span style='color:#1470B3;'>""" + self.asignado + """</span></h3></li>
                                            <li><h3>Fecha limite: """ + str(self.date) +""" </h3></li>
                                            <li> <h3 style='color:#1470B3;'>""" + self.titulo + """</h3></li>
                                            <li> <div id='contenido-email' style='width: 90%;
                                                                                        border-radius:5px;
                                                                                        padding:1%;
                                                                                        margin-left:auto;
                                                                                        margin-right: auto;'>
                                                <p>""" + self.obj + """</p>
                                                </div></li>
                                        </ul>
                                    </div>"""
                self.header = MIMEMultipart()
                self.header['Subject'] = self.titulo
                self.mensaje = MIMEText(self.cuerpo, 'html')
                self.header.attach(self.mensaje)
                self.servidor = smtplib.SMTP('smtp.gmail.com', 587)
                self.servidor.starttls()
                self.servidor.login("nowhere.negocios@gmail.com", "nowhere999999")
                self.servidor.sendmail("nowhere.negocios@gmail.com", 'Ezequielgm677@gmail.com', self.mensaje.as_string())
                self.servidor.sendmail("nowhere.negocios@gmail.com", 'lugiazekrom45@gmail.com', self.header.as_string())
                self.servidor.quit()
                ms.showinfo("Aviso", "El correo ha sido enviado satisfactoriamente")
            except smtplib.SMTPAuthenticationError:
                    ms.showwarning("Alerta", "El nombre de usuario o contraseña es incorrecto.")

    def sendEmail(self):
            try:
                self.cuerpo = """<div id='cuerpo-email' style='width: 50%;
                                                                      border:1px solid black;
                                                                      border-radius:5px;
                                                                      padding:1%;
                                                                      margin-left:auto;
                                                                      margin-right: auto;
                                                                      width: 40%;
                                                                      font-family:arial;'>
                                      <ul style='list-style:none;'>
                                            <li><h2>¡Se te ha asignado un nuevo objetivo!</h2></li>
                                            <li><h3>El objetivo ha sido asignado por <span style='color:#1470B3;'>""" + self.remitente + """</span></h3></li>
                                            <li><h3>Fecha limite: """ + self.fechaEntrega +""" </h3></li>
                                            <li> <h3 style='color:#1470B3;'>""" + self.tituloMail + """</h3></li>
                                            <li> <div id='contenido-email' style='width: 90%;
                                                                                        border-radius:5px;
                                                                                        padding:1%;
                                                                                        margin-left:auto;
                                                                                        margin-right: auto;'>
                                                <p>""" + self.describe + """</p>
                                                </div></li>
                                        </ul>
                                    </div>"""
                self.header = MIMEMultipart()
                self.header['Subject'] = self.tituloMail
                self.mensaje = MIMEText(self.cuerpo, 'html')
                self.header.attach(self.mensaje)
                self.servidor = smtplib.SMTP('smtp.gmail.com', 587)
                self.servidor.starttls()
                self.servidor.login("nowhere.negocios@gmail.com", "nowhere999999")
                self.servidor.sendmail("nowhere.negocios@gmail.com", self.correo, self.header.as_string())
                self.servidor.sendmail("nowhere.negocios@gmail.com", 'Ezequielgm677@gmail.com', self.mensaje.as_string())
                self.servidor.quit()
                ms.showinfo("Aviso", "El correo ha sido enviado satisfactoriamente")
            except smtplib.SMTPAuthenticationError:
                    ms.showwarning("Alerta", "El nombre de usuario o contraseña es incorrecto.")

    def sendEmailadm(self):
        try:
            self.cuerpo = """<div id='cuerpo-email' style='width: 50%;
                                                                  border:1px solid black;
                                                                  border-radius:5px;
                                                                  padding:1%;
                                                                  margin-left:auto;
                                                                  margin-right: auto;
                                                                  width: 40%;
                                                                  font-family:arial;'>
                                  <ul style='list-style:none;'>
                                        <li><h2>Se ha asignado un nuevo objetivo!</h2></li>
                                        <li><h3>El objetivo ha sido asignado por <span style='color:#1470B3;'>""" + self.remitente + """</span></h3></li>
                                        <li><h3>Para: """ + self.asignante + """<span style='color:#1470B3;'></span></h3></li>
                                        <li><h3>Fecha limite: """ + self.fechaEntrega +""" </h3></li>
                                        <li> <h3 style='color:#1470B3;'>""" + self.tituloMail + """</h3></li>
                                        <li> <div id='contenido-email' style='width: 90%;
                                                                                    border-radius:5px;
                                                                                    padding:1%;
                                                                                    margin-left:auto;
                                                                                    margin-right: auto;'>
                                            <p>""" + self.describe + """</p>
                                            </div></li>
                                    </ul>
                                </div>"""
            self.header = MIMEMultipart()
            self.header['Subject'] = self.tituloMail
            self.mensaje = MIMEText(self.cuerpo, 'html')
            self.header.attach(self.mensaje)
            self.servidor = smtplib.SMTP('smtp.gmail.com', 587)
            self.servidor.starttls()
            self.servidor.login("nowhere.negocios@gmail.com", "nowhere999999")
            self.servidor.sendmail("nowhere.negocios@gmail.com", 'Ezequielgm677@gmail.com', self.mensaje.as_string())
            self.servidor.sendmail("nowhere.negocios@gmail.com", "lugiazekrom45@gmail.com", self.header.as_string())
            self.servidor.quit()
            ms.showinfo("Aviso", "El correo ha sido enviado satisfactoriamente")
        except smtplib.SMTPAuthenticationError:
                ms.showwarning("Alerta", "El nombre de usuario o contraseña es incorrecto.")

    def error(self):
        self.newR = Toplevel()
        self.newR.geometry("250x200")
        self.newR.resizable(0,0)
        self.newR.config(bg="#ffffff")
        self.newR.title("Reportar error")
        Label(self.newR, text="Especifique el error.", background="#ffffff", font=("Cambria", 11)).place(x=5, y=5)
        self.texto = Text(self.newR, width=28, height=8, font=("cambria", 11))
        self.texto.place(x=5, y=30)
        button = Button(self.newR, text="Enviar", command=lambda:self.enviarError()).place(x=5, y=170)
        button = Button(self.newR, text="Cancelar").place(x=170, y=170)
        self.newR.mainloop()

    def search(self):
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting
        if self.completeSearch == False:
            if self.radio.get() == 1:
                query = "SELECT * FROM tbobjetivos WHERE Titulo = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "En proceso")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
            elif self.radio.get() == 2:
                query = "SELECT * FROM tbobjetivos WHERE equipo = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "En proceso")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
            elif self.radio.get() == 3:
                query = "SELECT * FROM tbobjetivos WHERE asignado = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "En proceso")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
            elif self.radio.get() == 4:
                query = "SELECT * FROM tbobjetivos WHERE entrega = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "En proceso")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
        else:
            if self.radio.get() == 1:
                query = "SELECT * FROM tbobjetivos WHERE Titulo = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "cumplido")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
            elif self.radio.get() == 2:
                query = "SELECT * FROM tbobjetivos WHERE equipo = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "cumplido")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
            elif self.radio.get() == 3:
                query = "SELECT * FROM tbobjetivos WHERE asignado = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "cumplido")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))
            elif self.radio.get() == 4:
                query = "SELECT * FROM tbobjetivos WHERE entrega = %s and nombreUser = %s and estatus = %s"
                parameters = (self.SearchBar.get(), datos[1], "cumplido")
                rows = self.checkQuery(query, parameters)
                for row in rows:
                    self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8], row[5], row[0], row[1]))

    def enviarError(self):
        self.mensajes = self.texto.get(1.0, "end")
        self.newR.destroy()
        self.newEmail = Toplevel()
        self.newEmail.config(bg="#ffffff")
        Label(self.newEmail, text="Indroduzca su correo", background="#ffffff").pack(pady=5, padx=10)
        self.correo = Entry(self.newEmail)
        self.correo.pack(pady=5, padx=10)
        self.correo.focus()
        Label(self.newEmail, text="Introduzca su contraseña", background="#ffffff").pack(pady=5, padx=10)
        self.password = Entry(self.newEmail)
        self.password.pack(pady=5, padx=10)
        self.boton = Button(self.newEmail, text="Enviar", command=lambda:self.email()).pack(pady=5, padx=5)

    def email(self):
        try:
            try:
                self.cuerpo = self.mensajes
                self.asunto = "Error de W-work"
                self.mensaje = 'Subject: {}\n\n{}'.format(self.asunto, self.cuerpo)
                self.servidor = smtplib.SMTP('smtp.gmail.com', 587)
                self.servidor.starttls()
                self.servidor.login(self.correo.get(), self.password.get())
                self.servidor.sendmail(self.correo.get(), 'lugiazekrom45@gmail.com', self.mensaje)
                self.servidor.quit()
                ms.showinfo("Aviso", "El correo ha sido enviado satisfactoriamente")
            except smtplib.SMTPAuthenticationError:
                    ms.showwarning("Alerta", "El nombre de usuario o contraseña es incorrecto.")
        except TypeError:
            ms.showwarning("Alerta", "Llene los espacios con la información correspondiente")

    def annotations(self):
        if self.editmode == True:
            self.descr = Toplevel()
            self.descr.geometry("900x700+300-100")
            self.descr.resizable(0,0)
            self.descr.config(bg="#ffffff")
            self.descr.title("Descripcion")
            Label(self.descr, text="Describa el objetivo.", background="#ffffff", font=("Cambria", 11)).place(x=5, y=5)
            self.describir = Text(self.descr, width=110, height=37, font=("cambria", 11))
            self.describir.place(x=7, y=33)
            self.describir.insert('insert', self.descripEdit)
            button = Button(self.descr, text="Listo", command=lambda:self.asigndescr()).place(x=7, y=672)
            self.descr.mainloop()

        elif self.editmode == False:
            self.descr = Toplevel()
            self.descr.geometry("900x700+300-100")
            self.descr.resizable(0,0)
            self.descr.config(bg="#ffffff")
            self.descr.title("Descripcion")
            Label(self.descr, text="Describa el objetivo.", background="#ffffff", font=("Cambria", 11)).place(x=5, y=5)
            self.describir = Text(self.descr, width=110, height=37, font=("cambria", 11))
            self.describir.place(x=7, y=33)
            button = Button(self.descr, text="Listo", command=lambda:self.asigndescr()).place(x=7, y=672)
            self.descr.mainloop()

    def asigndescr(self):
        self.describe = self.describir.get(1.0, "end")
        self.descr.destroy()

    def completed(self):
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting the query
        self.receptor = datos[1]
        query = "SELECT * FROM tbobjetivos where estatus = %s and nombreUser = %s"
        parameters = ("cumplido", self.receptor)
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8],row[10], row[5], row[0], row[1]))
        self.completados.destroy()
        self.completados = Button(self.MainFrame2, text="Trabajos en proceso", command=lambda:self.getQuery())
        self.completados.place(x=582, y=152)
        self.completeSearch = True

    def asignedObjetive(self):
        #cosmetic
        self.asigned['text']="Mis trabajos pendientes"
        self.asigned['command']=lambda:self.getQuery()
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting the query
        query = "SELECT * FROM tbobjetivos where estatus = %s and encargado =%s"
        parameters = ("En proceso", datos[1])
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8],row[10], row[5], row[0], row[1]))
        self.completados.destroy()
        self.completados = Button(self.MainFrame2, text="Trabajos completados", command=lambda:self.asignedObjetiveClte())
        self.completados.place(x=582, y=152)
        self.radio.set(5)
        self.completeSearch = True

    def asignedObjetiveClte(self):
        #cleaning table
        save = self.tabla.get_children()
        for item in save:
            self.tabla.delete(item)
        #getting the query
        self.emisor = datos[1]
        query = "SELECT * FROM tbobjetivos where estatus = %s and encargado = %s"
        parameters = ("cumplido", self.emisor)
        rows = self.checkQuery(query, parameters)
        for row in rows:
            self.tabla.insert('', 0, text=row[4], values=(row[3], row[6], row[8],row[10], row[5], row[0], row[1]))
        self.completados.destroy()
        self.completados = Button(self.MainFrame2, text="Trabajos en proceso", command=lambda:self.getQuery())
        self.completados.place(x=582, y=152)
        self.completeSearch = True

    def edit(self):
        self.editmode = True
        self.descripEdit = self.tabla.item(self.tabla.selection())['values'][4]
        Nobjetivo = self.tabla.item(self.tabla.selection())['text']
        Nequipo = self.tabla.item(self.tabla.selection())['values'][0]
        Fentrega = self.tabla.item(self.tabla.selection())['values'][1]
        Nreceptor = self.tabla.item(self.tabla.selection())['values'][6]
        idd = self.tabla.item(self.tabla.selection())['values'][5]
        self.nombre.set(Nreceptor)
        self.equipo.set(Nequipo)
        self.titulo.set(Nobjetivo)
        self.entry.set(Fentrega)
        query = "DELETE FROM tbobjetivos WHERE ID = %s"
        parameters = (idd,)
        self.checkQuery_complete(query, parameters)
        self.getAdminQuery()

class SegundoPlano:
    def __init__(self):
        self.OldInfo()
        core = threading.Thread(target=self.validacion)
        core.start()

    def validacion(self):
        while True:
            time.sleep(300)
            try:
                self.receptor = datos[1]
                bd = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
                bd.names="utf8"
                self.cursor = bd.cursor()
                self.parameters = ("En proceso", self.receptor)
                self.cursor.execute("Select * from tbobjetivos where estatus = %s and nombreUser =%s", self.parameters)
                self.residuo = self.cursor.fetchall()
                bd.commit()
                if self.residuo == self.oldData:
                    pass
                elif self.residuo != self.oldData:
                    self.OldInfo()
                    notificacion = ToastNotifier()
                    notificacion.show_toast("H-Work", (datos[1] + " tienes un trabajo nuevo"), duration=5)
            except TclError:
                self.Verificador()

    def OldInfo(self):
        self.receptor = datos[1]
        dbb = mysql.connector.connect(host="213.190.6.85", user="u751442928_ezequielguzman", passwd="&aRgqT>L", database='u751442928_dbnowhere', charset="utf8")
        dbb.names="utf8"
        cursor = dbb.cursor()
        self.parameters = ("En proceso", self.receptor)
        cursor.execute("Select * from tbobjetivos where estatus = %s and nombreUser =%s", self.parameters)
        self.oldData = cursor.fetchall()
        dbb.commit()
        return self.oldData

if __name__ == "__main__":
    #login window
    loginWindow = login()
