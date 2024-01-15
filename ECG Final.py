##
import tkinter as tk

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scipy.signal import find_peaks
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import ImageTk ,Image
from matplotlib import style
from scipy.misc import electrocardiogram
import scipy.signal as sc
import struct

'''Configuramos la Ventana'''
ventana = tk.Tk()                # Definimos la ventana con nombre window
ventana.geometry('800x550')      # Tamaño de la ventana
ventana.title('ECG')
ventana.config(cursor="heart", bg="white")


'''Definimos los Frames y sus configuraciones para organizar la GUI'''
framegrafica = tk.Frame(master=ventana)
framegrafica.place(x=160, y=45)
framegrafica.config(bg="snow", width=130, height=35, relief=tk.GROOVE, bd=2)
lbl_titulo1 = tk.Label(master=framegrafica, bg="snow", font=('Comic Sans MS', 12, 'bold italic'), text="Señal de ECG")
lbl_titulo1.place(x=1,y=0)

frameparametros=tk.Frame(master=ventana)
frameparametros.place(x = 480, y=30)
frameparametros.config(bg = "lemon chiffon", width = 280, height = 200, relief = tk.GROOVE, bd = 2)
lbl_titulo2 = tk.Label(master=frameparametros, bg="lemon chiffon", font=('Comic Sans MS', 15, 'bold italic'), text="Parametros")
lbl_titulo2.place(x=90,y=10)


frameED=tk.Frame(master=ventana)
frameED.place(x=480,y=238)
frameED.config(bg="lavenderblush2",width=280, height=300,relief=tk.GROOVE,bd=2)
lbl_titulo3 = tk.Label(master=frameED, bg="lavenderblush2", font=('Comic Sans MS', 15, 'bold italic'), text="Metodo de solucion ED")
lbl_titulo3.place(x=30,y=10)

frametabla=tk.Frame(master=ventana)
frametabla.place(x=90, y=390)
frametabla.config(bg="azure",width=335, height=150, relief=tk.GROOVE,bd=2)
lbl_titulo4 = tk.Label(master=frametabla, bg="azure", font=('Comic Sans MS', 15, 'bold italic'), text="P")
lbl_titulo4.place(x=59,y=3)
lbl_titulo5 = tk.Label(master=frametabla, bg="azure", font=('Comic Sans MS', 15, 'bold italic'), text="Q")
lbl_titulo5.place(x=113,y=3)
lbl_titulo6 = tk.Label(master=frametabla, bg="azure", font=('Comic Sans MS', 15, 'bold italic'), text="R")
lbl_titulo6.place(x=172,y=3)
lbl_titulo7 = tk.Label(master=frametabla, bg="azure", font=('Comic Sans MS', 15, 'bold italic'), text="S")
lbl_titulo7.place(x=231,y=3)
lbl_titulo8 = tk.Label(master=frametabla, bg="azure", font=('Comic Sans MS', 15, 'bold italic'), text="T")
lbl_titulo8.place(x=290,y=3)

frameaibi = tk.Frame(master = frametabla)
frameaibi.place(x=0,y = 45)
frameaibi.config(bg ="lemon chiffon", width = 330, height = 100, bd = 2)
lbl_titulo9 = tk.Label(master=frameaibi, bg="lemon chiffon", font=('Comic Sans MS', 20, 'bold italic'), text="ai")
lbl_titulo9.place(x=3,y=0)
lbl_titulo10 = tk.Label(master=frameaibi, bg="lemon chiffon", font=('Comic Sans MS', 20, 'bold italic'), text="bi")
lbl_titulo10.place(x=3,y=40)

frameMetodos = tk.Frame(master = ventana)
frameMetodos.place(x = 40, y= 105)
frameMetodos.config(bg = "pink", width = 400, height = 203, bd = 2)




def Cerrar():
    MsgBox = tk.messagebox.askquestion ('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?',icon = 'warning')
    if MsgBox == 'yes':
       ventana.destroy()
    else:
        tk.messagebox.showinfo('Retornar','Será retornado a la aplicación')

def frecuencia():
    tk.messagebox.showinfo("","Ha ingresado la frecuencia cardiaca")
def latidos():
    tk.messagebox.showinfo("","Ha ingresado el numero de latidos que desea ver")
def muestreo():
    tk.messagebox.showinfo("","Ha ingresado la frecuencia de muestreo")
def ruido():
    tk.messagebox.showinfo("","Ha ingresado  el factor de ruido")




Style = ttk.Style()       #Objeto para crear estilos  # https://kite.com/python/docs/ttk.Style
Style.configure('1.TButton', font=('Arial', 10, 'bold italic'), foreground = 'black', background='black')
Style.configure('2.TButton', font =('Times', 15 , 'bold',), foreground = 'black',background="indianred1")
Style.configure('3.TButton', font =('Times', 10, 'bold',), foreground = 'black',background="gray1")

