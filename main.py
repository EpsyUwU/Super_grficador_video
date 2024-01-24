import subprocess
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import cv2 as cv
import os

# Funciones para graficar
def f_sin(x):
    return np.sin(x)

def f_cos(x):
    return np.cos(x)

def x_al_cuadrado(x):
    return x**2

def x_al_cubo(x):
    return x**3

def x_ala_cuarta(x):
    return x**4

func_dict = {'sin': f_sin, 'cos': f_cos, 'x^2': x_al_cuadrado, 'x^3': x_al_cubo, 'x^4': x_ala_cuarta}

# Crear la ventana
root = tk.Tk()
root.title("Graficador de funciones")

# Crear el selector de funciones
label_func = tk.Label(root, text="Escoge la funcion:")
label_func.pack()

func_var = tk.StringVar()
func_var.set('sin')  # valor por defecto
func_menu = ttk.Combobox(root, textvariable=func_var, values=list(func_dict.keys()))
func_menu.pack()

# Crear los campos para los límites del eje x
label_xmin = tk.Label(root, text="x min:")
label_xmin.pack()
xmin_entry = tk.Entry(root)
xmin_entry.pack()

label_xmax = tk.Label(root, text="x max:")
label_xmax.pack()
xmax_entry = tk.Entry(root)
xmax_entry.pack()

# Lista para guardar las funciones seleccionadas
selected_funcs = []

# Botón para agregar función a la lista
def add_func():
    func = func_dict[func_var.get()]
    selected_funcs.append(func)
    tk.messagebox.showinfo("Función agregada", "Función agregada. Por favor, escoge la siguiente.")

add_button = tk.Button(root, text="Agregar función", command=add_func)
add_button.pack()

# Botón para graficar

def plot_func():
    xmin = float(xmin_entry.get())
    xmax = float(xmax_entry.get())
    x = np.linspace(xmin, xmax, 30)

    fig, ax = plt.subplots()

    # Calcular los valores de y para cada función
    y_values = [func(x) for func in selected_funcs]

    def actualizarPlot(i):
        ax.clear()
        for j, func in enumerate(selected_funcs):
            if i >= j * len(x) and i < (j + 1) * len(x):
                y = y_values[j]
                ax.plot(x[:i - j * len(x) + 1], y[:i - j * len(x) + 1])
                ax.set_xlim([xmin, xmax])
                ax.set_ylim([min(y), max(y)])  # calcular los límites del eje y para cada función

    animar = FuncAnimation(fig, actualizarPlot, frames=len(x) * len(selected_funcs), interval=0, cache_frame_data=False, repeat=False)
    grabarVideo((fig, animar), 'video.mp4')


def grabarVideo(animacion, nombre_video):
    fig, animar = animacion
    animar.save(nombre_video, writer='ffmpeg', fps=15, dpi=70)
    plt.close(fig)
    selected_funcs.clear()
    subprocess.call(['start', nombre_video], shell=True)

plot_button = tk.Button(root, text="Graficar y grabar", command=plot_func)
plot_button.pack()

root.mainloop()






