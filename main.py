from tkinter import *
from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PIL import Image, ImageTk
from tkinter import messagebox


def resolver_ecuacion_cuadratica(a, b, c):
    # Calculamos el discriminante
    discriminante = b**2 - 4*a*c

    if discriminante > 0:
        # Dos soluciones reales distintas
        solucion1 = (-b + sqrt(discriminante)) / (2*a)
        solucion2 = (-b - sqrt(discriminante)) / (2*a)

        solutions = [solucion1,solucion2]

        return solutions
    elif discriminante == 0:
        # Una sola solución real (raíz doble)
        solucion = -b / (2*a)

        solutions = [solucion]
        return solutions
    else:
        solutions = [-100,-100,-100]
        return solutions
    

    
def validar_choca_obstaculo(xObsc,yObsc,valores_teta,v,g,hf,h0,L):

    if((hf == yObsc and L == xObsc) or (h0 == yObsc and 0 == xObsc)):
        return (True,-200)
    
    


    if len(valores_teta) ==1:

        if(xObsc> L):
            return(False,valores_teta[0])
        
        tiempo = xObsc/(v*cos(radians(valores_teta[0])))

        y_cord= (v*sin(radians(valores_teta[0]))*tiempo - (g*tiempo**2)/2) + h0

        print(f"ycord {y_cord}")


        if(round(y_cord,2) == round(yObsc,2)):
            return(True,-100)
        else:
            return(False,valores_teta[0])

    
        
    elif len(valores_teta) ==2:

        if(valores_teta[0] > valores_teta[1]):
            angulo_final = valores_teta[1]
            angulo_opuesto= valores_teta[0]
        else:
            angulo_final = valores_teta[0]
            angulo_opuesto = valores_teta[1]

        if(xObsc> L):
            return(False,angulo_final)
            
            
        tiempo = xObsc/(v*cos(radians(angulo_final)))
        y_cord= (v*sin(radians(angulo_final))*tiempo - (g*tiempo**2)/2 )+h0

        print(f"ycord {y_cord}")

        if(round(y_cord,2) == round(yObsc,2)):
            return(False,angulo_opuesto)
        else:
            return(False,angulo_final)
        

        

def verificar_valores_maximos(v,h0,g,L,hf):
    altura_maxima= ((v**2 )*(sin(radians(45))**2))/(2*g)
    altura_maxima = altura_maxima + h0

    primer_termino = (v **2 * (sin(radians(90))))/g
    segundo_termino = (v**2)/(g*tan(radians(90)))


    distancia_maxima = primer_termino + segundo_termino

    print(f"Altura maxima {altura_maxima}")
    print(f"Distancia maxima {distancia_maxima}")

    if(hf>altura_maxima or L>distancia_maxima):
        return False
    else:
        return True
        

def es_numero(nuevo_valor):
    try:
     
        if(len(nuevo_valor)>=1):
            if nuevo_valor[0] == "-" and len(nuevo_valor) == 1:
                return True
            else:
                numero = float(nuevo_valor)
                return True
        
    except ValueError:
        return False
    

def es_numeroPositivo(nuevo_valor):
    try:

        if(float(nuevo_valor)>=0):
            return True
        
    except ValueError:
        return False