Style.map("1.TButton",
          foreground=[('pressed', 'MediumPurple3'), ('active', 'MediumPurple3')],
          background=[('pressed', '!disabled', 'Mediumpurple3'), ('active', 'mediumpurple3')])

Style.map("2.TButton",
           foreground=[('pressed', 'red'), ('active', 'red')],
           background=[('pressed', '!disabled', 'red'), ('active', 'red')])
Style.map("3.TButton",
           foreground=[('pressed', 'blue'), ('active', 'blue')],
           background=[('pressed', '!disabled', 'black'), ('active', 'white')])
Style.map("4.TButton",
          foreground = [('pressed', 'darkgoldenrod1'), ('active', 'darkgoldenrod1')],
          background = [('pressed', '!disabled', 'black'), ('active', 'white')])
Style.map("5.TButton",
          foreground = [('pressed', 'azure'), ('active', 'black')],
          background = [('pressed', '!disabled', 'black'), ('active', 'white')])

Botoncerrar = ttk.Button(master=ventana, text="x", style="2.TButton", command=Cerrar)
Botoncerrar.place(x=10,y=4)
Botoncerrar.config(width=3)


#botones de parametros
Botonfrecuenciacardiaca  = ttk.Button(master = frameparametros, text = "Frecuencia cardiaca", style = "4.TButton"
                                    ,command=frecuencia , width = 20).place(x= 15, y = 50)
Botonnumerolatidos  = ttk.Button(master = frameparametros, text = "Numero latidos", style = "4.TButton"
                                 ,command= latidos, width = 20).place(x= 15, y = 80)
Botonfactorruido  = ttk.Button(master = frameparametros, text = "Factor ruido", style = "4.TButton"
                               ,command=ruido, width = 20).place(x= 15, y = 140)
Botonfactormuestreo  = ttk.Button(master = frameparametros, text = "Factor muestreo", style = "4.TButton"
                                  ,command=muestreo, width = 20).place(x= 15, y = 110)
def anchoAlto():
    tk.messagebox.showinfo("", "Alto y ancho configurado")

BotonAiBi  = ttk.Button(master = frameaibi, text = "Insertar", style = "4.TButton"
                                  ,command=anchoAlto, width = 10).place(x= 120, y = 27)

#Crea variable y casilla respectiva
var_frecuenciacardiaca = tk.StringVar()
ent_frecuenciacardiaca = ttk.Entry(master = frameparametros, textvariable= var_frecuenciacardiaca ,width = 15)
ent_frecuenciacardiaca.place(x = 160, y = 50)

var_numerolatidos = tk.StringVar()
ent_numerolatidos = ttk.Entry(master = frameparametros, textvariable = var_numerolatidos, width = 15)
ent_numerolatidos.place(x = 160, y = 80)

var_frecuenciamuestreo = tk.StringVar()
ent_frecuenciamuestreo = ttk.Entry(master = frameparametros, textvariable = var_frecuenciamuestreo, width = 15)
ent_frecuenciamuestreo.place(x = 160, y = 110)

var_factorruido = tk.StringVar()
ent_factorruido = ttk.Entry(master = frameparametros, textvariable = var_factorruido, width = 15)
ent_factorruido.place(x = 160, y = 140)


var_hallarHR = tk.StringVar()
label_hallarHR = tk.Label(master = ventana, textvariable = var_hallarHR, width = 15)
label_hallarHR.place(x = 260, y = 340)



#Se crean las variables de la tabla con ai y bi
var_aiP = tk.StringVar()
ent_aiP = ttk.Entry(master = frameaibi, textvariable = var_aiP, width = 5)
ent_aiP.insert(0,"1.2")
ent_aiP.place(x = 56, y = 5)

var_aiQ = tk.StringVar()
ent_aiQ = ttk.Entry(master = frameaibi, textvariable = var_aiQ, width = 5)
ent_aiQ.insert(0,"-5.0")
ent_aiQ.place(x = 110, y = 5)

var_aiR = tk.StringVar()
ent_aiR = ttk.Entry(master = frameaibi, textvariable = var_aiR, width = 5)
ent_aiR.insert(0,"30.0")
ent_aiR.place(x = 169, y = 5)

var_aiS = tk.StringVar()
ent_aiS = ttk.Entry(master = frameaibi, textvariable = var_aiS, width = 5)
ent_aiS.insert(0,"-7.5")
ent_aiS.place(x =228, y = 5)

