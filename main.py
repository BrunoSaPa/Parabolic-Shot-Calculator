from tkinter import *
from numpy import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox


#funcion para resolver ecuaciones cuadraticas
def resolver_ecuacion_cuadratica(a, b, c):
    # Calculamos el discriminante
    discriminante = b**2 - 4*a*c

    if discriminante > 0:
        # Dos soluciones reales distintas
        solucion1 = (-b + sqrt(discriminante)) / (2*a)
        solucion2 = (-b - sqrt(discriminante)) / (2*a)
        #se retornan las dos raices
        solutions = [solucion1,solucion2]

        return solutions
    elif discriminante == 0:
        # Una sola solución real (raíz doble)
        solucion = -b / (2*a)
        #se retorna la única raiz
        solutions = [solucion]
        return solutions
    else:
        #al no existir soluciones, se retorna -100,-100,-100
        solutions = [-100,-100,-100]
        return solutions
    

#funcion para validar si con una trayectoria dada choca en un obstaculo
def validar_choca_obstaculo(xObsc,yObsc,valores_tetha,v,g,hf,h0,L):
    #verifica si el obstaculo se encuentra en el inicio o al final de la trayectoria del objetivo
    if((hf == yObsc and L == xObsc) or (h0 == yObsc and 0 == xObsc)):
        return (True,-200)

    #Verifica cuando tetha tiene una sola solucion
    if len(valores_tetha) ==1:
        #verifica si el obstaculo se encuentra después de L
        if(xObsc> L):
            return(False,valores_tetha[0])
    
        #calcula tiempo y y_cord para el tiempo calculado
        tiempo = xObsc/(v*cos(radians(valores_tetha[0])))
        y_cord= (v*sin(radians(valores_tetha[0]))*tiempo - (g*tiempo**2)/2) + h0

        #redondea el resultado de la y_cord a 2 decimales, si choca retorna true y si no choca returna falso
        if(round(y_cord,2) == round(yObsc,2)):
            return(True,-100)
        else:
            return(False,valores_tetha[0])

    
    #verifica si choca el proyectil cuando se tienen dos soluciones    
    elif len(valores_tetha) ==2:
        #toma primero el angulo menor y retorna aquel angulo que no choque
        if(valores_tetha[0] > valores_tetha[1]):
            angulo_final = valores_tetha[1]
            angulo_opuesto= valores_tetha[0]
        else:
            angulo_final = valores_tetha[0]
            angulo_opuesto = valores_tetha[1]
            
        #verifica si el obstaculo se encuentra después de L
        if(xObsc> L):
            return(False,angulo_final)
            
        #calcula tiempo y y_cord para el tiempo calculado    
        tiempo = xObsc/(v*cos(radians(angulo_final)))
        y_cord= (v*sin(radians(angulo_final))*tiempo - (g*tiempo**2)/2 )+h0

        #redondea el resultado de la y_cord a 2 decimales, si choca retorna true y el angulo mayor, si no choca returna false y el angulo menor
        if(round(y_cord,2) == round(yObsc,2)):
            return(False,angulo_opuesto)
        else:
            return(False,angulo_final)
        

        

        
#funcion para determinar que la cadena ingresada sea un numero solamente
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
    
#funcion para determinar que la cadena ingresada sea un numero positivo
def es_numeroPositivo(nuevo_valor):
    try:

        if(float(nuevo_valor)>=0):
            return True
        
    except ValueError:
        return False