def validar_masa(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de masa")
        return False

def validar_gravedad(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de gravedad")
        return False
def validar_constante_resorte(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de constante de resorte")
        return False

def validar_altura_objetivo(nuevo_valor):
    if es_numero(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de altura del objetivo")
        return False

def validar_altura_disparador(nuevo_valor):
    if es_numero(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de altura del disparador")
        return False

def validar_distancia_objetivo(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de distancia al objetivo (Positivos)")
        return False

def validar_obstaculo_x(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de coordenada x del obstáculo (Positivos)")
        return False

def validar_obstaculo_y(nuevo_valor):
    if es_numero(nuevo_valor) or nuevo_valor == "" :
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de coordenada y del obstáculo")
        return False
    
def habilitar_envio():
    for entry in entries:
        if not entry.get():
            enviar_button.config(state=DISABLED)
            return
    enviar_button.config(state=NORMAL)


def parabolic_trajectory(v,h0,hf,g,xObsc,yObsc,L,y, distancia_resorte):
     # Crea una fuente más grande y en negritas
     font_style = ("Helvetica", 14, "bold")

     
     band = verificar_valores_maximos(v,h0,g,L,hf)

     if(band==True):

        A = g*L**2

        B =-2*v**2*L

        C = 2*y*v**2+ A


        valores_teta = []

        soluciones = resolver_ecuacion_cuadratica(A, B, C)

        if len(soluciones) == 2:

            angulo = arctan(soluciones[0])
            valores_teta.append(degrees(angulo))
            angulo = arctan(soluciones[1])
            valores_teta.append(degrees(angulo))
            
        elif len(soluciones) == 1:
            angulo = arctan(soluciones[0])
            valores_teta.append(degrees(angulo))

        elif len(soluciones) == 3:
            valores_teta = [-100,-100,-100]

        for valor in valores_teta:
            if len(valores_teta) >= 1 and len(valores_teta) <= 2:
                print(f"valor {valor} grados")


            

        if(len(valores_teta) >=1 and len(valores_teta) <=2):

            valor_funcion = validar_choca_obstaculo(xObsc,yObsc,valores_teta,v,g,hf,h0,L)

            if(valor_funcion[0]) == False:
              
                angulo_final= valor_funcion[1]


                anguloL = Label(variables_salidas_frame, text=f'Ángulo: {round(angulo_final,2)}°', fg="#010101", font=font_style, bg="#D4D4D4")
                anguloL.grid(row=0, column=0, sticky="nswe", pady=37.5, padx=(200,20))


                compresionL = Label(variables_salidas_frame, text=f'Compresión: {distancia_resorte*100}%', fg="#010101", font=font_style, bg="#D4D4D4")
                compresionL.grid(row=0, column=1, sticky="nswe", pady=37.5, padx=(20))

                print(f'vo :  {v}')
                
             
                datos_x = linspace(0,int(L), 10000)
                ax.clear()  # Limpia la gráfica anterior

                y = []

         
                for x in datos_x:
                    y_value = h0 + (x * tan(radians(valor_funcion[1])) - ((g * x**2) / (2 * v**2 * cos(radians(valor_funcion[1]))**2)))
                    y.append(y_value)



                # Ajusta las listas para que tengan la misma longitud
                min_length = min(len(datos_x), len(y))
                datos_x = datos_x[:min_length]
                y = y[:min_length]


                # Agregar la función
                ax.plot(datos_x, y, label="Función Tiro Parabolico")

                # Agrega el punto
                ax.plot(xObsc, yObsc, 'ro', label="Obstaculo")
                ax.plot(0,h0, 'bo', label="Disparador")
                ax.plot(L,hf, 'go', label="Objetivo")

                # Ajustar los límites de los ejes automáticamente
                ax.relim()
                ax.autoscale_view()

                ax.set_title("Tiro Parabólico")
                ax.set_xlabel("Eje X (Longitud Horizontal)")
                ax.set_ylabel("Eje Y (Longitud Vertical)")
                ax.legend()
           
                canvas.draw()

            elif (valor_funcion[0]) == True and valor_funcion[1] == -200:        
                messagebox.showerror("Eror","Choca el Obstaculo (Estan en las miasmas coordenadas de inicio o final)")
            
            elif (valor_funcion[0]) == True and valor_funcion[1] == -100:
                messagebox.showerror("Eror","Choca el Obstaculo (No es posible chocar el objetivo ya que la unica alternativa choca con el obstaculo)")
             
            else:
                messagebox.showerror("Eror","No es posible supera las altura o distancia maxima que se puede obtener")
        

        


    

def enviar_datos():

    masa = float(entries[0].get())
    gravedad = float(entries[1].get())
    constante_resorte = float(entries[2].get())
    altura_objetivo = float(entries[3].get())
    altura_disparador = float(entries[4].get())
    distancia_objetivo = float(entries[5].get())
    obstaculo_x = float(entries[6].get())
    obstaculo_y = float(entries[7].get())

 

    h0=altura_disparador #Altura del disparador respecto al piso
    hf= altura_objetivo #Altura del suelo al objetivo
    L = distancia_objetivo
    g= gravedad

    y = hf-h0

    #Coordenadas del obstaculo
    xObsc = obstaculo_x
    yObsc = obstaculo_y



    distancia_resorte = 1
    v = sqrt((constante_resorte / masa) * distancia_resorte ** 2)

    parabolic_trajectory(v, h0, hf, g, xObsc, yObsc, L, y, distancia_resorte)


      
    


def limpiar_campos():
    enviar_button.config(state=DISABLED)
    for entry in entries:
        entry.delete(0, END)




# Configuración de la ventana principal de Tkinter
raiz = Tk()
raiz.title("Calculadora de Tiro Parabolico")

# Establecer colores (Paleta Azul)
color_campos = "#BBDEFB"  # Azul claro
color_botones = "#1976D2"  # Azul oscuro

# Configurar colores
raiz.configure()

# Hacer la ventana redimensionable
raiz.resizable(0, 0)

# Dimensiones iniciales de la ventana

raiz.geometry("1400x700")


# entradas izquierda

entradas_titulo_frame = Frame(raiz, bg="#F0EFEB")
menu_variables_frame = Frame(raiz, width=700, bg="#F0EFEB", padx=(16))
variables_frame = Frame(raiz, width=700, bg="#F0EFEB")
botones_frame = Frame(raiz, width=700, bg="#F0EFEB")
enviar_button = Button(botones_frame, text="Enviar", command=enviar_datos, bg=color_botones, fg="white", state=DISABLED, cursor='hand2',font=("Helvetica", 14, "bold"), border=0)
limpiar_button = Button(botones_frame, text="Limpiar", command=limpiar_campos, bg=color_botones, fg="white", cursor='hand2',font=("Helvetica", 14, "bold"),border=0)

limpiar_button.pack(side="left",fill="both", expand=True, padx=100, pady=(2,60))
enviar_button.pack(side="left", fill="both", expand=True, padx=100, pady=(2,60))

entradas_titulo = Label(entradas_titulo_frame, text="Entradas",font=("Helvetica", 16, "bold"), fg="#010101")
entradas_titulo.pack(expand=False, pady=20)


#etiquetas menu de variables
Label(menu_variables_frame, text="Variables", fg="#010101",font=("Helvetica", 10, "bold")).pack()
Label(menu_variables_frame, text="Masa del balón = m    Gravedad = g    Constante del resorte = k",fg="#010101",font=("Helvetica", 10)).pack()
Label(menu_variables_frame, text="Distancia al centro del objetivo = L     Altura del suelo al objetivo = hf     Altura del disparador respecto al piso = ho",fg="#010101",font=("Helvetica", 10)).pack()
Label(menu_variables_frame, text="Coordenada x del obstáculo = x   Coordenada y del obstáculo = y",fg="#010101",font=("Helvetica", 10)).pack()



# Etiquetas 1
labels = ["m:", "g:", "k:",
          "hf:"]


for i, label_text in enumerate(labels):
    Label(variables_frame, text=label_text, fg="#010101",font=("Helvetica", 14, "italic")).grid(row=i+1, column=0, sticky="e", padx=(40,0))



entries = []
validaciones = [validar_masa, validar_gravedad, validar_constante_resorte,
                validar_altura_objetivo]

for i in range(len(labels)):
    entry = Entry(variables_frame, bg=color_campos,font=("Helvetica", 14), cursor='hand2')

    # Asignar función de validación si está definida
    if validaciones[i]:
        validacion = (variables_frame.register(validaciones[i]), "%P")
        entry.config(validate="key", validatecommand=validacion)

    entry.grid(row=i+1, column=1, pady=5)
    entry.bind("<KeyRelease>", lambda event: habilitar_envio())  # Llama a la función cada vez que se libera una tecla
    entries.append(entry)

# Etiquetas1
labels = ["kg", "m/s²", "N/m",
          "m",]

for i, label_text in enumerate(labels):
    Label(variables_frame, text=label_text, fg="#010101",font=("Helvetica", 14, "italic")).grid(row=i+1, column=2, sticky="w", pady=20)


    
#Etiquetas 2
labels2 = ["ho:",
          "L:", "x:", "y:"]

for i, label_text in enumerate(labels2):
    Label(variables_frame, text=label_text, fg="#010101",font=("Helvetica", 14, "italic")).grid(row=i+1, column=3, sticky="e", padx=(40,0))



validaciones = [validar_altura_disparador,
                validar_distancia_objetivo, validar_obstaculo_x, validar_obstaculo_y]

for i in range(len(labels2)):
    entry = Entry(variables_frame, bg=color_campos,font=("Helvetica", 14), cursor='hand2')

    # Asignar función de validación si está definida
    if validaciones[i]:
        validacion = (variables_frame.register(validaciones[i]), "%P")
        entry.config(validate="key", validatecommand=validacion)

    entry.grid(row=i+1, column=5, pady=5)
    entry.bind("<KeyRelease>", lambda event: habilitar_envio())  # Llama a la función cada vez que se libera una tecla
    entries.append(entry)

# Etiquetas2
labels2 = ["m",
          "m", "x", "y"]

for i, label_text in enumerate(labels2):
    Label(variables_frame, text=label_text, fg="#010101",font=("Helvetica", 14, "italic")).grid(row=i+1, column=6, sticky="w")

#salidas derecha

salidas_titulo_frame = Frame(raiz, bg="#D4D4D4")
variables_salidas_frame = Frame(raiz, width=700,height=100, bg="#D4D4D4")
grafica_frame = Frame(raiz, width=700, bg="#D4D4D4")


limpiar_button.pack(side="left",fill="both", expand=True, padx=100, pady=60)
enviar_button.pack(side="left", fill="both", expand=True, padx=100, pady=60)

fig = Figure(figsize=(5, 4), dpi=100, constrained_layout= True, facecolor="#D4D4D4")
ax = fig.add_subplot(111)

#Crear un lienzo de Matplotlib
canvas = FigureCanvasTkAgg(fig, master=grafica_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=100, y=30)

#Personalizar el gráfico y sus etiquetas aquí si es necesario
ax.set_title("Simulación Tiro Parabólico")
ax.set_xlabel("Eje X (Longitud Horizontal)")
ax.set_ylabel("Eje Y (Longitud Vertical)")


salidas_titulo = Label(salidas_titulo_frame, text="Salidas",font=("Helvetica", 16, "bold"),fg="#010101", bg="#D4D4D4")
salidas_titulo.pack(expand=False, pady=20)

# titulo
titulo_Frame = Frame(raiz, bg="#283618")
titulo = Label(titulo_Frame, text="Concurso Open Doors - Calculadora de Tiro Parabólico",font=("Helvetica", 20, "bold"),fg="white", bg="#283618")
titulo.pack(fill="both", expand=True, pady=10)

titulo_Frame.grid(row=0, column=0, columnspan=4, sticky="ew")
entradas_titulo_frame.grid(row=1, column=0,columnspan=2, sticky="nwes")
salidas_titulo_frame.grid(row=1, column=2,columnspan=2, sticky="nwes")
menu_variables_frame.grid(row=2, column=0,columnspan=2, sticky="wnes")
variables_frame.grid(row=3, column=0,columnspan=2, rowspan=3, sticky="wnes")
botones_frame.grid(row=6, column=0, columnspan=2, sticky="wnes")
variables_salidas_frame.grid(row= 2, column= 2, columnspan=2, sticky="wens")
grafica_frame.grid(row= 3, column=2 ,columnspan=2, rowspan=4, sticky="wens")

raiz.rowconfigure(3, weight=1)



raiz.mainloop()