var_aiT = tk.StringVar()
ent_aiT = ttk.Entry(master = frameaibi, textvariable = var_aiT, width = 5)
ent_aiT.insert(0,"0.75")
ent_aiT.place(x = 287, y = 5)

var_biP = tk.StringVar()
ent_biP = ttk.Entry(master = frameaibi, textvariable = var_biP, width = 5)
ent_biP.insert(0,"0.25")
ent_biP.place(x = 56 , y = 55)

var_biQ = tk.StringVar()
ent_biQ = ttk.Entry(master = frameaibi, textvariable = var_biQ, width = 5)
ent_biQ.insert(0,"0.1")
ent_biQ.place(x = 110, y =55)

var_biR = tk.StringVar()
ent_biR = ttk.Entry(master = frameaibi, textvariable = var_biR, width = 5)
ent_biR.insert(0,"0.1")
ent_biR.place(x = 169, y =55)

var_biS = tk.StringVar()
ent_biS = ttk.Entry(master = frameaibi, textvariable = var_biS, width = 5)
ent_biS.insert(0,"0.1")
ent_biS.place(x = 228, y =55)

var_biT = tk.StringVar()
ent_biT = ttk.Entry(master = frameaibi, textvariable = var_biT, width = 5)
ent_biT.insert(0,"0.4")
ent_biT.place(x = 287 , y =55)


def borrar():
    ent_aiP.delete(0, tk.END)
    ent_aiQ.delete(0, tk.END)
    ent_aiR.delete(0, tk.END)
    ent_aiT.delete(0, tk.END)
    ent_aiS.delete(0, tk.END)
    ent_biP.delete(0, tk.END)
    ent_biQ.delete(0, tk.END)
    ent_biR.delete(0, tk.END)
    ent_biS.delete(0, tk.END)
    ent_biT.delete(0, tk.END)

#boton para reiniciar datos
'''''
img= Image.open("reiniciar.jpeg")
img=img.resize((40,40), Image.ANTIALIAS)
img=ImageTk.PhotoImage(img)
botonreiniciar=tk.Button(ventana, image=img,command=borrar)
botonreiniciar.place(x=20, y=450)
'''''


#ecuaciones
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

''''''''''''"Modelo dinámico del E.C.G"''''''''''''

"Parametros: Orden--> P Q R S T"   #Ejemplo
tetai = np.array([-np.pi/3,-np.pi/12,0,np.pi/12,np.pi/2])
ai = np.array([1.2,-5.0,30.0,-7.5,0.75])
bi = np.array([0.25,0.1,0.1,0.1,0.4])
t0 = 0.001
tf = 8
fs = 340
h = 1/fs
fc = 60 #frecuencia cardiaca
fre = 60/ fc

def difX(x,y,T):
    alpha = 1 - np.sqrt(x**2 + y**2)
    return alpha*x - (2*np.pi*(1/T))*y

def difY(x,y,T):
    alpha = 1 - np.sqrt(x ** 2 + y ** 2)
    return alpha*y + (2*np.pi*(1/T))*x

def difZ(x,y,z,ai,tetai,bi,t):
    iteracionSuma = 0
    fr2 = 0.25 # Frecuencia respiratoria
    for i in range(len(bi)):
        dTeta = np.fmod(np.arctan2(y,x)-tetai[i],2*np.pi)
        iteracionSuma += -( ai[i]*(dTeta)*np.exp(-(dTeta**2)/(2*(bi[i]**2))) )

    return iteracionSuma - z + (0.15/1000)*np.sin(2*np.pi*fr2*t)

class vistaGrafica():
    #Los diferentes vigilantes son: "f"---> euler-forward
    #                               "b"---> euler-back
    #                               "m"---> euler-mod
    #                               "r2"---> RK2
    #                               "r4"---> RK4
    vigilanteGrafica = "no hay selección"  # vigila en que gráfica está seleccionada
    def __init__(self,vigilanteGrafica):
        self.vigilanteGrafica = vigilanteGrafica
    def cambiarEstado(self,valorGrafica):     # Cambia el atributo a la grafica seleccionada
        if valorGrafica == 1:
            self.vigilanteGrafica = "f"
        elif valorGrafica == 2:
            self.vigilanteGrafica = "b"
        elif valorGrafica == 3:
            self.vigilanteGrafica = "m"
        elif valorGrafica == 4:
            self.vigilanteGrafica = "r2"
        elif valorGrafica == 5:
            self.vigilanteGrafica = "r4"
accionGraficadora = vistaGrafica("no hay selección")
'---------------------------------------------------------------------------------------------'