#funcion para validar que la masa sea positiva
def validar_masa(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números positivo en el campo de masa")
        return False
    
#funcion para validar que la gravedad sea positiva
def validar_gravedad(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números positivos en el campo de gravedad")
        return False
    
#funcion para validar que la constante del resorte sea positiva
def validar_constante_resorte(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números positivos en el campo de constante de resorte")
        return False

#funcion para validar que la altura del objetivo sea un valor numerico
def validar_altura_objetivo(nuevo_valor):
    if es_numero(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de altura del objetivo")
        return False

#funcion para validar que la altura del disparador sea un valor numerico
def validar_altura_disparador(nuevo_valor):
    if es_numero(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de altura del disparador")
        return False

#funcion para validar que la distancia al objetivo sea un valor positivo
def validar_distancia_objetivo(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números positivos en el campo de distancia al objetivo ")
        return False

#funcion para validar que la cordenada x del obstaculo sea un valor positivo
def validar_obstaculo_x(nuevo_valor):
    if es_numeroPositivo(nuevo_valor) or nuevo_valor == "":
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números positivos en el campo de coordenada x del obstáculo")
        return False

#funcion para validar que la cordenada y del obstaculo sea un valor numerico
def validar_obstaculo_y(nuevo_valor):
    if es_numero(nuevo_valor) or nuevo_valor == "" :
        return True
    else:
        messagebox.showerror("Error", "Por favor, ingrese solo números en el campo de coordenada y del obstáculo")
        return False
    
#funcion para habilitar el boton de enviar cuando todas las casillas de entrada contengan un valor
def habilitar_envio():
    for entry in entries:
        if not entry.get():
            enviar_button.config(state=DISABLED)
            return
    enviar_button.config(state=NORMAL)

#funcion para determinar la trayectoria del objetivo
def parabolic_trajectory(v,h0,hf,g,xObsc,yObsc,L,y, distancia_resorte):
     # Crea una fuente más grande y en negritas
    font_style = ("Helvetica", 14, "bold")

    #coeficientes para ecuacion del angulo a calcular
    A = g*L**2

    B =-2*v**2*L

    C = 2*y*v**2+ A 

    valores_tetha = []

    #invocacion para resolver la ecuacion cuadratica con los coeficientes anteriormente definidos
    soluciones = resolver_ecuacion_cuadratica(A, B, C)

    #cuando existan dos soluciones, se obtiene el angulo y se guardan las soluciones en un arreglo
    if len(soluciones) == 2:
        angulo = arctan(soluciones[0])
        valores_tetha.append(degrees(angulo))
        angulo = arctan(soluciones[1])
        valores_tetha.append(degrees(angulo))
    
    #cuando exista una soluciones, se obtiene el angulo y se guarda la solucion en un arreglo
    elif len(soluciones) == 1:
        angulo = arctan(soluciones[0])
        valores_tetha.append(degrees(angulo))

    #cuando no existan soluciones se guardan los valores de -100,-100,-100 en el arreglo
    elif len(soluciones) == 3:
        valores_tetha = [-100,-100,-100]


    #ciclo para imprimir los angulos de la solucion en la terminal
    for valor in valores_tetha:
        if len(valores_tetha) >= 1 and len(valores_tetha) <= 2:
            print(f"valor {valor} grados")

    print("--------------------------------------------------------")

    #cuando tetha tenga soluciones reales
    if(len(valores_tetha) >=1 and len(valores_tetha) <=2):

        valor_funcion = validar_choca_obstaculo(xObsc,yObsc,valores_tetha,v,g,hf,h0,L)

        if(valor_funcion[0]) == False:
            angulo_final= valor_funcion[1]

            anguloL = Label(variables_salidas_frame, text=f'Ángulo: {round(angulo_final,2)}°', fg="#010101", font=font_style, bg="#D4D4D4")
            anguloL.grid(row=0, column=0, sticky="nswe", pady=37.5, padx=(200,20))


            compresionL = Label(variables_salidas_frame, text=f'Compresión: {distancia_resorte*100}%', fg="#010101", font=font_style, bg="#D4D4D4")
            compresionL.grid(row=0, column=1, sticky="nswe", pady=37.5, padx=(20))
                
            #determinacion de valores para datos x
            datos_x = linspace(0,(L), 10000)
            ax.clear()  # Limpia la gráfica anterior

            y = []

            #generacion de valores para y
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
            ax.plot(xObsc, yObsc, 'ro', label="Obstáculo")
            ax.plot(0,h0, 'bo', label="Disparador")
            ax.plot(L,hf, 'go', label="Objetivo")

            # Ajustar los límites de los ejes automáticamente
            ax.relim()
            ax.autoscale_view()

            ax.set_title("Tiro Parabólico")
            ax.set_xlabel("Eje X (Longitud Horizontal)")
            ax.set_ylabel("Eje Y (Longitud Vertical)")
            ax.legend()
           #imprimir la grafica
            canvas.draw()

        elif (valor_funcion[0]) == True and valor_funcion[1] == -200:        
                messagebox.showerror("Eror","Choca el Obstaculo (Estan en las miasmas coordenadas de inicio o final)")
            
        elif (valor_funcion[0]) == True and valor_funcion[1] == -100:
                messagebox.showerror("Eror","Choca el Obstaculo (No es posible impactar el objetivo ya que la unica alternativa choca con el obstaculo)")

    else:
            messagebox.showerror("Eror","No es posible impactar el objetivo ya que no hay soluciones reales")
             

    
#funcion para captar los datos enviados
def enviar_datos():
    #captacion de datos
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

    #adecuar la linea de referencia respecto al disparador
    y = hf-h0

    #Coordenadas del obstaculo
    xObsc = obstaculo_x
    yObsc = obstaculo_y

    #calcular la velocidad inicial con una compresion del resorte del 100%
    distancia_resorte = 1
    v = sqrt((constante_resorte / masa) * distancia_resorte ** 2)

    #llamada a funcion para determinar la trayectoria
    parabolic_trajectory(v, h0, hf, g, xObsc, yObsc, L, y, distancia_resorte)
  

#funcion para limpiar todos los campos de entrada
def limpiar_campos():
    enviar_button.config(state=DISABLED)
    for entry in entries:
        entry.delete(0, END)
    fig.clf()




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


#entradas izquierda
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
Label(menu_variables_frame, text="Variables", fg="#010101",font=("Helvetica", 12, "bold")).pack()
Label(menu_variables_frame, text="Masa del balón = m    Gravedad = g    Constante del resorte = k",fg="#010101",font=("Helvetica", 10)).pack()
Label(menu_variables_frame, text="Distancia al centro del objetivo = L     Altura del suelo al objetivo = hf     Altura del disparador respecto al piso = ho",fg="#010101",font=("Helvetica", 10)).pack()
Label(menu_variables_frame, text="Coordenada x del obstáculo = x      Coordenada y del obstáculo = y",fg="#010101",font=("Helvetica", 10)).pack()



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
          "m", "m", "m"]

for i, label_text in enumerate(labels2):
    Label(variables_frame, text=label_text, fg="#010101",font=("Helvetica", 14, "italic")).grid(row=i+1, column=6, sticky="w")

#salidas derecha
salidas_titulo_frame = Frame(raiz, bg="#D4D4D4")
variables_salidas_frame = Frame(raiz, width=700,height=100, bg="#D4D4D4")
grafica_frame = Frame(raiz, width=700, bg="#D4D4D4")


limpiar_button.pack(side="left",fill="both", expand=True, padx=100, pady=60)
enviar_button.pack(side="left", fill="both", expand=True, padx=100, pady=60)

fig = Figure(figsize=(5, 4), dpi=100, constrained_layout= True, facecolor="#D4D4D4")
#definicion de la figura de tipo grafica
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


#deficion del layout
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