def FEulerBackRoot(vectoXYZ, xAnterior, yAnterior, zAnterior, Ti, tiempoI, h, ai, tetai, bi):
    return [xAnterior + h * difX(vectoXYZ[0], vectoXYZ[1], Ti[0]) - vectoXYZ[0],
            yAnterior + h * difY(vectoXYZ[0], vectoXYZ[1], Ti[0]) - vectoXYZ[1],
            zAnterior + h * difZ(vectoXYZ[0], vectoXYZ[1], vectoXYZ[2], ai, tetai, bi, tiempoI[0]) - vectoXYZ[2]]
#euler modificado
# yt2 -->  Vector de tres posiciones
# donde yt2[0] corresponde al valor de X(i)
# y yt2[1] corresponde al valor de Y(i)
# y yt2[2] corresponde al valor de Z(i)
# t1 --> Tiempo en la iteración i-1
# t2 --> Tiempo en la iteración i
# y1t1 --> Estimación de X1 en la iteración i-1
# y2t1 --> Estimación de Y1 en la iteración i-1
# y3t1 --> Estimación de Z1 en la iteración i-1
# h --> Intervalo entre un tiempo y el
# siguiente (p.ej. t2-t1)
def FEulerModRoot(yt2, t1, t2, y1t1, y2t1,y3t1, h,ai,bi,tetai,tiempo1,tiempo2):
    return [y1t1 + (h / 2.0) * \
           (difX(y1t1,y2t1,t1) + difX(yt2[0],yt2[1],t2)) - yt2[0],
            y2t1 + (h / 2.0) * \
           (difY(y1t1,y2t1,t1) + difY(yt2[0], yt2[1],t2)) - yt2[1],
            y3t1 + (h / 2.0) * \
            (difZ(y1t1,y2t1,y3t1,ai,tetai,bi,tiempo1) + difZ(yt2[0], yt2[1],yt2[2],ai,tetai,bi,tiempo2)) - yt2[2]]

def tiempo():

    fs = int(var_frecuenciamuestreo.get())
    h = 1 / fs
    t0 = 0.001
    tf = int(var_numerolatidos.get())
    tiempo = np.arange(t0,tf + h,h)
    return tiempo

def EulerAdelante():
    fs = int(var_frecuenciamuestreo.get())
    h = 1 / fs
    fc = int(var_frecuenciacardiaca.get())  # frecuencia cardiaca
    tf = int(var_numerolatidos.get())
    fre = 60 / fc
    tiempo = np.arange(t0, tf + h, h)
    T = (np.random.normal(fre, fre * 0.12, len(tiempo)))
    ai = np.array([float(var_aiP.get()),float(var_aiQ.get()),float(var_aiR.get()),float(var_aiS.get()),float(var_aiT.get())])
    bi = np.array([float(var_biP.get()),float(var_biQ.get()),float(var_biR.get()),float(var_biS.get()),float(var_biT.get())])
    x0 = 1
    y0 = 0
    z0 = 0.06
    XEulerFor = np.zeros(len(tiempo))
    YEulerFor = np.zeros(len(tiempo))
    ZEulerFor = np.zeros(len(tiempo))

    XEulerFor[0] = x0
    YEulerFor[0] = y0
    ZEulerFor[0] = z0
    for i in range(1, len(tiempo)):
        XEulerFor[i] = XEulerFor[i - 1] + h * (difX(XEulerFor[i - 1], YEulerFor[i - 1], T[i]))

        YEulerFor[i] = YEulerFor[i - 1] + h * (difY(XEulerFor[i - 1], YEulerFor[i - 1], T[i]))

        ZEulerFor[i] = ZEulerFor[i - 1] + h * \
                       (difZ(XEulerFor[i - 1], YEulerFor[i - 1], ZEulerFor[i - 1], ai, tetai, bi, tiempo[i - 1]))
    return ZEulerFor

def EulerBack():
    fs = int(var_frecuenciamuestreo.get())
    h = 1 / fs
    fc = int(var_frecuenciacardiaca.get())  # frecuencia cardiaca
    tf = int(var_numerolatidos.get())
    fre = 60 / fc
    tiempo = np.arange(t0, tf + h, h)
    T = (np.random.normal(fre, fre * 0.12, len(tiempo)))
    ai = np.array(
        [float(var_aiP.get()), float(var_aiQ.get()), float(var_aiR.get()), float(var_aiS.get()), float(var_aiT.get())])
    bi = np.array(
        [float(var_biP.get()), float(var_biQ.get()), float(var_biR.get()), float(var_biS.get()), float(var_biT.get())])
    x0 = 1
    y0 = 0
    z0 = 0.05
    XEulerBackRoot = np.zeros(len(tiempo))
    YEulerBackRoot = np.zeros(len(tiempo))
    ZEulerBackRoot = np.zeros(len(tiempo))

    XEulerBackRoot[0] = x0
    YEulerBackRoot[0] = y0
    ZEulerBackRoot[0] = z0

    for i in range(1, len(tiempo)):
        # Euler hacia atras
        solucionBack = opt.fsolve(FEulerBackRoot,
                                  np.array([XEulerBackRoot[i - 1], YEulerBackRoot[i - 1], ZEulerBackRoot[i - 1]]), (
                                  XEulerBackRoot[i - 1], YEulerBackRoot[i - 1], ZEulerBackRoot[i - 1], T, tiempo, h, ai,
                                  tetai, bi), xtol=10 ** -5)
        XEulerBackRoot[i] = solucionBack[0]
        YEulerBackRoot[i] = solucionBack[1]
        ZEulerBackRoot[i] = solucionBack[2]
    return ZEulerBackRoot

def EulerModificado():
    fs = int(var_frecuenciamuestreo.get())
    h = 1 / fs
    fc = int(var_frecuenciacardiaca.get())  # frecuencia cardiaca
    tf = int(var_numerolatidos.get())
    fre = 60 / fc
    tiempo = np.arange(t0, tf + h, h)
    T = (np.random.normal(fre, fre * 0.12, len(tiempo)))
    ai = np.array(
        [float(var_aiP.get()), float(var_aiQ.get()), float(var_aiR.get()), float(var_aiS.get()), float(var_aiT.get())])
    bi = np.array(
        [float(var_biP.get()), float(var_biQ.get()), float(var_biR.get()), float(var_biS.get()), float(var_biT.get())])
    x0 = 1
    y0 = 0
    z0 = 0.05

    XEulerModRoot = np.zeros(len(tiempo))
    YEulerModRoot = np.zeros(len(tiempo))
    ZEulerModRoot = np.zeros(len(tiempo))

    XEulerModRoot[0] = x0
    YEulerModRoot[0] = y0
    ZEulerModRoot[0] = z0
    for i in range(1,len(tiempo)):
        SolMod = opt.fsolve(FEulerModRoot,
                            np.array([XEulerModRoot[i - 1], YEulerModRoot[i - 1], ZEulerModRoot[i - 1]]),
                            (T[i - 1], T[i], XEulerModRoot[i - 1], YEulerModRoot[i - 1], ZEulerModRoot[i - 1],
                             h, ai, bi, tetai, tiempo[i - 1], tiempo[i]), xtol=10 ** -5)
        XEulerModRoot[i] = SolMod[0]
        YEulerModRoot[i] = SolMod[1]
        ZEulerModRoot[i] = SolMod[2]
    return ZEulerModRoot


def RK2():
    fs = int(var_frecuenciamuestreo.get())
    h = 1 / fs
    fc = int(var_frecuenciacardiaca.get())  # frecuencia cardiaca
    tf = int(var_numerolatidos.get())
    fre = 60 / fc
    tiempo = np.arange(t0, tf + h, h)
    T = (np.random.normal(fre, fre * 0.12, len(tiempo)))
    ai = np.array(
        [float(var_aiP.get()), float(var_aiQ.get()), float(var_aiR.get()), float(var_aiS.get()), float(var_aiT.get())])
    bi = np.array(
        [float(var_biP.get()), float(var_biQ.get()), float(var_biR.get()), float(var_biS.get()), float(var_biT.get())])
    x0 = 1
    y0 = 0
    z0 = 0.05
    XRK2 = np.zeros(len(tiempo))
    YRK2 = np.zeros(len(tiempo))
    ZRK2 = np.zeros(len(tiempo))

    XRK2[0] = x0
    YRK2[0] = y0
    ZRK2[0] = z0
    for i in range(1, len(tiempo)):
        k11 = difX(XRK2[i - 1], YRK2[i - 1], T[i - 1])
        k21 = difY(XRK2[i - 1], YRK2[i - 1], T[i - 1])
        k31 = difZ(XRK2[i - 1], YRK2[i - 1], ZRK2[i - 1], ai, tetai, bi, tiempo[i - 1])
        k12 = difX(XRK2[i - 1] + k11 * h, YRK2[i - 1] + k21 * h, T[i - 1] + h)
        k22 = difY(XRK2[i - 1] + k11 * h, YRK2[i - 1] + k21 * h, T[i - 1] + h)
        k32 = difZ(XRK2[i - 1] + h * k11, YRK2[i - 1] + h * k21, ZRK2[i - 1] + h * k31, ai, tetai, bi, tiempo[i - 1] + h)
        XRK2[i] = XRK2[i - 1] + (h / 2.0) * (k11 + k12)
        YRK2[i] = YRK2[i - 1] + (h / 2.0) * (k21 + k22)
        ZRK2[i] = ZRK2[i - 1] + (h / 2.0) * (k31 + k32)
    return ZRK2

def RK4():
    fs = int(var_frecuenciamuestreo.get())
    h = 1 / fs
    fc = int(var_frecuenciacardiaca.get())  # frecuencia cardiaca
    tf = int(var_numerolatidos.get())
    fre = 60 / fc
    tiempo = np.arange(t0, tf + h, h)
    T = (np.random.normal(fre, fre * 0.12, len(tiempo)))
    ai = np.array(
        [float(var_aiP.get()), float(var_aiQ.get()), float(var_aiR.get()), float(var_aiS.get()), float(var_aiT.get())])
    bi = np.array(
        [float(var_biP.get()), float(var_biQ.get()), float(var_biR.get()), float(var_biS.get()), float(var_biT.get())])
    x0 = 1
    y0 = 0
    z0 = 0.05
    XRK4 = np.zeros(len(tiempo))
    YRK4 = np.zeros(len(tiempo))
    ZRK4 = np.zeros(len(tiempo))

    XRK4[0] = x0
    YRK4[0] = y0
    ZRK4[0] = z0

    for i in range(1, len(tiempo)):
        k11 = difX(XRK4[i - 1], YRK4[i - 1], T[i - 1])
        k21 = difY(XRK4[i - 1], YRK4[i - 1], T[i - 1])
        k31 = difZ(XRK4[i - 1], YRK4[i - 1], ZRK4[i - 1], ai, tetai, bi, tiempo[i - 1])
        k12 = difX(XRK4[i - 1] + 0.5 * k11 * h, YRK4[i - 1] + 0.5 * k21 * h, T[i - 1] + 0.5 * h)
        k22 = difY(XRK4[i - 1] + 0.5 * k11 * h, YRK4[i - 1] + 0.5 * k21 * h, T[i - 1] + 0.5 * h)
        k32 = difZ(XRK4[i - 1] + 0.5 * h * k11, YRK4[i - 1] + 0.5 * h * k21, ZRK4[i - 1] + 0.5 * h * k31, ai, tetai, bi,
                   tiempo[i - 1] + 0.5*h)
        k13 = difX(XRK4[i - 1] + 0.5 * k12 * h, YRK4[i - 1] + 0.5 * k22 * h, T[i - 1] + 0.5 * h)
        k23 = difY(XRK4[i - 1] + 0.5 * k12 * h, YRK4[i - 1] + 0.5 * k22 * h, T[i - 1] + 0.5 * h)
        k33 = difZ(XRK4[i - 1] + 0.5 * h * k12, YRK4[i - 1] + 0.5 * h * k22, ZRK4[i - 1] + 0.5 * h * k32, ai, tetai, bi,
                   tiempo[i - 1] + 0.5*h)
        k14 = difX(XRK4[i - 1] + 0.5 * k13 * h, YRK4[i - 1] + 0.5 * k23 * h, T[i - 1] + 0.5 * h)
        k24 = difY(XRK4[i - 1] + 0.5 * k13 * h, YRK4[i - 1] + 0.5 * k23 * h, T[i - 1] + 0.5 * h)
        k34 = difZ(XRK4[i - 1] + 0.5 * h * k13, YRK4[i - 1] + 0.5 * h * k23, ZRK4[i - 1] + 0.5 * h * k33, ai, tetai, bi,
                   tiempo[i - 1] + 0.5*h)
        XRK4[i] = XRK4[i - 1] + (h / 6.0) * (k11 + k12 + k13 + k14)
        YRK4[i] = YRK4[i - 1] + (h / 6.0) * (k21 + k22 + k23 + k24)
        ZRK4[i] = ZRK4[i - 1] + (h / 6.0) * (k31 + k32 + k33 + k34)
    return ZRK4

R = 180 #Hz  EJEMPLO DEL FACTOR DE RUIDO

def Ruido():
    R = int(var_factorruido.get())
    xruido = tiempo()   # Se mapea a lo largo del ECG
    yrruido = np.array( 0.01 * np.sin((0.1 * R) * xruido))  # el factor de ruido altera la frecuencia de la funcióin seno
    return yrruido

#grafica de los metodos

def GraficaEulerFor():
    R = int(var_factorruido.get())        # Es el factor de ruido que el usuario ingreso en la interfaz
    accionGraficadora.cambiarEstado(1)   # Cambia el estado de la grafica ha la opcion seleccionada
    if R > 0:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(),EulerAdelante(),"pink")  # subplot(filas, columnas, item)
        fig.add_subplot(111).plot(tiempo(), Ruido(), "pink")
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
    else:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), EulerAdelante(), "pink")  # subplot(filas, columnas, item)
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)

def GraficaEulerBack():
    R = int(var_factorruido.get())      # Es el factor de ruido que el usuario ingreso en la interfaz
    accionGraficadora.cambiarEstado(2)  # Cambia el estado de la grafica ha la opcion seleccionada
    if R > 0:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), EulerBack(), "yellow")  # subplot(filas, columnas, item)
        fig.add_subplot(111).plot(tiempo(), Ruido(), "yellow")
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
    else:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), EulerBack(), "yellow")  # subplot(filas, columnas, item)
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
def GraficaEulerModificado():
    R = int(var_factorruido.get())      # Es el factor de ruido que el usuario ingreso en la interfaz
    accionGraficadora.cambiarEstado(3)  # Cambia el estado de la grafica ha la opcion seleccionada
    if R > 0:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), EulerModificado(), "red")  # subplot(filas, columnas, item)
        fig.add_subplot(111).plot(tiempo(), Ruido(), "red")
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
    else:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(),  EulerModificado(), "red")  # subplot(filas, columnas, item)
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
def GraficaRK2():
    R = int(var_factorruido.get())       # Es el factor de ruido que el usuario ingreso en la interfaz
    accionGraficadora.cambiarEstado(4)  # Cambia el estado de la grafica ha la opcion seleccionada
    if R > 0:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), RK2(), "green")  # subplot(filas, columnas, item)
        fig.add_subplot(111).plot(tiempo(), Ruido(), "green")
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
    else:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), RK2(), "green")  # subplot(filas, columnas, item)
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
def GraficaRK4():
    R = int(var_factorruido.get())      # Es el factor de ruido que el usuario ingreso en la interfaz
    accionGraficadora.cambiarEstado(5)  # Cambia el estado de la grafica ha la opcion seleccionada
    if R > 0:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), RK4(), "purple")  # subplot(filas, columnas, item)
        fig.add_subplot(111).plot(tiempo(), Ruido(), "purple")
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)
    else:
        fig = plt.Figure(figsize=(4, 2), dpi=100)
        fig.add_subplot(111).plot(tiempo(), RK4(), "purple")  # subplot(filas, columnas, item)
        plt.close()
        plt.style.use('seaborn-darkgrid')
        Plot = FigureCanvasTkAgg(fig, master=frameMetodos)
        Plot.draw()
        Plot.get_tk_widget().place(x=0, y=0)

# DEFINIR localizacion de los puntos RR dependiendo de la frecuencia cardiaca ingresada
def amplitudIPM(fc):
    def conversion():
        if getattr(accionGraficadora, 'vigilanteGrafica') == "f":  # En esta parte se traduce las letras de la clase al tipo de metodo utilizado
            ecg = EulerAdelante()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "b":
            ecg = EulerBack()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "m":
            ecg = EulerModificado()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "r2":
            ecg = RK2()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "r4":
            ecg = RK4()
            return ecg

    ecgTamano = conversion()
    indice = int(len(ecgTamano) / 4) # se reduce el rango que se registra para heart rate (esto es debido a que
    ecg = conversion()[indice:]      # al principio algunos picos RR no están bien definidos

    if (fc <= 60):
        peaks, properties = sc.find_peaks(ecg, height=0.03, width=5)
    elif (fc<=100):
        peaks, properties = sc.find_peaks(ecg, height=0.02, width=1)     # Estas restricciones del detector de picos se hace con
    elif (fc <=120):                                                   # frecuencia de muestreo de 340
        peaks, properties = sc.find_peaks(ecg, height=0.016, width=2)
    elif (fc > 120):
        peaks, properties = sc.find_peaks(ecg, height=0.014, width=2)
    return peaks,properties

# HR el cual se hace por medio de funcion que detecte los picos
def HR():
    def conversion():
        if getattr(accionGraficadora,
                   'vigilanteGrafica') == "f":  # En esta parte se traduce las letras de la clase al tipo de metodo utilizado
            ecg = EulerAdelante()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "b":
            ecg = EulerBack()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "m":
            ecg = EulerModificado()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "r2":
            ecg = RK2()
            return ecg
        elif getattr(accionGraficadora, 'vigilanteGrafica') == "r4":
            ecg = RK4()
            return ecg


    ecgTamano = conversion()
    indice = int(len(ecgTamano) / 4)   # se reduce el rango que se registra para heart rate (esto es debido a que
    ecg = conversion()[indice:]        # al principio  algunos picos RR no están bien definidos

    fs = int(var_frecuenciamuestreo.get())

    time = np.arange(ecg.size) / fs
    peaks, properties = amplitudIPM(int(var_frecuenciacardiaca.get()))

    fpeak = properties['peak_heights']
    # taco
    time_ecg = time[peaks]
    time_ecg = time_ecg[1:]
    taco = np.diff(time[peaks])

    tacobpm = 60 / taco
    Hr = np.mean(tacobpm)
    var_hallarHR.set(round(Hr,4))   # se cambia el label de la interfaz por la informacion del heart rate
    return Hr


def MensajeH():
    tk.messagebox.showinfo("", "Heat rate promedio :"+ str(HR()))

# Funcion que permite guardar los datos de las frecuencias (cardiaca,ruido y muestreo) y numero de latidos.
# La información se empaqueta en archivo bin-double
def exportarDatos():
    tiempoE = tiempo()
    fll = open("ECGXtime.bin", "wb")  # crea un archivo de tipo bin el cual se puede escribir sobre ella
    empaque1 = struct.pack("d" * len(tiempoE), *tiempoE)  # Se empaqueta el eje del tiempo con tamaño "d"
    fll.write(empaque1)  # en el archivo creado se escribe la informacion empaquetada
    fll.close()  # se cierra el archivo

    fll = open("ECGpicos.bin", "wb")  # crea un archivo de tipo bin el cual se puede escribir sobre ella
    empaque2 = struct.pack("d" * len(EulerAdelante()), *EulerAdelante())  # Se empaqueta el eje Z el cual tiene el valor de las ondas PQRST con tamaño "d"
    fll.write(empaque2)  # en el archivo creado se escribe la informacion empaquetada
    fll.close()  # se cierra el archivo
def exportarInterface():
    tk.messagebox.showinfo("", "Ha exportado los datos")
    exportarDatos()   #Una vez se selecciona el botón, se procede a mostrar en una ventana adicional la grafica del ECG guardado.


def importarDatos():
    fllX = open("ECGXtime.bin", "rb")
    lecturaX = fllX.read()
    fllY = open("ECGpicos.bin", "rb")
    lecturaY = fllY.read()

    desempaqueX = struct.unpack("d" * int(len(lecturaX) / 8), lecturaX)   # Para leer correctamente los archivos se debe desempacar con el tamano double "8"
    desempaqueY = struct.unpack("d" * int(len(lecturaY) / 8), lecturaY)

    fllX.close()
    fllY.close()

    plt.plot(desempaqueX,desempaqueY)         # Se mostrará cuando el usuario desee importar lo datos(es decir que debe clickear el botón "importar"
    plt.title("Grafica de datos importados")


def importarInterface():
    tk.messagebox.showinfo("", "Ha importado los datos ECG")
    importarDatos()


#botones de metodos de solucion
BotoneulerA = ttk.Button(master=frameED, text="Euler adelante", style="1.TButton",command=GraficaEulerFor,width = 13).place(x=160, y=68)
Botoneuleratras = ttk.Button(master=frameED, text="Euler atras", style="1.TButton",command=GraficaEulerBack,width = 13).place(x=160, y=105)
Botoneulermod = ttk.Button(master=frameED, text="Euler modificado", style="1.TButton",command=GraficaEulerModificado ,width = 13).place(x=160, y=142)
BotonRK2 = ttk.Button(master=frameED, text="Runge-Kutta2", style="1.TButton",command=GraficaRK2,width = 13).place(x=160, y=179)
BotonRK4= ttk.Button(master=frameED, text="Runge-Kutta4", style="1.TButton",command= GraficaRK4,width = 13).place(x=160, y=216)


BotonhallarHR = ttk.Button(master=ventana, text="Hallar HR", style="3.TButton",command= MensajeH,width = 15).place(x=100, y=340)

#botones de exportar y cargar datos
BotonexportarD = ttk.Button(master=ventana, text="Exportar datos", style="3.TButton",command=exportarInterface ,width = 20).place(x=60, y=10)
Botoncargardatos = ttk.Button(master=ventana, text="Cargar datos", style="3.TButton",command=importarInterface ,width = 20).place(x=220, y=10)



#Boton que cambia
gris1 = Image.open("gris.png")
gris1 = gris1.resize((20,20), Image.ANTIALIAS)
gris1 = ImageTk.PhotoImage(gris1)
BotonCambia1 = ttk.Button(master = frameED, image = gris1, command = GraficaEulerFor).place(x = 40, y= 68)
BotonCambia2 = ttk.Button(master = frameED, image = gris1, command = GraficaEulerBack).place(x = 40, y= 105)
BotonCambia3 = ttk.Button(master = frameED, image = gris1, command = GraficaEulerModificado).place(x = 40, y= 142)
BotonCambia4 = ttk.Button(master = frameED, image = gris1, command = GraficaRK2).place(x = 40, y= 179)
BotonCambia5 = ttk.Button(master = frameED, image = gris1, command = GraficaRK4).place(x = 40, y= 216)





ventana.mainloop()
##

